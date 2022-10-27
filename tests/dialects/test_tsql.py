from tests.dialects.test_dialect import Validator


class TestTSQL(Validator):
    dialect = "tsql"

    def test_tsql(self):
        self.validate_identity('SELECT "x"."y" FROM foo')
        self.validate_identity(
            "SELECT DISTINCT DepartmentName, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY BaseRate) OVER (PARTITION BY DepartmentName) AS MedianCont FROM dbo.DimEmployee"
        )

        self.validate_all(
            "SELECT CAST([a].[b] AS SMALLINT) FROM foo",
            write={
                "tsql": 'SELECT CAST("a"."b" AS SMALLINT) FROM foo',
                "spark": "SELECT CAST(`a`.`b` AS SHORT) FROM foo",
            },
        )

        self.validate_all(
            "CONVERT(INT, CONVERT(NUMERIC, '444.75'))",
            write={
                "mysql": "CAST(CAST('444.75' AS DECIMAL) AS INT)",
                "tsql": "CAST(CAST('444.75' AS NUMERIC) AS INTEGER)",
            },
        )

    def test_types(self):
        self.validate_identity("CAST(x AS XML)")
        self.validate_identity("CAST(x AS UNIQUEIDENTIFIER)")
        self.validate_identity("CAST(x AS MONEY)")
        self.validate_identity("CAST(x AS SMALLMONEY)")
        self.validate_identity("CAST(x AS ROWVERSION)")
        self.validate_identity("CAST(x AS IMAGE)")
        self.validate_identity("CAST(x AS SQL_VARIANT)")
        self.validate_identity("CAST(x AS BIT)")
        self.validate_all(
            "CAST(x AS DATETIME2)",
            read={
                "": "CAST(x AS DATETIME)",
            },
            write={
                "mysql": "CAST(x AS DATETIME)",
                "tsql": "CAST(x AS DATETIME2)",
            },
        )

    def test_charindex(self):
        self.validate_all(
            "CHARINDEX(x, y, 9)",
            write={
                "spark": "LOCATE(x, y, 9)",
            },
        )
        self.validate_all(
            "CHARINDEX(x, y)",
            write={
                "spark": "LOCATE(x, y)",
            },
        )
        self.validate_all(
            "CHARINDEX('sub', 'testsubstring', 3)",
            write={
                "spark": "LOCATE('sub', 'testsubstring', 3)",
            },
        )
        self.validate_all(
            "CHARINDEX('sub', 'testsubstring')",
            write={
                "spark": "LOCATE('sub', 'testsubstring')",
            },
        )

    def test_len(self):
        self.validate_all("LEN(x)", write={"spark": "LENGTH(x)"})

    def test_replicate(self):
        self.validate_all("REPLICATE('x', 2)", write={"spark": "REPEAT('x', 2)"})

    def test_isnull(self):
        self.validate_all("ISNULL(x, y)", write={"spark": "COALESCE(x, y)"})

    def test_jsonvalue(self):
        self.validate_all(
            "JSON_VALUE(r.JSON, '$.Attr_INT')",
            write={"spark": "GET_JSON_OBJECT(r.JSON, '$.Attr_INT')"},
        )

    def test_datefromparts(self):
        self.validate_all(
            "SELECT DATEFROMPARTS('2020', 10, 01)",
            write={"spark": "SELECT MAKE_DATE('2020', 10, 01)"},
        )

    def test_datename(self):
        self.validate_all(
            "SELECT DATENAME(mm,'01-01-1970')",
            write={"spark": "SELECT DATE_FORMAT('01-01-1970', 'MMMM')"},
        )
        self.validate_all(
            "SELECT DATENAME(dw,'01-01-1970')",
            write={"spark": "SELECT DATE_FORMAT('01-01-1970', 'EEEE')"},
        )

    def test_datepart(self):
        self.validate_all(
            "SELECT DATEPART(month,'01-01-1970')",
            write={"spark": "SELECT DATE_FORMAT('01-01-1970', 'MM')"},
        )

    def test_convert_date_format(self):
        self.validate_all(
            "CONVERT(NVARCHAR(200), x)",
            write={
                "spark": "CAST(x AS VARCHAR(200))",
            },
        )
        self.validate_all(
            "CONVERT(NVARCHAR, x)",
            write={
                "spark": "CAST(x AS VARCHAR(30))",
            },
        )
        self.validate_all(
            "CONVERT(NVARCHAR(MAX), x)",
            write={
                "spark": "CAST(x AS STRING)",
            },
        )
        self.validate_all(
            "CONVERT(VARCHAR(200), x)",
            write={
                "spark": "CAST(x AS VARCHAR(200))",
            },
        )
        self.validate_all(
            "CONVERT(VARCHAR, x)",
            write={
                "spark": "CAST(x AS VARCHAR(30))",
            },
        )
        self.validate_all(
            "CONVERT(VARCHAR(MAX), x)",
            write={
                "spark": "CAST(x AS STRING)",
            },
        )
        self.validate_all(
            "CONVERT(CHAR(40), x)",
            write={
                "spark": "CAST(x AS CHAR(40))",
            },
        )
        self.validate_all(
            "CONVERT(CHAR, x)",
            write={
                "spark": "CAST(x AS CHAR(30))",
            },
        )
        self.validate_all(
            "CONVERT(NCHAR(40), x)",
            write={
                "spark": "CAST(x AS CHAR(40))",
            },
        )
        self.validate_all(
            "CONVERT(NCHAR, x)",
            write={
                "spark": "CAST(x AS CHAR(30))",
            },
        )
        self.validate_all(
            "CONVERT(VARCHAR, x, 121)",
            write={
                "spark": "CAST(DATE_FORMAT(x, 'yyyy-MM-dd HH:mm:ss.SSSSSS') AS VARCHAR(30))",
            },
        )
        self.validate_all(
            "CONVERT(VARCHAR(40), x, 121)",
            write={
                "spark": "CAST(DATE_FORMAT(x, 'yyyy-MM-dd HH:mm:ss.SSSSSS') AS VARCHAR(40))",
            },
        )
        self.validate_all(
            "CONVERT(VARCHAR(MAX), x, 121)",
            write={
                "spark": "DATE_FORMAT(x, 'yyyy-MM-dd HH:mm:ss.SSSSSS')",
            },
        )
        self.validate_all(
            "CONVERT(NVARCHAR, x, 121)",
            write={
                "spark": "CAST(DATE_FORMAT(x, 'yyyy-MM-dd HH:mm:ss.SSSSSS') AS VARCHAR(30))",
            },
        )
        self.validate_all(
            "CONVERT(NVARCHAR(40), x, 121)",
            write={
                "spark": "CAST(DATE_FORMAT(x, 'yyyy-MM-dd HH:mm:ss.SSSSSS') AS VARCHAR(40))",
            },
        )
        self.validate_all(
            "CONVERT(NVARCHAR(MAX), x, 121)",
            write={
                "spark": "DATE_FORMAT(x, 'yyyy-MM-dd HH:mm:ss.SSSSSS')",
            },
        )
        self.validate_all(
            "CONVERT(DATE, x, 121)",
            write={
                "spark": "TO_DATE(x, 'yyyy-MM-dd HH:mm:ss.SSSSSS')",
            },
        )
        self.validate_all(
            "CONVERT(DATETIME, x, 121)",
            write={
                "spark": "TO_TIMESTAMP(x, 'yyyy-MM-dd HH:mm:ss.SSSSSS')",
            },
        )
        self.validate_all(
            "CONVERT(DATETIME2, x, 121)",
            write={
                "spark": "TO_TIMESTAMP(x, 'yyyy-MM-dd HH:mm:ss.SSSSSS')",
            },
        )
        self.validate_all(
            "CONVERT(INT, x)",
            write={
                "spark": "CAST(x AS INT)",
            },
        )
        self.validate_all(
            "CONVERT(INT, x, 121)",
            write={
                "spark": "CAST(x AS INT)",
            },
        )
        self.validate_all(
            "TRY_CONVERT(NVARCHAR, x, 121)",
            write={
                "spark": "CAST(DATE_FORMAT(x, 'yyyy-MM-dd HH:mm:ss.SSSSSS') AS VARCHAR(30))",
            },
        )
        self.validate_all(
            "TRY_CONVERT(INT, x)",
            write={
                "spark": "CAST(x AS INT)",
            },
        )
        self.validate_all(
            "TRY_CAST(x AS INT)",
            write={
                "spark": "CAST(x AS INT)",
            },
        )
        self.validate_all(
            "CAST(x AS INT)",
            write={
                "spark": "CAST(x AS INT)",
            },
        )
        self.validate_all(
            "SELECT CONVERT(VARCHAR(10), testdb.dbo.test.x, 120) y FROM testdb.dbo.test",
            write={
                "mysql": "SELECT CAST(TIME_TO_STR(testdb.dbo.test.x, '%Y-%m-%d %H:%M:%S') AS VARCHAR(10)) AS y FROM testdb.dbo.test",
                "spark": "SELECT CAST(DATE_FORMAT(testdb.dbo.test.x, 'yyyy-MM-dd HH:mm:ss') AS VARCHAR(10)) AS y FROM testdb.dbo.test",
            },
        )
        self.validate_all(
            "SELECT CONVERT(VARCHAR(10), y.x) z FROM testdb.dbo.test y",
            write={
                "mysql": "SELECT CAST(y.x AS VARCHAR(10)) AS z FROM testdb.dbo.test AS y",
                "spark": "SELECT CAST(y.x AS VARCHAR(10)) AS z FROM testdb.dbo.test AS y",
            },
        )

    def test_add_date(self):
        self.validate_identity("SELECT DATEADD(year, 1, '2017/08/25')")
        self.validate_all(
            "SELECT DATEADD(year, 1, '2017/08/25')", write={"spark": "SELECT ADD_MONTHS('2017/08/25', 12)"}
        )
        self.validate_all("SELECT DATEADD(qq, 1, '2017/08/25')", write={"spark": "SELECT ADD_MONTHS('2017/08/25', 3)"})
        self.validate_all(
            "SELECT DATEADD(wk, 1, '2017/08/25')",
            write={"spark": "SELECT DATE_ADD('2017/08/25', 7)", "databricks": "SELECT DATEADD(week, 1, '2017/08/25')"},
        )

    def test_date_diff(self):
        self.validate_identity("SELECT DATEDIFF(year, '2020/01/01', '2021/01/01')")
        self.validate_all(
            "SELECT DATEDIFF(year, '2020/01/01', '2021/01/01')",
            write={
                "tsql": "SELECT DATEDIFF(year, '2020/01/01', '2021/01/01')",
                "spark": "SELECT MONTHS_BETWEEN('2021/01/01', '2020/01/01') / 12",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(mm, 'start','end')",
            write={
                "spark": "SELECT MONTHS_BETWEEN('end', 'start')",
                "tsql": "SELECT DATEDIFF(month, 'start', 'end')",
                "databricks": "SELECT DATEDIFF(month, 'start', 'end')",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(quarter, 'start', 'end')",
            write={
                "spark": "SELECT MONTHS_BETWEEN('end', 'start') / 3",
                "databricks": "SELECT DATEDIFF(quarter, 'start', 'end')",
            },
        )

    def test_iif(self):
        self.validate_identity("SELECT IIF(cond, 'True', 'False')")
        self.validate_all(
            "SELECT IIF(cond, 'True', 'False');",
            write={
                "spark": "SELECT IF(cond, 'True', 'False')",
            },
        )

    def test_lateral_subquery(self):
        self.validate_all(
            "SELECT x.a, x.b, t.v, t.y FROM x CROSS APPLY (SELECT v, y FROM t) t(v, y)",
            write={
                "spark": "SELECT x.a, x.b, t.v, t.y FROM x JOIN LATERAL (SELECT v, y FROM t) AS t(v, y)",
            },
        )
        self.validate_all(
            "SELECT x.a, x.b, t.v, t.y FROM x OUTER APPLY (SELECT v, y FROM t) t(v, y)",
            write={
                "spark": "SELECT x.a, x.b, t.v, t.y FROM x LEFT JOIN LATERAL (SELECT v, y FROM t) AS t(v, y)",
            },
        )

    def test_lateral_table_valued_function(self):
        self.validate_all(
            "SELECT t.x, y.z FROM x CROSS APPLY tvfTest(t.x)y(z)",
            write={
                "spark": "SELECT t.x, y.z FROM x JOIN LATERAL TVFTEST(t.x) y AS z",
            },
        )
        self.validate_all(
            "SELECT t.x, y.z FROM x OUTER APPLY tvfTest(t.x)y(z)",
            write={
                "spark": "SELECT t.x, y.z FROM x LEFT JOIN LATERAL TVFTEST(t.x) y AS z",
            },
        )

    def test_top(self):
        self.validate_all(
            "SELECT TOP 3 * FROM A",
            write={
                "spark": "SELECT * FROM A LIMIT 3",
            },
        )
        self.validate_all(
            "SELECT TOP (3) * FROM A",
            write={
                "spark": "SELECT * FROM A LIMIT 3",
            },
        )
