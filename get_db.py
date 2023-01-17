
import mysql.connector
def get_connection():
    conn = mysql.connector.connect(
        host="algoprimary.c1jlffazred9.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="adminadmin",
        database="algoprimary"
    )
    # conn = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     database="algoprimary"
    # )
    return conn



#
# # Insert data into the table
# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("John Smith", "123 Main St.")
# mycursor.execute(sql, val)
# mydb.commit()
#
# # Read data from the table
# sql = "SELECT * FROM customers"
# mycursor.execute(sql)
# results = mycursor.fetchall()
# for row in results:
#     print(row)
#
# # Update data in the table
# sql = "UPDATE customers SET address = %s WHERE id = %s"
# val = ("456 Park Ave.", 1)
# mycursor.execute(sql, val)
# mydb.commit()
#
# # Delete data from the table
# sql = "DELETE FROM customers WHERE id = %s"
# val = (1,)
# mycursor.execute(sql, val)
# mydb.commit()
# mycursor.close()
#
#
# mydb.close()
#
# "UPDATE customers SET address = %s WHERE apiClientId = %s"
#
#
#
# def databaseConnectionCommitAndClosed(self, conn):
#     conn.commit()
#     conn.close()
#     # self.logger.info(
#     #     self.apiClientId + ": Database connection closed")
#
# def insertDataTotalFundAvailable(self, table_name, dataList):
#
#     cursorObject = self.cursorObject
#     conn = self.conn
#     for data in dataList:
#         Client = data[0]
#         Client_Name = data[1]
#         Available_Fund = data[2]
#         Broker = data[3]
#
#         delete = "DELETE from " + table_name + " where Client= '" + str(Client) + "'"
#         self.logger.info(Client + " : " + str(delete))
#         cursorObject.execute(delete)
#         insert = "INSERT INTO " + table_name + " (Client, Client_Name,Available_Fund,Broker) VALUES('" + Client + "','" + Client_Name + "','" + Available_Fund + "','" + Broker + "')"
#         self.logger.info(Client + " : " + str(insert))
#         cursorObject.execute(insert)
#         self.logger.info(
#             self.apiClientId + ": Data inserted into Table: " + str(table_name))
#     else:
#         self.logger.info(
#             self.apiClientId + ": Please enter correct Table")
#     self.databaseConnectionCommitAndClosed(conn)
#     return True
#
# def deleteData(self, table_name, clientCode):
#     self.getConnection(table_name)
#     # data comes in map data = {"password":"mno"}
#     cursorObject = self.cursorObject
#     conn = self.conn
#     delete = "DELETE from " + table_name + " where clientCode= '" + str(clientCode) + "'"
#     self.logger.info(self.apiClientId + " : " + str(delete))
#     cursorObject.execute(delete)
#     # self.logger.info(
#     #     self.apiClientId + ": All records deleted from the Table: " + str(table_name))
#     self.databaseConnectionCommitAndClosed(conn)
#     return True
#
# def deleteAllData(self, table_name):
#     self.getConnection(table_name)
#     # data comes in map data = {"password":"mno"}
#     cursorObject = self.cursorObject
#     conn = self.conn
#     delete = "DELETE from " + str(table_name)
#     self.logger.info(self.apiClientId + " : " + str(delete))
#     cursorObject.execute(delete)
#     self.logger.info(
#         self.apiClientId + ": All records deleted from the Table: " + str(table_name))
#     self.databaseConnectionCommitAndClosed(conn)
#     return True