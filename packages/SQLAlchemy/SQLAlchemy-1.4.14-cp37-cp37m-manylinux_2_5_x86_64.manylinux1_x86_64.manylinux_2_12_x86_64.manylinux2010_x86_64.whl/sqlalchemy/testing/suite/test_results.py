import datetime

from .. import engines
from .. import fixtures
from ..assertions import eq_
from ..config import requirements
from ..schema import Column
from ..schema import Table
from ... import DateTime
from ... import func
from ... import Integer
from ... import select
from ... import sql
from ... import String
from ... import testing
from ... import text
from ... import util


class RowFetchTest(fixtures.TablesTest):
    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "plain_pk",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("data", String(50)),
        )
        Table(
            "has_dates",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("today", DateTime),
        )

    @classmethod
    def insert_data(cls, connection):
        connection.execute(
            cls.tables.plain_pk.insert(),
            [
                {"id": 1, "data": "d1"},
                {"id": 2, "data": "d2"},
                {"id": 3, "data": "d3"},
            ],
        )

        connection.execute(
            cls.tables.has_dates.insert(),
            [{"id": 1, "today": datetime.datetime(2006, 5, 12, 12, 0, 0)}],
        )

    def test_via_attr(self, connection):
        row = connection.execute(
            self.tables.plain_pk.select().order_by(self.tables.plain_pk.c.id)
        ).first()

        eq_(row.id, 1)
        eq_(row.data, "d1")

    def test_via_string(self, connection):
        row = connection.execute(
            self.tables.plain_pk.select().order_by(self.tables.plain_pk.c.id)
        ).first()

        eq_(row._mapping["id"], 1)
        eq_(row._mapping["data"], "d1")

    def test_via_int(self, connection):
        row = connection.execute(
            self.tables.plain_pk.select().order_by(self.tables.plain_pk.c.id)
        ).first()

        eq_(row[0], 1)
        eq_(row[1], "d1")

    def test_via_col_object(self, connection):
        row = connection.execute(
            self.tables.plain_pk.select().order_by(self.tables.plain_pk.c.id)
        ).first()

        eq_(row._mapping[self.tables.plain_pk.c.id], 1)
        eq_(row._mapping[self.tables.plain_pk.c.data], "d1")

    @requirements.duplicate_names_in_cursor_description
    def test_row_with_dupe_names(self, connection):
        result = connection.execute(
            select(
                self.tables.plain_pk.c.data,
                self.tables.plain_pk.c.data.label("data"),
            ).order_by(self.tables.plain_pk.c.id)
        )
        row = result.first()
        eq_(result.keys(), ["data", "data"])
        eq_(row, ("d1", "d1"))

    def test_row_w_scalar_select(self, connection):
        """test that a scalar select as a column is returned as such
        and that type conversion works OK.

        (this is half a SQLAlchemy Core test and half to catch database
        backends that may have unusual behavior with scalar selects.)

        """
        datetable = self.tables.has_dates
        s = select(datetable.alias("x").c.today).scalar_subquery()
        s2 = select(datetable.c.id, s.label("somelabel"))
        row = connection.execute(s2).first()

        eq_(row.somelabel, datetime.datetime(2006, 5, 12, 12, 0, 0))


