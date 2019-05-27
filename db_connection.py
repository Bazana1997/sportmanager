import pyodbc
import hashlib


# connection = pyodbc.connect(
#    "Driver={ODBC Driver 17 for SQL Server};"
#    "Server=localhost;"
#    "Database=TestDB;"
#    "UID=sa;"
#    "PWD=<6DeDiciembre>;"
# )

# returns a hash sha256 from a string


def string2hash(password):
    return hashlib.sha1(str.encode(password)).hexdigest()


# convert a list to a string of values with format "'value1', 'values2', ..."


def list2values(columns):
    return ','.join("\'" + str(e) + "\'" for e in columns)


# convert a list to a string of columns name with format "value1, values2, ..."
def list2columns(columns):
    return ','.join(columns)


# convert two lists to a string of assignments with format
# "column2='value1', columns2='value2'"
def list2assignments(columns, values):
    assignments = ""
    for i in range(len(columns)):
        assignments += str(columns[i]) + " = \'" + str(values[i]) + "\', "

    return assignments[:len(assignments) - 2]


# SELECT Query


class SQLConnection():
    """docstring for SQL_Connection"""

    def __init__(self, driver='', server_name='', db_name='', UID='', PWD='', connection_str=''):
        self.connection_str = ''
        self.connection = None
        self.cursor = None
        if connection_str == '':
            self.driver = "{ODBC Driver 17 for SQL Server}" if driver is None else driver
            self.server_name = server_name
            self.db_name = db_name
            self.UID = UID
            self.connection_str = "DRIVER={};".format(self.driver)
            self.connection_str += "Server={};".format(self.server_name)
            self.connection_str += "Database={};".format(self.db_name)
            self.connection_str += "UID={};".format(self.UID)
        else:
            self.connection_str = connection_str

        try:
            self.connection = pyodbc.connect(
                self.connection_str + "PWD=" + PWD + ";")
            self.init_cursor()
        except Exception as e:
            print("Error ----> ", e)

    def select_tables(self, tables, columns, condition=None):
        data = []
        query = "SELECT {} FROM {}{}".format(list2columns(columns), list2columns(tables),
                                             "\nWHERE " + condition + ";" if condition is not None else ";")
        print(query)
        try:
            self.cursor.execute(query)
        except Exception as e:
            print("Error ---->", e)
            return None
        for row in self.cursor:
            print('row{}'.format(row))
            data.append(row)
        return data

    def read(self, table, columns, condition=None):
        print("Read")
        data = []
        # query = "SELECT " + list2columns(columns) + " FROM " + table
        query = "SELECT {} FROM {}{}".format(list2columns(
            columns), table, "\nWHERE " + condition + ";" if condition is not None else ";")
        print(query)

        try:
            self.cursor.execute(query)
        except Exception as e:
            print("Error ---->", e)
            return None

        for row in self.cursor:
            print('row{}'.format(row))
            data.append(row)
        return data

    # INSERT INTO Query
    def create(self, table, columns, values):
        print("Create")
        query = "INSERT INTO {} ({})\nVALUES({});".format(
            table, list2columns(columns), list2values(values))
        print(query)
        try:
            self.cursor.execute(query)
            return "Success"
        except Exception as e:
            print("Error ---->", e)
            return None

    # UPDATE Query
    def update(self, table, columns, values, condition):
        print("Delete")

        query = "UPDATE {}\nSET {}\nWHERE {};".format(
            table, list2assignments(columns, values), condition)
        try:
            self.cursor.execute(query)
            return "Success"
        except Exception as e:
            print("Error ---->", e)
            return None

    # DELETE Query
    def delete(self, table, condition):
        query = "DELETE FROM {} WHERE {};".format(table, condition)
        try:
            self.cursor.execute(query)
            return "Success"
        except Exception as e:
            print("Error ---->", e)
            return None

    # Finding the current last id for assign a new tuple
    def next_ID(self, table, id):
        self.cursor.execute("SELECT MAX({}) FROM {}".format(id, table))
        ID = 0
        for i in self.cursor:
            ID = i
        print(ID)
        return ID[0]

    def commit(self):
        self.cursor.commit()

    def init_cursor(self):
        self.cursor = self.connection.cursor()

# connection.close()
