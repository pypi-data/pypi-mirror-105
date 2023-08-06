CREATE EXTENSION IF NOT EXISTS postgis;
CREATE SCHEMA IF NOT EXISTS partman;
CREATE EXTENSION IF NOT EXISTS pg_partman SCHEMA partman;
CREATE SCHEMA IF NOT EXISTS pgstac;


SET SEARCH_PATH TO pgstac, public;

CREATE TABLE versions (
  version text PRIMARY KEY,
  datetime timestamptz DEFAULT now() NOT NULL
);

/* converts a jsonb text array to a pg text[] array */
CREATE OR REPLACE FUNCTION textarr(_js jsonb)
  RETURNS text[] AS $$
  SELECT ARRAY(SELECT jsonb_array_elements_text(_js));
$$ LANGUAGE sql IMMUTABLE PARALLEL SAFE;

/*
converts a jsonb text array to comma delimited list of identifer quoted
useful for constructing column lists for selects
*/
CREATE OR REPLACE FUNCTION array_idents(_js jsonb)
  RETURNS text AS $$
  SELECT string_agg(quote_ident(v),',') FROM jsonb_array_elements_text(_js) v;
$$ LANGUAGE sql IMMUTABLE PARALLEL SAFE;

CREATE OR REPLACE FUNCTION properties_idx(_in jsonb) RETURNS jsonb AS $$
WITH kv AS (
    SELECT key, value FROM jsonb_each(_in) WHERE key = 'datetime' OR jsonb_typeof(value) IN ('object','array')
) SELECT lower((_in - array_agg(key))::text)::jsonb FROM kv;
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE;
SET SEARCH_PATH TO pgstac, public;

CREATE TABLE IF NOT EXISTS collections (
    id VARCHAR GENERATED ALWAYS AS (content->>'id') STORED PRIMARY KEY,
    content JSONB
);

CREATE OR REPLACE FUNCTION create_collection(data jsonb) RETURNS VOID AS $$
    INSERT INTO collections (content)
    VALUES (data)
    ON CONFLICT (id) DO
    UPDATE
        SET content=EXCLUDED.content
    ;
$$ LANGUAGE SQL SET SEARCH_PATH TO pgstac, public;


CREATE OR REPLACE FUNCTION get_collection(id text) RETURNS jsonb AS $$
SELECT content FROM collections
WHERE id=$1
;
$$ LANGUAGE SQL SET SEARCH_PATH TO pgstac, public;

CREATE OR REPLACE FUNCTION all_collections() RETURNS jsonb AS $$
SELECT jsonb_agg(content) FROM collections;
;
$$ LANGUAGE SQL SET SEARCH_PATH TO pgstac, public;






CREATE OR REPLACE FUNCTION collections_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    IF pg_trigger_depth() = 1 THEN
        PERFORM create_collection(NEW.content);
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SET SEARCH_PATH TO pgstac, public;

CREATE TRIGGER collections_trigger
BEFORE INSERT ON collections
FOR EACH ROW EXECUTE PROCEDURE collections_trigger_func();
SET SEARCH_PATH TO pgstac, public;

CREATE TABLE IF NOT EXISTS items (
    id VARCHAR GENERATED ALWAYS AS (content->>'id') STORED PRIMARY KEY,
    content JSONB
);

CREATE TABLE IF NOT EXISTS items_search (
    id text NOT NULL,
    geometry geometry NOT NULL,
    properties jsonb,
    collection_id text NOT NULL,
    datetime timestamptz NOT NULL
)
PARTITION BY RANGE (datetime)
;

CREATE TABLE IF NOT EXISTS items_search_template (
    LIKE items_search
)
;
ALTER TABLE items_search_template ADD PRIMARY KEY (id);

SELECT partman.create_parent(
    'pgstac.items_search',
    'datetime',
    'native',
    'weekly',
    p_template_table := 'pgstac.items_search_template',
    p_start_partition := '2015-01-01',
    p_premake := 104
);


CREATE INDEX "datetime_id_idx" ON items_search (datetime, id);
CREATE INDEX "properties_idx" ON items_search USING GIN (properties);
CREATE INDEX "collection_idx" ON items_search (collection_id);
CREATE INDEX "geometry_idx" ON items_search USING GIST (geometry);


CREATE TYPE item AS (
    id text,
    geometry geometry,
    properties JSONB,
    collection_id text,
    datetime timestamptz
);