class PercentSchemaNamesTest(fixtures.TablesTest):
    """tests using percent signs, spaces in table and column names.

    This didn't work for PostgreSQL / MySQL drivers for a long time
    but is now supported.

    """

    __requires__ = ("percent_schema_names",)

    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        cls.tables.percent_table = Table(
            "percent%table",
            metadata,
            Column("percent%", Integer),
            Column("spaces % more spaces", Integer),
        )
        cls.tables.lightweight_percent_table = sql.table(
            "percent%table",
            sql.column("percent%"),
            sql.column("spaces % more spaces"),
        )

    def test_single_roundtrip(self, connection):
        percent_table = self.tables.percent_table
        for params in [
            {"percent%": 5, "spaces % more spaces": 12},
            {"percent%": 7, "spaces % more spaces": 11},
            {"percent%": 9, "spaces % more spaces": 10},
            {"percent%": 11, "spaces % more spaces": 9},
        ]:
            connection.execute(percent_table.insert(), params)
        self._assert_table(connection)

    def test_executemany_roundtrip(self, connection):
        percent_table = self.tables.percent_table
        connection.execute(
            percent_table.insert(), {"percent%": 5, "spaces % more spaces": 12}
        )
        connection.execute(
            percent_table.insert(),
            [
                {"percent%": 7, "spaces % more spaces": 11},
                {"percent%": 9, "spaces % more spaces": 10},
                {"percent%": 11, "spaces % more spaces": 9},
            ],
        )
        self._assert_table(connection)

    def _assert_table(self, conn):
        percent_table = self.tables.percent_table
        lightweight_percent_table = self.tables.lightweight_percent_table

        for table in (
            percent_table,
            percent_table.alias(),
            lightweight_percent_table,
            lightweight_percent_table.alias(),
        ):
            eq_(
                list(
                    conn.execute(table.select().order_by(table.c["percent%"]))
                ),
                [(5, 12), (7, 11), (9, 10), (11, 9)],
            )

            eq_(
                list(
                    conn.execute(
                        table.select()
                        .where(table.c["spaces % more spaces"].in_([9, 10]))
                        .order_by(table.c["percent%"])
                    )
                ),
                [(9, 10), (11, 9)],
            )

            row = conn.execute(
                table.select().order_by(table.c["percent%"])
            ).first()
            eq_(row._mapping["percent%"], 5)
            eq_(row._mapping["spaces % more spaces"], 12)

            eq_(row._mapping[table.c["percent%"]], 5)
            eq_(row._mapping[table.c["spaces % more spaces"]], 12)

        conn.execute(
            percent_table.update().values(
                {percent_table.c["spaces % more spaces"]: 15}
            )
        )

        eq_(
            list(
                conn.execute(
                    percent_table.select().order_by(
                        percent_table.c["percent%"]
                    )
                )
            ),
            [(5, 15), (7, 15), (9, 15), (11, 15)],
        )


