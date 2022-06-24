# Copyright (C) 2016-present the asyncpg authors and contributors
# <see AUTHORS file>
#
# This module is part of asyncpg and is released under
# the Apache 2.0 License: http://www.apache.org/licenses/LICENSE-2.0


INTRO_LOOKUP_TYPES_CRDB = """\
SELECT
    t.oid                           AS oid,
    ns.nspname                      AS ns,
    t.typname                       AS name,
    t.typtype                       AS kind,
    NULL                            AS basetype,
    t.typelem                       AS elemtype,
    NULL                            AS elemdelim,
    NULL                            AS range_subtype,
    NULL                            AS attrtypoids,
    NULL                            AS attrnames,
    NULL                            AS basetype_name,
    '-'                             AS elemtype_name,
    NULL                            AS range_subtype_name
FROM
    pg_catalog.pg_type AS t
    JOIN pg_catalog.pg_namespace ns
        ON (ns.oid = t.typnamespace)
WHERE
        t.oid = any($1::oid[])
"""


TYPE_BY_NAME = """\
SELECT
    t.oid,
    t.typelem     AS elemtype,
    t.typtype     AS kind
FROM
    pg_catalog.pg_type AS t
    INNER JOIN pg_catalog.pg_namespace ns ON (ns.oid = t.typnamespace)
WHERE
    t.typname = $1 AND ns.nspname = $2
"""


TYPE_BY_OID = """\
SELECT
    t.oid,
    t.typelem     AS elemtype,
    t.typtype     AS kind
FROM
    pg_catalog.pg_type AS t
WHERE
    t.oid = $1
"""


# 'b' for a base type, 'd' for a domain, 'e' for enum.
SCALAR_TYPE_KINDS = (b"b", b"d", b"e")


def is_scalar_type(typeinfo) -> bool:
    return typeinfo["kind"] in SCALAR_TYPE_KINDS and not typeinfo["elemtype"]


def is_domain_type(typeinfo) -> bool:
    return typeinfo["kind"] == b"d"
