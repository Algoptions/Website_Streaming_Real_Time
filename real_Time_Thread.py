import random
import threading
import time
from datetime import date
from datetime import datetime

import django
import django.db  # from Management.real_time_data.writeLogs import logsWrite
from django.conf import settings


import bonanza_api_response
# Python program to illustrate the concept
# of threading
# importing the threading module
import get_db
import indira_api_response
import mysql.connector

class Real_Time_Positions():
    def __init__(self):
        self.listOfRows = []
        self.return_data = []
        execution_date = date.today()

        self.iteration = 10
        self.all_access_token_dict = {}

        self.table_name = "Management_real_time_positions_data"

        # Create a cursor object


    def getYesRecords(self, table_name):
        conn = get_db.get_connection()
        cursorObject = conn.cursor()
        query = "SELECT  *  from " + table_name + " where Status = \'Yes\'"
        # query = "SELECT  *  from " + table_name + " where Status = \'Yes\' AND Broker= \'Indira\' " # AND Broker= \'Indothai\' AND Trading_Symbol= \'BankNifty\'
        # query = "SELECT  *  from " + table_name + " where Status = \'Yes\' AND Broker= \'Bonanza\' "
        cursorObject.execute(query)
        query_result = cursorObject.fetchall()

        conn.commit()
        conn.close()
        return query_result

    def readDatabase(self):
        self.db_flag = True
        account_data = self.getYesRecords("accountDetailsTable")
        for i in account_data:
            if i[3].lower() == 'yes' and i[14].lower() != 'zerodha' :#  and i[14].lower() == 'bonanza' and i[0].lower() == 'h7555'and i[0].lower() == 'at22'
                valuesInList = list(i)
                self.listOfRows.append(valuesInList)

    def position_book_execute_user_list(self, row):
        conn = self.djangodb()
        mycursor = conn.cursor()
        while True:
            apiClientId = row[0]
            system = row[5]
            strategy = row[6]
            name = row[12]
            trading_symbol = row[4]
            Broker = row[14]
            Quantity = row[7]

            merged_data = {}

            print(" Threads working For account  :" + apiClientId)
            if str(row[5]).lower() == 'indraapi':
                print("---------------------------------")
                print("---------------", row[0], "------------------")
                start = time.time()
                access_token = self.all_access_token_dict[apiClientId]
                try:
                    merged_data = indira_api_response.Indira_API_RESPONSE(apiClientId, access_token, strategy, name, trading_symbol, Broker).get_positionBook_data()
                except:
                    pass
                done = time.time()
                elapsed = done - start
                print("position book ", row[0], round(elapsed, 2))
                print("---------------------------------")

            if str(row[5]).lower() == 'symphony':
                print("---------------------------------")
                print("---------------", row[0], "------------------")
                start = time.time()
                access_token = self.all_access_token_dict[apiClientId]
                try:
                    merged_data = bonanza_api_response.Bonanza_API_RESPONSE(apiClientId,access_token, strategy, name, trading_symbol, Broker).get_positionBook_data()
                except:
                    pass
                done = time.time()
                elapsed = done - start
                print("position book ", row[0], round(elapsed, 2))
                print("---------------------------------")
            now = datetime.now()  # current date and time
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            current_time = str(now.strftime("%H:%M"))
            # if str(current_time) == "16:00" or str(current_time) == "16:01" or str(current_time) == "16:02" \
            #         or str(current_time) == "16:03" or str(current_time) == "16:04" or str(current_time) == "16:05" \
            #         or str(current_time) == "16:06" or str(current_time) == "16:07" or str(current_time) == "16:08" \
            #         or str(current_time) == "16:09":
            #     time_thread = False

            # print("Quantity ="+Quantity)
            if Quantity == "0" or Quantity == "None" or Quantity == "":
                Quantity = "None"




            sql = "UPDATE Management_real_time_positions_data SET Strategy = %s, name = %s" ", trading_symbol = %s, CP = %s, CQ = %s," \
                  " CLP = %s, CAP = %s, PP = %s, PQ = %s, PAP = %s"  ", PP_B = %s," \
                  " PQ_B = %s, PAP_B = %s, PLP_B = %s, PLP = %s, NOP = %s," \
                  " OpenPOs = %s, Broker = %s" ", defined_quantity = %s, datetime = %s WHERE apiClientId = %s"
            val = (merged_data['Strategy'], merged_data['name'], merged_data['trading_symbol'], merged_data['CP'], merged_data['CQ'],
                   merged_data['CLP'],merged_data['CAP'], merged_data['PP'], merged_data['PQ'], merged_data['PAP'], merged_data['PP_B'],
                   merged_data['PQ_B'], merged_data['PAP_B'], merged_data['PLP_B'], merged_data['PLP'],merged_data['NOP'],
                   merged_data['OpenPOs'], merged_data['Broker'], str(Quantity), str(date_time), merged_data['apiClientId'])



            timeout = 5
            now = time.time()
            give_up_time = now + timeout
            retries = 0
            while now < give_up_time:
                now = time.time()
                try:
                    mycursor.execute(sql, val)
                    conn.commit()


                    if retries:
                        print(f'db_retry: Succeeded after {retries} retries')
                    # return result
                except django.db.OperationalError as exception:
                    msg = str(exception)
                    if 'locked' in msg:  # pragma: no cover
                        retries += 1
                        wait_time = random.uniform(1, timeout / 10)
                        print(f'db_retry: {msg}: Retrying after {wait_time} seconds')
                        django.db.close_old_connections()
                        time.sleep(wait_time)
                    else:  # pragma: no cover
                        print(f'db_retry: {msg}: Giving up')
                        raise
            timeout = 5
            now = time.time()
            give_up_time = now + timeout
            retries = 0
            while now < give_up_time:
                now = time.time()
                try:
                    mycursor.execute(sql, val)
                    conn.commit()
                    time.sleep(1)
                    if retries:
                        print(f'db_retry: Succeeded after {retries} retries')
                    # return result
                except django.db.OperationalError as exception:
                    msg = str(exception)
                    if 'locked' in msg:  # pragma: no cover
                        retries += 1
                        wait_time = random.uniform(1, timeout / 10)
                        print(f'db_retry: {msg}: Retrying after {wait_time} seconds')
                        django.db.close_old_connections()
                        time.sleep(wait_time)
                    else:  # pragma: no cover
                        print(f'db_retry: {msg}: Giving up')
                        raise


    def order_book_execute_user_list(self, row):
        conn = self.djangodb()
        mycursor = conn.cursor()
        while True:
            apiClientId = row[0]
            system = row[5]
            strategy = row[6]
            name = row[12]
            trading_symbol = row[4]
            Broker = row[14]
            Quantity = row[7]



            merged_data = {}

            print(" Threads working For account  :" + apiClientId)
            if str(row[5]).lower() == 'indraapi':
                print("---------------------------------")
                print("---------------", row[0], "------------------")
                start = time.time()
                access_token = self.all_access_token_dict[apiClientId]
                try:
                    merged_data = indira_api_response.Indira_API_RESPONSE(apiClientId, access_token, strategy, name, trading_symbol, Broker).order_book_data()
                except:
                    pass
                done = time.time()
                elapsed = done - start
                print("order Book",row[0], round(elapsed, 2))
                print("---------------------------------")

            if str(row[5]).lower() == 'symphony':
                print("---------------------------------")
                print("---------------", row[0], "------------------")
                start = time.time()
                access_token = self.all_access_token_dict[apiClientId]
                try:
                    merged_data = bonanza_api_response.Bonanza_API_RESPONSE(apiClientId,access_token, strategy, name, trading_symbol, Broker).order_book_data()
                except:
                    pass
                done = time.time()
                elapsed = done - start
                print(row[0], round(elapsed, 2))
                print("---------------------------------")
            now = datetime.now()  # current date and time
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            current_time = str(now.strftime("%H:%M"))
            # if str(current_time) == "16:00" or str(current_time) == "16:01" or str(current_time) == "16:02" \
            #         or str(current_time) == "16:03" or str(current_time) == "16:04" or str(current_time) == "16:05" \
            #         or str(current_time) == "16:06" or str(current_time) == "16:07" or str(current_time) == "16:08" \
            #         or str(current_time) == "16:09":
            #     time_thread = False

            # print("Quantity ="+Quantity)
            sql = "UPDATE Management_real_time_positions_data SET CSLP = %s, PSLP = %s" ", CSL = %s, PSL = %s, NoSL = %s," \
                  " OpenSl = %s  WHERE apiClientId = %s"
            val = (merged_data['CSLP'], merged_data['PSLP'], merged_data['CSL'], merged_data['PSL'], merged_data['NoSL'],
                   merged_data['OpenSl'], merged_data['apiClientId'])



            timeout = 5
            now = time.time()
            give_up_time = now + timeout
            retries = 0
            while now < give_up_time:
                now = time.time()
                try:
                    mycursor.execute(sql, val)
                    conn.commit()
                    if retries:
                        print(f'db_retry: Succeeded after {retries} retries')
                    # return result
                except django.db.OperationalError as exception:
                    msg = str(exception)
                    if 'locked' in msg:  # pragma: no cover
                        retries += 1
                        wait_time = random.uniform(1, timeout / 10)
                        print(f'db_retry: {msg}: Retrying after {wait_time} seconds')
                        django.db.close_old_connections()
                        time.sleep(wait_time)
                    else:  # pragma: no cover
                        print(f'db_retry: {msg}: Giving up')
                        raise

            timeout = 5
            now = time.time()
            give_up_time = now + timeout
            retries = 0
            while now < give_up_time:
                now = time.time()
                try:
                    mycursor.execute(sql, val)
                    conn.commit()
                    time.sleep(1)
                    if retries:
                        print(f'db_retry: Succeeded after {retries} retries')
                    # return result
                except django.db.OperationalError as exception:
                    msg = str(exception)
                    if 'locked' in msg:  # pragma: no cover
                        retries += 1
                        wait_time = random.uniform(1, timeout / 10)
                        print(f'db_retry: {msg}: Retrying after {wait_time} seconds')
                        django.db.close_old_connections()
                        time.sleep(wait_time)
                    else:  # pragma: no cover
                        print(f'db_retry: {msg}: Giving up')
                        raise


    def available_fund_execute_user_list(self, row):
        conn = self.djangodb()
        mycursor = conn.cursor()
        while True:
            apiClientId = row[0]
            system = row[5]
            strategy = row[6]
            name = row[12]
            trading_symbol = row[4]
            Broker = row[14]
            Quantity = row[7]



            merged_data = {}

            print(" Threads working For account  :" + apiClientId)
            if str(row[5]).lower() == 'indraapi':
                print("---------------------------------")
                print("---------------", row[0], "------------------")
                start = time.time()
                access_token = self.all_access_token_dict[apiClientId]
                try:
                    merged_data = indira_api_response.Indira_API_RESPONSE(apiClientId, access_token, strategy, name, trading_symbol, Broker).get_available_fund()
                except:
                    pass
                done = time.time()
                elapsed = done - start
                print("Available Balance :",row[0], round(elapsed, 2))
                print("---------------------------------")

            if str(row[5]).lower() == 'symphony':
                print("---------------------------------")
                print("---------------", row[0], "------------------")
                start = time.time()
                access_token = self.all_access_token_dict[apiClientId]
                try:
                    merged_data = bonanza_api_response.Bonanza_API_RESPONSE(apiClientId,access_token, strategy, name, trading_symbol, Broker).get_available_fund()
                except:
                    pass
                done = time.time()
                elapsed = done - start
                print(row[0], round(elapsed, 2))
                print("---------------------------------")

            now = datetime.now()  # current date and time
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            current_time = str(now.strftime("%H:%M"))
            # if str(current_time) == "16:00" or str(current_time) == "16:01" or str(current_time) == "16:02" \
            #         or str(current_time) == "16:03" or str(current_time) == "16:04" or str(current_time) == "16:05" \
            #         or str(current_time) == "16:06" or str(current_time) == "16:07" or str(current_time) == "16:08" \
            #         or str(current_time) == "16:09":
            #     time_thread = False

            # print("Quantity ="+Quantity)
            sql = "UPDATE Management_real_time_positions_data SET AF = %s WHERE apiClientId = %s"
            val = (merged_data['AF'], merged_data['apiClientId'])



            timeout = 5
            now = time.time()
            give_up_time = now + timeout
            retries = 0
            while now < give_up_time:
                now = time.time()
                try:
                    mycursor.execute(sql, val)
                    conn.commit()
                    if retries:
                        print(f'db_retry: Succeeded after {retries} retries')
                    # return result
                except django.db.OperationalError as exception:
                    msg = str(exception)
                    if 'locked' in msg:  # pragma: no cover
                        retries += 1
                        wait_time = random.uniform(1, timeout / 10)
                        print(f'db_retry: {msg}: Retrying after {wait_time} seconds')
                        django.db.close_old_connections()
                        time.sleep(wait_time)
                    else:  # pragma: no cover
                        print(f'db_retry: {msg}: Giving up')
                        raise

            timeout = 5
            now = time.time()
            give_up_time = now + timeout
            retries = 0
            while now < give_up_time:
                now = time.time()
                try:
                    mycursor.execute(sql, val)
                    conn.commit()
                    time.sleep(1)
                    if retries:
                        print(f'db_retry: Succeeded after {retries} retries')
                    # return result
                except django.db.OperationalError as exception:
                    msg = str(exception)
                    if 'locked' in msg:  # pragma: no cover
                        retries += 1
                        wait_time = random.uniform(1, timeout / 10)
                        print(f'db_retry: {msg}: Retrying after {wait_time} seconds')
                        django.db.close_old_connections()
                        time.sleep(wait_time)
                    else:  # pragma: no cover
                        print(f'db_retry: {msg}: Giving up')
                        raise



    def get_all_access_token(self):
        conn = get_db.get_connection()
        cursorObject = conn.cursor()
        read = ''
        for row_list in self.listOfRows:
            # for indira
            if row_list[5].lower() == 'IndraAPI'.lower():
                read = "SELECT * FROM  algoprimary.odinAccessTokenTable  WHERE clientId = '" + row_list[0] + "'"
            if row_list[5].lower() == 'Symphony'.lower():
                read = "SELECT * FROM  algoprimary.symphonyAccessTokenTable  WHERE clientId = '" + row_list[0] + "'"
            cursorObject.execute(read)
            allData = cursorObject.fetchall()
            if allData != []:
                accessToken = allData[0][2]
                # apiKey = allData[0][1]
                self.all_access_token_dict[row_list[0]] = accessToken
            else:
                continue
        conn.commit()
        conn.close()

    def create_thread(self):
        for row_list in self.listOfRows:
            #position book
            position_book_thread = threading.Thread(target=self.position_book_execute_user_list, args=(row_list,))
            print(":  Starting position_book_thread for account : " + row_list[0])
            position_book_thread.start()

            order_book_thread = threading.Thread(target=self.order_book_execute_user_list, args=(row_list,))
            print(":  Starting order_book_thread for account : " + row_list[0])
            order_book_thread.start()
            #
            available_fund_thread = threading.Thread(target=self.available_fund_execute_user_list, args=(row_list,))
            print(":  Starting available_fund_thread for account : " + row_list[0])
            available_fund_thread.start()

        print("all threads created")

    def djangodb(self):
        conn = mysql.connector.connect(
            host="algoprimary.c1jlffazred9.ap-south-1.rds.amazonaws.com",
            user="admin",
            password="adminadmin",
            database="djangodb"
        # conn = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     database="djangodb"
        )
        return conn

    def databaseConnectionCommitAndClosed(self, conn):
        conn.commit()
        conn.close()

    def run(self):
        conn = self.djangodb()
        mycursor = conn.cursor()
        query = "DELETE FROM Management_real_time_positions_data"
        mycursor.execute(query)
        conn.commit()

        self.readDatabase()
        for client in self.listOfRows:
            apiClientId = client[0]
            sql = "INSERT INTO Management_real_time_positions_data (apiClientId, Strategy, name,trading_symbol,CP," \
                  " CQ, CLP, CAP," "PP,PQ, " \
                  "PAP, PLP, PP_B,PQ_B,PAP_B," \
                  "PLP_B, CSLP, PSLP,CSL,PSL," \
                  " NOP, NoSL,OpenPOs, OpenSl, Broker," \
                  " defined_quantity, datetime,AF)" \
                    " VALUES (%s, %s,%s, %s, %s," \
                  "%s, %s,%s, %s, %s," \
                  "%s, %s,%s, %s, %s," \
                  "%s, %s,%s, %s, %s," \
                  "%s, %s,%s, %s, %s," \
                  "%s, %s,%s)"
            val = (apiClientId,'initializing','initializing','initializing','initializing',
                   'initializing','initializing','initializing','initializing','initializing',
                   'initializing','initializing','initializing','initializing','initializing',
                   'initializing','initializing','initializing','initializing','initializing'
                   ,'initializing','initializing','initializing','initializing','initializing',
                   'initializing','initializing','initializing')
            mycursor.execute(sql, val)
            conn.commit()

        mycursor.close()


        self.get_all_access_token()
        self.create_thread()



Real_Time_Positions().run()