class ServerSideCursorsTest(
    fixtures.TestBase, testing.AssertsExecutionResults
):

    __requires__ = ("server_side_cursors",)

    __backend__ = True

    def _is_server_side(self, cursor):
        # TODO: this is a huge issue as it prevents these tests from being
        # usable by third party dialects.
        if self.engine.dialect.driver == "psycopg2":
            return bool(cursor.name)
        elif self.engine.dialect.driver == "pymysql":
            sscursor = __import__("pymysql.cursors").cursors.SSCursor
            return isinstance(cursor, sscursor)
        elif self.engine.dialect.driver == "aiomysql":
            return cursor.server_side
        elif self.engine.dialect.driver == "mysqldb":
            sscursor = __import__("MySQLdb.cursors").cursors.SSCursor
            return isinstance(cursor, sscursor)
        elif self.engine.dialect.driver == "mariadbconnector":
            return not cursor.buffered
        elif self.engine.dialect.driver in ("asyncpg", "aiosqlite"):
            return cursor.server_side
        elif self.engine.dialect.driver == "pg8000":
            return getattr(cursor, "server_side", False)
        else:
            return False

    def _fixture(self, server_side_cursors):
        if server_side_cursors:
            with testing.expect_deprecated(
                "The create_engine.server_side_cursors parameter is "
                "deprecated and will be removed in a future release.  "
                "Please use the Connection.execution_options.stream_results "
                "parameter."
            ):
                self.engine = engines.testing_engine(
                    options={"server_side_cursors": server_side_cursors}
                )
        else:
            self.engine = engines.testing_engine(
                options={"server_side_cursors": server_side_cursors}
            )
        return self.engine

    @testing.combinations(
        ("global_string", True, "select 1", True),
        ("global_text", True, text("select 1"), True),
        ("global_expr", True, select(1), True),
        ("global_off_explicit", False, text("select 1"), False),
        (
            "stmt_option",
            False,
            select(1).execution_options(stream_results=True),
            True,
        ),
        (
            "stmt_option_disabled",
            True,
            select(1).execution_options(stream_results=False),
            False,
        ),
        ("for_update_expr", True, select(1).with_for_update(), True),
        # TODO: need a real requirement for this, or dont use this test
        (
            "for_update_string",
            True,
            "SELECT 1 FOR UPDATE",
            True,
            testing.skip_if("sqlite"),
        ),
        ("text_no_ss", False, text("select 42"), False),
        (
            "text_ss_option",
            False,
            text("select 42").execution_options(stream_results=True),
            True,
        ),
        id_="iaaa",
        argnames="engine_ss_arg, statement, cursor_ss_status",
    )
    def test_ss_cursor_status(
        self, engine_ss_arg, statement, cursor_ss_status
    ):
        engine = self._fixture(engine_ss_arg)
        with engine.begin() as conn:
            if isinstance(statement, util.string_types):
                result = conn.exec_driver_sql(statement)
            else:
                result = conn.execute(statement)
            eq_(self._is_server_side(result.cursor), cursor_ss_status)
            result.close()

    def test_conn_option(self):
        engine = self._fixture(False)

        with engine.connect() as conn:
            # should be enabled for this one
            result = conn.execution_options(
                stream_results=True
            ).exec_driver_sql("select 1")
            assert self._is_server_side(result.cursor)

    def test_stmt_enabled_conn_option_disabled(self):
        engine = self._fixture(False)

        s = select(1).execution_options(stream_results=True)

        with engine.connect() as conn:
            # not this one
            result = conn.execution_options(stream_results=False).execute(s)
            assert not self._is_server_side(result.cursor)

    def test_aliases_and_ss(self):
        engine = self._fixture(False)
        s1 = (
            select(sql.literal_column("1").label("x"))
            .execution_options(stream_results=True)
            .subquery()
        )

        # options don't propagate out when subquery is used as a FROM clause
        with engine.begin() as conn:
            result = conn.execute(s1.select())
            assert not self._is_server_side(result.cursor)
            result.close()

        s2 = select(1).select_from(s1)
        with engine.begin() as conn:
            result = conn.execute(s2)
            assert not self._is_server_side(result.cursor)
            result.close()

    def test_roundtrip_fetchall(self, metadata):
        md = self.metadata

        engine = self._fixture(True)
        test_table = Table(
            "test_table",
            md,
            Column("id", Integer, primary_key=True),
            Column("data", String(50)),
        )

        with engine.begin() as connection:
            test_table.create(connection, checkfirst=True)
            connection.execute(test_table.insert(), dict(data="data1"))
            connection.execute(test_table.insert(), dict(data="data2"))
            eq_(
                connection.execute(
                    test_table.select().order_by(test_table.c.id)
                ).fetchall(),
                [(1, "data1"), (2, "data2")],
            )
            connection.execute(
                test_table.update()
                .where(test_table.c.id == 2)
                .values(data=test_table.c.data + " updated")
            )
            eq_(
                connection.execute(
                    test_table.select().order_by(test_table.c.id)
                ).fetchall(),
                [(1, "data1"), (2, "data2 updated")],
            )
            connection.execute(test_table.delete())
            eq_(
                connection.scalar(
                    select(func.count("*")).select_from(test_table)
                ),
                0,
            )

    def test_roundtrip_fetchmany(self, metadata):
        md = self.metadata

        engine = self._fixture(True)
        test_table = Table(
            "test_table",
            md,
            Column("id", Integer, primary_key=True),
            Column("data", String(50)),
        )

        with engine.begin() as connection:
            test_table.create(connection, checkfirst=True)
            connection.execute(
                test_table.insert(),
                [dict(data="data%d" % i) for i in range(1, 20)],
            )

            result = connection.execute(
                test_table.select().order_by(test_table.c.id)
            )

            eq_(
                result.fetchmany(5),
                [(i, "data%d" % i) for i in range(1, 6)],
            )
            eq_(
                result.fetchmany(10),
                [(i, "data%d" % i) for i in range(6, 16)],
            )
            eq_(result.fetchall(), [(i, "data%d" % i) for i in range(16, 20)])
