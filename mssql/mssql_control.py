import pyodbc


def conneected():
    server = 'MSI\SQLEXPRESS'
    database = 'TEST'
    username = 'SA'
    password = '12345'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                          server+';DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = cnxn.cursor()

    # create('test', cursor)
    # query_column_exist(cursor, 'test', 'id')
    # alter_column(cursor,'test','A','nvarchar(30)','null')
    # alter_column(cursor,'test','B','nvarchar(30)','null')
    # insert_values(cursor,'test','A,B',"'aaa','bbb'")
    return cursor

def create(table, cursor):
    cursor.execute(
        "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME =?", table)
    detail = cursor.fetchone()
    command = ("""
    CREATE TABLE [dbo].["""+table+"""](
	[id] [uniqueidentifier] ROWGUIDCOL  NOT NULL,
    CONSTRAINT [PK_"""+table+"""] PRIMARY KEY CLUSTERED
    (
	    [id] ASC
    )WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
    ) ON [PRIMARY]
    ALTER TABLE [dbo].["""+table+"""] ADD  CONSTRAINT [DF_"""+table+"""_id]  DEFAULT (newid()) FOR [id]

    """)
    if detail == None:
        cursor.execute(command)
        cursor.execute('commit')
        return True
    else:
        return True


def alter_column(cursor, table, column_name, data_type, check_null):
    command = ("""
    ALTER TABLE  """+table+""" ADD """ '"'+column_name+'"' """ """+data_type+""" """+check_null+"""
    """)
    cursor.execute(command)
    cursor.execute('commit')


def query_column_exist(cursor, table, column_name):
    cursor.execute(
        "SELECT 1 FROM sys.columns WHERE Name = ? AND Object_ID = Object_ID(?)", column_name, table)
    detail = cursor.fetchone()
    if detail == None:
        return False
    else:
        return True
def query_values_not_exist_insert(cursor, table, column_names, args_str):
    split_column_names = column_names.split(',')
    split_args_str = args_str.split(',')
    x = 0
    where_command =''
    for s in split_column_names:
        where_command += s +'='+split_args_str[x]+' and '
        x= x+1
    command_insert_values = 'INSERT INTO %s (%s) VALUES (%s) ' % (
        table, column_names, args_str)
    where_command = where_command[:-4]

    sql_command = """
        IF NOT EXISTS(SELECT * FROM """+table+""" WHERE """+where_command+""")
        BEGIN
	            """+command_insert_values+"""
        END
    """
    cursor.execute(sql_command)
    cursor.execute('commit')

# def insert_values(cursor, table, column_names, args_str):
#     query_values_exist(cursor, table, column_names, args_str)
#     sql_command = 'INSERT INTO %s (%s) VALUES (%s) ' % (
#         table, column_names, args_str)
#     cursor.execute(sql_command)
#     cursor.execute('commit')