/*
Converts single feature into an items row
*/
CREATE OR REPLACE FUNCTION feature_to_item(value jsonb) RETURNS item AS $$
    SELECT
        value->>'id' as id,
        CASE
            WHEN value->>'geometry' IS NOT NULL THEN
                ST_GeomFromGeoJSON(value->>'geometry')
            WHEN value->>'bbox' IS NOT NULL THEN
                ST_MakeEnvelope(
                    (value->'bbox'->>0)::float,
                    (value->'bbox'->>1)::float,
                    (value->'bbox'->>2)::float,
                    (value->'bbox'->>3)::float,
                    4326
                )
            ELSE NULL
        END as geometry,
        properties_idx(value ->'properties') as properties,
        value->>'collection' as collection_id,
        (value->'properties'->>'datetime')::timestamptz as datetime
;
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE SET SEARCH_PATH TO pgstac,public;

/*
Takes a single feature, an array of features, or a feature collection
and returns a set up individual items rows
*/
CREATE OR REPLACE FUNCTION features_to_items(value jsonb) RETURNS SETOF item AS $$
    WITH features AS (
        SELECT
        jsonb_array_elements(
            CASE
                WHEN jsonb_typeof(value) = 'array' THEN value
                WHEN value->>'type' = 'Feature' THEN '[]'::jsonb || value
                WHEN value->>'type' = 'FeatureCollection' THEN value->'features'
                ELSE NULL
            END
        ) as value
    )
    SELECT feature_to_item(value) FROM features
    ;
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE SET SEARCH_PATH TO pgstac,public;


CREATE OR REPLACE FUNCTION get_item(_id text) RETURNS jsonb AS $$
SELECT content FROM items WHERE id=_id;
$$ LANGUAGE SQL SET SEARCH_PATH TO pgstac,public;

CREATE OR REPLACE FUNCTION delete_item(_id text) RETURNS VOID AS $$
    DELETE FROM items WHERE id = _id;
$$ LANGUAGE SQL SET SEARCH_PATH TO pgstac,public;

CREATE OR REPLACE FUNCTION create_item(data jsonb) RETURNS VOID AS $$
    DELETE FROM items WHERE id=data->>'id';
    INSERT INTO items (content) VALUES (data);
$$ LANGUAGE SQL SET SEARCH_PATH TO pgstac,public;

/* Trigger Function to cascade inserts/updates/deletes
from items table to items_search table */
CREATE OR REPLACE FUNCTION items_trigger_func()
RETURNS TRIGGER AS $$
DECLARE
BEGIN
    DELETE FROM items_search WHERE id = NEW.id;
    IF TG_OP = 'DELETE' THEN
        RAISE NOTICE 'DELETE TRIGGER';
        DELETE FROM items_search WHERE id = OLD.id;
        RETURN OLD;
    ELSIF TG_OP IN ('INSERT', 'UPDATE') AND pg_trigger_depth() = 1 THEN
        INSERT INTO items (content) VALUES (NEW.content)
        ON CONFLICT (id) DO UPDATE
            SET content=EXCLUDED.content;
        INSERT INTO items_search SELECT * FROM feature_to_item(NEW.content)
        ON CONFLICT DO NOTHING
        ;
        RETURN NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SET SEARCH_PATH TO pgstac,public;

CREATE TRIGGER items_trigger
BEFORE INSERT OR UPDATE OR DELETE ON items
FOR EACH ROW EXECUTE PROCEDURE items_trigger_func();

/* Trigger Function to cascade inserts/updates/deletes
from items table to items_search table */
CREATE OR REPLACE FUNCTION items_trigger_stmt_func()
RETURNS TRIGGER AS $$
DECLARE
BEGIN
    ANALYZE items_search;
    RETURN NULL;
END;
$$ LANGUAGE PLPGSQL SET SEARCH_PATH TO pgstac,public;

CREATE TRIGGER items_stmt_trigger
AFTER INSERT OR UPDATE OR DELETE ON items
FOR EACH STATEMENT EXECUTE PROCEDURE items_trigger_stmt_func();

