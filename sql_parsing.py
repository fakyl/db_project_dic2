from pyparsing import (
    Word,
    delimitedList,
    Optional,
    Literal,
    Group,
    Combine,
    alphas,
    alphanums,
    Forward,
    oneOf,
    quotedString,
    dblQuotedString,
    infixNotation,
    opAssoc,
    restOfLine,
    CaselessKeyword,
    pyparsing_common as ppc,
)

# Create keywords constant expressions
SELECT, FROM, WHERE, AND, OR, IN, IS, NOT, NULL, INSERT, INTO, VALUES, DELETE, CREATE, TABLE, IF, EXISTS, CHAR, VARCHAR, INT, FLOAT, DATE, DATETIME, TIME, YEAR, DATABASE = map(
    CaselessKeyword, "select from where and or in is not null insert into values delete create table if exists char varchar int float date datetime time year database".split()
)

KEYWORDS = SELECT ^ FROM ^ WHERE ^ AND ^ OR ^ IN ^ IS ^ NOT ^ NULL ^ INSERT ^ INTO ^ VALUES ^ DELETE ^ CREATE ^ TABLE ^ IF ^ EXISTS ^ CHAR ^ VARCHAR ^ INT ^ FLOAT ^ DATE ^ DATETIME ^ TIME ^ YEAR ^ DATABASE


# if not exists keyword
IF_NOT_EXISTS = IF + NOT + EXISTS

# not null keyword
NOT_NULL = NOT + NULL

# Token for an identifier
ident = ~KEYWORDS + ~Literal(' ') + Word(alphas, alphanums + "_$").setName("identifier")
# Token for a column name
# a columName is formed by identifier separated by a dot and combined together
columnName = delimitedList(ident, ".", combine=True).setName("column name")
columnName.addParseAction(ppc.upcaseTokens)
# Token for a sublist of column name
columnNameList = Group(delimitedList(columnName))
# Token for a table name
tableName = delimitedList(ident, ".", combine=True).setName("table name")
tableName.addParseAction(ppc.upcaseTokens)
# Token for a sublist of table name
tableNameList = Group(delimitedList(tableName))

# list of token literal to identify binary operator
binop = oneOf("= != < > >= <= eq ne lt le gt ge", caseless=True)
# Token to match float number
realNum = ppc.real()
# Token to match integer
intNum = ppc.signed_integer()

# Token for matching the right element of an comparison using binary op
columnRval = (
    realNum | intNum | quotedString | columnName
)

# Token for matching where condition
whereCondition = Group(
    (columnName + binop + columnRval)
    | (columnName + IN + Group("(" + delimitedList(columnRval) + ")"))
    | (columnName + IS + (NULL | NOT_NULL))
)

whereExpression = infixNotation(
    whereCondition,
    [(NOT, 1, opAssoc.RIGHT), (AND, 2, opAssoc.LEFT), (OR, 2, opAssoc.LEFT),],
)

# define Oracle comment format, and ignore them
oracleSqlComment = "--" + restOfLine

def create_db_parse(query):
    # Forward declaration of selectStmt to define it later
    createDBStmt = Forward()
    # define the grammar
    # e.g the rules to parse an sql select query
    createDBStmt <<= (
        CREATE
        + DATABASE
        + Optional(IF_NOT_EXISTS)("existence_clause")
        + ident("dbName")
    )
    createDBStmt.ignore(oracleSqlComment)
    return createDBStmt.parseString(query)

def delete_query_parse(query):
    deleteStmt = Forward()
    # define the grammar
    # e.g the rules to parse an sql select query
    deleteStmt <<= (
        DELETE
        + FROM
        + tableName("tableName")
        + Optional(Group(WHERE + whereExpression), "")("where")
    )
    deleteStmt.ignore(oracleSqlComment)
    return deleteStmt.parseString(query)

def insert_query_parse(query):
    insertStmt = Forward()
    value = (
        realNum | intNum | quotedString | dblQuotedString
    )
    values = Group(delimitedList(value))
    valuesWithParenthesis = "(" + values + ")"
    valuesList = Group(delimitedList(valuesWithParenthesis))
    # define the grammar
    insertStmt <<= (
        INSERT
        + INTO
        + tableName("tableName")
        + VALUES
        + valuesList("valuesList")
    )
    insertStmt.ignore(oracleSqlComment)
    return insertStmt.parseString(query)

def create_table_query_parse(query):
    createTableStmt = Forward()
    charType = Combine(CHAR + "(" + intNum + ")")
    varcharType = Combine(VARCHAR + "(" + intNum + ")")

    columnTypeName = (
        INT | FLOAT | charType | varcharType | DATE | DATETIME | TIME | YEAR
    )

    column = Group(columnName + columnTypeName + Optional(NOT_NULL | NULL))
    # Token for a sublist of column name
    columnList = Group(delimitedList(column))
    # define the grammar
    # e.g the rules to parse an sql select query
    createTableStmt <<= (
        CREATE
        + TABLE
        + tableName("tableName")
        + "("
        + columnList("columnList")
        + ")"
    )
    createTableStmt.ignore(oracleSqlComment)
    return createTableStmt.parseString(query)
    return tableName

def select_parsing(query):
    selectStmt = Forward()
    selectStmt <<= (
        SELECT
        + ("*" | columnNameList)("columnsToShow")
        + FROM
        + tableNameList("tables")
        + Optional(Group(WHERE + whereExpression), "")("where")
    )
    selectStmt.ignore(oracleSqlComment)
    return selectStmt.parseString(query)

if __name__ == "__main__":
    query = input("Enter an sql select query: ")
    res = create_table_query_parse(query)
    print("table", res.tableName)
    print("colonne", res.columnList)















