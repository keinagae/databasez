"""
All the unique changes for the databases package
with the custom Numeric as the deprecated pypostgresql
for backwards compatibility and to make sure the
package can go to SQLAlchemy 2.0+.
"""

import typing

from sqlalchemy import types, util
from sqlalchemy.dialects.postgresql.base import PGExecutionContext,PGDialect
from sqlalchemy.engine import processors
from sqlalchemy.types import Float, Numeric
from sqlalchemy_cockroachdb.base import CockroachDBDialect
from sqlalchemy_cockroachdb.ddl_compiler import CockroachDDLCompiler
from sqlalchemy_cockroachdb.stmt_compiler import CockroachIdentifierPreparer,CockroachCompiler
class PGExecutionContext_psycopg(PGExecutionContext):
    ...


class PGNumeric(Numeric):
    def bind_processor(self, dialect: typing.Any) -> typing.Union[str, None]:  # pragma: no cover
        return processors.to_str

    def result_processor(
        self, dialect: typing.Any, coltype: typing.Any
    ) -> typing.Union[float, None]:  # pragma: no cover
        if self.asdecimal:
            return None
        else:
            return processors.to_float


class CockroachDBDialect_psycopg(CockroachDBDialect):
    ...
    colspecs = util.update_copy(
        CockroachDBDialect.colspecs,
        {
            types.Numeric: PGNumeric,
            types.Float: Float,
        },
    )
    preparer = CockroachIdentifierPreparer
    statement_compiler = CockroachCompiler
    ddl_compiler = CockroachDDLCompiler
    # execution_ctx_cls = PGExecutionContext_psycopg



dialect = CockroachDBDialect_psycopg