/*
View to get a table of available items partitions
with date ranges
*/
DROP VIEW IF EXISTS items_search_partitions;
CREATE VIEW items_search_partitions AS
WITH base AS
(SELECT
    c.oid::pg_catalog.regclass::text as partition,
    pg_catalog.pg_get_expr(c.relpartbound, c.oid) as _constraint,
    regexp_matches(
        pg_catalog.pg_get_expr(c.relpartbound, c.oid),
        E'\\(''\([0-9 :+-]*\)''\\).*\\(''\([0-9 :+-]*\)''\\)'
    ) as t,
    reltuples::bigint as est_cnt
FROM pg_catalog.pg_class c, pg_catalog.pg_inherits i
WHERE c.oid = i.inhrelid AND i.inhparent = 'items_search'::regclass)
SELECT partition, tstzrange(
    t[1]::timestamptz,
    t[2]::timestamptz
), est_cnt
FROM base
WHERE est_cnt >0
ORDER BY 2 desc;

CREATE OR REPLACE FUNCTION collection_bbox(id text) RETURNS jsonb AS $$
SELECT (replace(replace(replace(st_extent(geometry)::text,'BOX(','[['),')',']]'),' ',','))::jsonb
FROM items_search WHERE collection_id=$1;
;
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE SET SEARCH_PATH TO pgstac, public;

CREATE OR REPLACE FUNCTION collection_temporal_extent(id text) RETURNS jsonb AS $$
SELECT to_jsonb(array[array[min(datetime)::text, max(datetime)::text]])
FROM items_search WHERE collection_id=$1;
;
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE SET SEARCH_PATH TO pgstac, public;

CREATE OR REPLACE FUNCTION update_collection_extents() RETURNS VOID AS $$
UPDATE collections SET
    content = content ||
    jsonb_build_object(
        'extent', jsonb_build_object(
            'spatial', jsonb_build_object(
                'bbox', collection_bbox(collections.id)
            ),
            'temporal', jsonb_build_object(
                'interval', collection_temporal_extent(collections.id)
            )
        )
    )
;
$$ LANGUAGE SQL SET SEARCH_PATH TO pgstac, public;
SET SEARCH_PATH TO pgstac, public;

/*
View to get a table of available items partitions
with date ranges
*/
DROP VIEW IF EXISTS items_search_partitions;
CREATE VIEW items_search_partitions AS
WITH base AS
(SELECT
    c.oid::pg_catalog.regclass::text as partition,
    pg_catalog.pg_get_expr(c.relpartbound, c.oid) as _constraint,
    regexp_matches(
        pg_catalog.pg_get_expr(c.relpartbound, c.oid),
        E'\\(''\([0-9 :+-]*\)''\\).*\\(''\([0-9 :+-]*\)''\\)'
    ) as t,
    reltuples::bigint as est_cnt
FROM pg_catalog.pg_class c, pg_catalog.pg_inherits i
WHERE c.oid = i.inhrelid AND i.inhparent = 'items_search'::regclass)
SELECT partition, tstzrange(
    t[1]::timestamptz,
    t[2]::timestamptz
), est_cnt
FROM base
WHERE est_cnt >0
ORDER BY 2 desc;


CREATE OR REPLACE FUNCTION items_by_partition(
    IN _where text DEFAULT 'TRUE',
    IN _dtrange tstzrange DEFAULT tstzrange('-infinity','infinity'),
    IN _orderby text DEFAULT 'datetime DESC, id DESC',
    IN _limit int DEFAULT 10
) RETURNS SETOF text AS $$
DECLARE
partition_query text;
main_query text;
batchcount int;
counter int := 0;
p record;
BEGIN
IF _orderby ILIKE 'datetime d%' THEN
    partition_query := format($q$
        SELECT * FROM (SELECT partition
        FROM items_search_partitions
        WHERE tstzrange && $1
        ORDER BY tstzrange DESC ) as p
        UNION ALL SELECT 'items_search_default';
    $q$);
ELSIF _orderby ILIKE 'datetime a%' THEN
    partition_query := format($q$
        SELECT partition FROM (SELECT partition
        FROM items_search_partitions
        WHERE tstzrange && $1
        ORDER BY tstzrange ASC
        ) as p UNION ALL SELECT 'items_search_default';
    $q$);
ELSE
    partition_query := format($q$
        SELECT 'items_search' as partition WHERE $1 IS NOT NULL;
    $q$);
END IF;
RAISE NOTICE 'Partition Query: %', partition_query;
FOR p IN
    EXECUTE partition_query USING (_dtrange)
LOOP
    IF lower(_dtrange)::timestamptz > '-infinity' THEN
        _where := concat(_where,format(' AND datetime >= %L',lower(_dtrange)::timestamptz::text));
    END IF;
    IF upper(_dtrange)::timestamptz < 'infinity' THEN
        _where := concat(_where,format(' AND datetime <= %L',upper(_dtrange)::timestamptz::text));
    END IF;

    main_query := format($q$
        SELECT id FROM %I
        WHERE %s
        ORDER BY %s
        LIMIT %s - $1
    $q$, p.partition::text, _where, _orderby, _limit
    );
    RAISE NOTICE 'Partition Query %', main_query;
    RAISE NOTICE '%', counter;
    RETURN QUERY EXECUTE main_query USING counter;

    GET DIAGNOSTICS batchcount = ROW_COUNT;
    counter := counter + batchcount;
    RAISE NOTICE 'FOUND %', batchcount;
    IF counter >= _limit THEN
        EXIT;
    END IF;
    RAISE NOTICE 'ADDED % FOR A TOTAL OF %', batchcount, counter;
END LOOP;
RETURN;
END;
$$ LANGUAGE PLPGSQL SET SEARCH_PATH TO pgstac,public;


CREATE OR REPLACE FUNCTION split_stac_path(IN path text, OUT col text, OUT dotpath text, OUT jspath text, OUT jspathtext text) AS $$
WITH col AS (
    SELECT
        CASE WHEN
            split_part(path, '.', 1) IN ('id', 'stac_version', 'stac_extensions','geometry','properties','assets','collection_id','datetime','links', 'extra_fields') THEN split_part(path, '.', 1)
        ELSE 'properties'
        END AS col
),
dp AS (
    SELECT
        col, ltrim(replace(path, col , ''),'.') as dotpath
    FROM col
),
paths AS (
SELECT
    col, dotpath,
    regexp_split_to_table(dotpath,E'\\.') as path FROM dp
) SELECT
    col,
    btrim(concat(col,'.',dotpath),'.'),
    CASE WHEN btrim(concat(col,'.',dotpath),'.') != col THEN concat(col,'->',string_agg(concat('''',path,''''),'->')) ELSE col END,
    regexp_replace(
        CASE WHEN btrim(concat(col,'.',dotpath),'.') != col THEN concat(col,'->',string_agg(concat('''',path,''''),'->')) ELSE col END,
        E'>([^>]*)$','>>\1'
    )
FROM paths group by col, dotpath;
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE;


/* Functions for searching items */
CREATE OR REPLACE FUNCTION sort_base(
    IN _sort jsonb DEFAULT '[{"field":"datetime","direction":"desc"}]',
    OUT key text,
    OUT col text,
    OUT dir text,
    OUT rdir text,
    OUT sort text,
    OUT rsort text
) RETURNS SETOF RECORD AS $$
WITH sorts AS (
    SELECT
        value->>'field' as key,
        (split_stac_path(value->>'field')).jspathtext as col,
        coalesce(upper(value->>'direction'),'ASC') as dir
    FROM jsonb_array_elements('[]'::jsonb || coalesce(_sort,'[{"field":"datetime","direction":"desc"}]') )
)
SELECT
    key,
    col,
    dir,
    CASE dir WHEN 'DESC' THEN 'ASC' ELSE 'ASC' END as rdir,
    concat(col, ' ', dir, ' NULLS LAST ') AS sort,
    concat(col,' ', CASE dir WHEN 'DESC' THEN 'ASC' ELSE 'ASC' END, ' NULLS LAST ') AS rsort
FROM sorts
UNION ALL
SELECT 'id', 'id', 'DESC', 'ASC', 'id DESC', 'id ASC'
;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION sort(_sort jsonb) RETURNS text AS $$
SELECT string_agg(sort,', ') FROM sort_base(_sort);
$$ LANGUAGE SQL PARALLEL SAFE SET SEARCH_PATH TO pgstac,public;


CREATE OR REPLACE FUNCTION rsort(_sort jsonb) RETURNS text AS $$
SELECT string_agg(rsort,', ') FROM sort_base(_sort);
$$ LANGUAGE SQL PARALLEL SAFE SET SEARCH_PATH TO pgstac,public;


CREATE OR REPLACE FUNCTION bbox_geom(_bbox jsonb) RETURNS box3d AS $$
SELECT CASE jsonb_array_length(_bbox)
    WHEN 4 THEN
        ST_SetSRID(ST_MakeEnvelope(
            (_bbox->>0)::float,
            (_bbox->>1)::float,
            (_bbox->>2)::float,
            (_bbox->>3)::float
        ),4326)
    WHEN 6 THEN
    ST_SetSRID(ST_3DMakeBox(
        ST_MakePoint(
            (_bbox->>0)::float,
            (_bbox->>1)::float,
            (_bbox->>2)::float
        ),
        ST_MakePoint(
            (_bbox->>3)::float,
            (_bbox->>4)::float,
            (_bbox->>5)::float
        )
    ),4326)
    ELSE null END;
;
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE;

CREATE OR REPLACE FUNCTION in_array_q(col text, arr jsonb) RETURNS text AS $$
SELECT CASE jsonb_typeof(arr) WHEN 'array' THEN format('%I = ANY(textarr(%L))', col, arr) ELSE format('%I = %L', col, arr) END;
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE;

CREATE OR REPLACE FUNCTION count_by_delim(text, text) RETURNS int AS $$
SELECT count(*) FROM regexp_split_to_table($1,$2);
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE;



CREATE OR REPLACE FUNCTION stac_query_op(att text, _op text, val jsonb) RETURNS text AS $$
DECLARE
ret text := '';
idx text;
idx_func text;
idx_typ text;
op text;
jp text;
att_parts RECORD;
BEGIN
val := lower(val::text)::jsonb;

att_parts := split_stac_path(att);

op := CASE _op
    WHEN 'eq' THEN '='
    WHEN 'ge' THEN '>='
    WHEN 'gt' THEN '>'
    WHEN 'le' THEN '<='
    WHEN 'lt' THEN '<'
    WHEN 'ne' THEN '!='
    ELSE _op
END;
RAISE NOTICE 'att_parts: % %', att_parts, count_by_delim(att_parts.dotpath,'\.');
IF
    op = '='
    AND att_parts.col = 'properties'
    AND count_by_delim(att_parts.dotpath,'\.') = 2
THEN
    -- use jsonpath query to leverage index for eqaulity tests on single level deep properties
    jp := btrim(format($jp$ $.%I[*] ? ( @ == %s ) $jp$, replace(att_parts.dotpath, 'properties.',''), val));
    raise notice 'jp: %', jp;
    ret := format($q$ properties @? %L $q$, jp);
ELSIF jsonb_typeof(val) = 'number' THEN
    ret := format('(%s)::numeric %s %s', att_parts.jspathtext, op, val);
ELSE
    ret := format('lower(%s) %s %L', att_parts.jspathtext, op, val);
END IF;
RAISE NOTICE 'Op Query: %', ret;

return ret;
END;
$$ LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION stac_query(_query jsonb) RETURNS TEXT[] AS $$
DECLARE
qa text[];
att text;
ops jsonb;
op text;
val jsonb;
BEGIN
FOR att, ops IN SELECT key, value FROM jsonb_each(_query)
LOOP
    FOR op, val IN SELECT key, value FROM jsonb_each(ops)
    LOOP
        qa := array_append(qa, stac_query_op(att,op, val));
        RAISE NOTICE '% % %', att, op, val;
    END LOOP;
END LOOP;
RETURN qa;
END;
$$ LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION filter_by_order(item_id text, _sort jsonb, _type text) RETURNS text AS $$
DECLARE
item item;
BEGIN
SELECT * INTO item FROM items_search WHERE id=item_id;
RETURN filter_by_order(item, _sort, _type);
END;
$$ LANGUAGE PLPGSQL SET SEARCH_PATH TO pgstac,public;

-- Used to create filters used for paging using the items id from the token
CREATE OR REPLACE FUNCTION filter_by_order(_item item, _sort jsonb, _type text) RETURNS text AS $$
DECLARE
sorts RECORD;
filts text[];
itemval text;
op text;
idop text;
ret text;
eq_flag text;
_item_j jsonb := to_jsonb(_item);
BEGIN
FOR sorts IN SELECT * FROM sort_base(_sort) LOOP
    IF sorts.col = 'datetime' THEN
        CONTINUE;
    END IF;
    IF sorts.col='id' AND _type IN ('prev','next') THEN
        eq_flag := '';
    ELSE
        eq_flag := '=';
    END IF;

    op := concat(
        CASE
            WHEN _type in ('prev','first') AND sorts.dir = 'ASC' THEN '<'
            WHEN _type in ('last','next') AND sorts.dir = 'ASC' THEN '>'
            WHEN _type in ('prev','first') AND sorts.dir = 'DESC' THEN '>'
            WHEN _type in ('last','next') AND sorts.dir = 'DESC' THEN '<'
        END,
        eq_flag
    );

    IF _item_j ? sorts.col THEN
        filts = array_append(filts, format('%s %s %L', sorts.col, op, _item_j->>sorts.col));
    END IF;
END LOOP;
ret := coalesce(array_to_string(filts,' AND '), 'TRUE');
RAISE NOTICE 'Order Filter %', ret;
RETURN ret;
END;
$$ LANGUAGE PLPGSQL SET SEARCH_PATH TO pgstac,public;

CREATE OR REPLACE FUNCTION search_dtrange(IN _indate jsonb, OUT _tstzrange tstzrange) AS
$$
WITH t AS (
    SELECT CASE
        WHEN jsonb_typeof(_indate) = 'array' THEN
            textarr(_indate)
        ELSE
            regexp_split_to_array(
                btrim(_indate::text,'"'),
                '/'
            )
        END AS arr
)
, t1 AS (
    SELECT
        CASE
            WHEN arr[1] = '..' THEN '-infinity'::timestamptz
            ELSE arr[1]::timestamptz
        END AS st,
        CASE
            WHEN array_upper(arr,1) = 1 THEN null
            WHEN arr[2] = '..' THEN 'infinity'::timestamptz
            ELSE arr[2]::timestamptz
        END AS et
    FROM t
)
SELECT
    CASE
        WHEN et IS NULL
            THEN tstzrange(st, st, '()')
        ELSE
            tstzrange(st, et)
    END AS _tstzrange
FROM t1;
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE;


CREATE OR REPLACE FUNCTION search(_search jsonb = '{}'::jsonb) RETURNS SETOF jsonb AS $$
DECLARE
qstart timestamptz := clock_timestamp();
_sort text := '';
_rsort text := '';
_limit int := 10;
_geom geometry;
qa text[];
pq text[];
query text;
pq_prop record;
pq_op record;
prev_id text := NULL;
next_id text := NULL;
whereq text := 'TRUE';
links jsonb := '[]'::jsonb;
token text;
tok_val text;
tok_q text := 'TRUE';
tok_sort text;
first_id text;
first_dt timestamptz;
last_id text;
sort text;
rsort text;
dt text[];
dqa text[];
dq text;
mq_where text;
startdt timestamptz;
enddt timestamptz;
item items_search%ROWTYPE;
counter int := 0;
batchcount int;
month timestamptz;
m record;
_dtrange tstzrange := tstzrange('-infinity','infinity');
_dtsort text;
_token_dtrange tstzrange := tstzrange('-infinity','infinity');
_token_record items_search%ROWTYPE;
is_prev boolean := false;
BEGIN
-- Create table from sort query of items to sort
CREATE TEMP TABLE pgstac_tmp_sorts ON COMMIT DROP AS SELECT * FROM sort_base(_search->'sortby');

-- Get the datetime sort direction, necessary for efficient cycling through partitions
SELECT INTO _dtsort dir FROM pgstac_tmp_sorts WHERE key='datetime';
RAISE NOTICE '_dtsort: %',_dtsort;

SELECT INTO _sort string_agg(s.sort,', ') FROM pgstac_tmp_sorts s;
SELECT INTO _rsort string_agg(s.rsort,', ') FROM pgstac_tmp_sorts s;
tok_sort := _sort;


-- Get datetime from query as a tstzrange
IF _search ? 'datetime' THEN
    _dtrange := search_dtrange(_search->'datetime');
    _token_dtrange := _dtrange;
END IF;

-- Get the paging token
IF _search ? 'token' THEN
    token := _search->>'token';
    tok_val := substr(token,6);
    IF starts_with(token, 'prev:') THEN
        is_prev := true;
    END IF;
    SELECT INTO _token_record * FROM items_search WHERE id=tok_val;
    IF
        (is_prev AND _dtsort = 'DESC')
        OR
        (not is_prev AND _dtsort = 'ASC')
    THEN
        _token_dtrange := tstzrange(_token_record.datetime, 'infinity');
    ELSIF
        _dtsort IS NOT NULL
    THEN
        _token_dtrange := tstzrange('-infinity',_token_record.datetime);
    END IF;
    IF is_prev THEN
        tok_q := filter_by_order(tok_val,  _search->'sortby', 'first');
        _sort := _rsort;
    ELSIF starts_with(token, 'next:') THEN
       tok_q := filter_by_order(tok_val,  _search->'sortby', 'last');
    END IF;
END IF;
RAISE NOTICE 'timing: %', age(clock_timestamp(), qstart);
RAISE NOTICE 'tok_q: % _token_dtrange: %', tok_q, _token_dtrange;

IF _search ? 'ids' THEN
    RAISE NOTICE 'searching solely based on ids... %',_search;
    qa := array_append(qa, in_array_q('id', _search->'ids'));
ELSE
    IF _search ? 'intersects' THEN
        _geom := ST_SetSRID(ST_GeomFromGeoJSON(_search->>'intersects'), 4326);
    ELSIF _search ? 'bbox' THEN
        _geom := bbox_geom(_search->'bbox');
    END IF;

    IF _geom IS NOT NULL THEN
        qa := array_append(qa, format('st_intersects(geometry, %L::geometry)',_geom));
    END IF;

    IF _search ? 'collections' THEN
        qa := array_append(qa, in_array_q('collection_id', _search->'collections'));
    END IF;

    IF _search ? 'query' THEN
        qa := array_cat(qa,
            stac_query(_search->'query')
        );
    END IF;
END IF;

IF _search ? 'limit' THEN
    _limit := (_search->>'limit')::int;
END IF;


whereq := COALESCE(array_to_string(qa,' AND '),' TRUE ');
dq := COALESCE(array_to_string(dqa,' AND '),' TRUE ');
RAISE NOTICE 'timing before temp table: %', age(clock_timestamp(), qstart);

CREATE TEMP TABLE results_page ON COMMIT DROP AS
SELECT items_by_partition(
    concat(whereq, ' AND ', tok_q),
    _token_dtrange,
    _sort,
    _limit + 1
) as id;
RAISE NOTICE 'timing after temp table: %', age(clock_timestamp(), qstart);

RAISE NOTICE 'timing before min/max: %', age(clock_timestamp(), qstart);

IF is_prev THEN
    SELECT INTO last_id, first_id
        first_value(id) OVER (),
        last_value(id) OVER ()
    FROM results_page;
ELSE
    SELECT INTO first_id, last_id
        first_value(id) OVER (),
        last_value(id) OVER ()
    FROM results_page;
END IF;
RAISE NOTICE 'firstid: %, lastid %', first_id, last_id;
RAISE NOTICE 'timing after min/max: %', age(clock_timestamp(), qstart);





next_id := last_id;
RAISE NOTICE 'next_id: %', next_id;

IF tok_q = 'TRUE' THEN
    RAISE NOTICE 'Not a paging query, no previous item';
ELSE
    RAISE NOTICE 'Getting previous item id';
    RAISE NOTICE 'timing: %', age(clock_timestamp(), qstart);
    SELECT INTO _token_record * FROM items_search WHERE id=first_id;
    IF
        _dtsort = 'DESC'
    THEN
        _token_dtrange := _dtrange * tstzrange(_token_record.datetime, 'infinity');
    ELSE
        _token_dtrange := _dtrange * tstzrange('-infinity',_token_record.datetime);
    END IF;
    RAISE NOTICE '% %', _token_dtrange, _dtrange;
    SELECT INTO prev_id items_by_partition(
        concat(whereq, ' AND ', filter_by_order(first_id, _search->'sortby', 'prev')),
        _token_dtrange,
        _rsort,
        1
    ) as id;
    RAISE NOTICE 'timing: %', age(clock_timestamp(), qstart);

    RAISE NOTICE 'prev_id: %', prev_id;
END IF;


RETURN QUERY
WITH features AS (
    SELECT jsonb_agg(content) features
    FROM items WHERE id IN (SELECT id FROM results_page LIMIT _limit)
)
SELECT jsonb_build_object(
    'type', 'FeatureCollection',
    'features', coalesce(features,'[]'::jsonb),
    'links', links,
    'timeStamp', now(),
    'next', next_id,
    'prev', prev_id
)
FROM features
;


END;
$$ LANGUAGE PLPGSQL SET SEARCH_PATH TO pgstac,public;
