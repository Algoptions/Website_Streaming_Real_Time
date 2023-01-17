# import views

import json
# from Management.real_time_data.writeLogs import logsWrite
from datetime import date

import requests


class Indira_API_RESPONSE:
    def __init__(self, apiClientId, accessToken, strategy, name, trading_symbol, broker):
        execution_date = date.today()
        # logs = logsWrite(str(execution_date) + "_indira_api_response_")
        # self.logger = logs.get_logger('_Indira_API_RESPONSE_')
        self.apiClientId = apiClientId
        self.strategy = strategy
        self.name = name
        self.trading_symbol = trading_symbol
        self.accessToken = accessToken
        self.broker = broker
        self.headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "a4fca2a5-1f9c-b59e-e5ad-6bcda36c5144",
            'Authorization': 'Bearer {accessToken}'.format(accessToken=self.accessToken)
        }

    def get_positionBook_data(self):
        book_dict = {}
        book_dict['apiClientId'] = self.apiClientId
        book_dict['Strategy'] = self.strategy
        book_dict['name'] = self.name
        book_dict['trading_symbol'] = self.trading_symbol
        book_dict['Broker'] = self.broker
        book_dict['CP'] = "None"
        book_dict['CQ'] = "0"
        book_dict['CLP'] = "None"
        book_dict['CAP'] = "None"
        book_dict['PP'] = "None"
        book_dict['PQ'] = "0"
        book_dict['PAP'] = "None"
        book_dict['PLP'] = "None"
        book_dict['PP_B'] = "None"
        book_dict['PQ_B'] = "0"
        book_dict['PAP_B'] = "None"
        book_dict['PLP_B'] = "None"
        book_dict['NOP'] = "NOP"
        book_dict['OpenPOs'] = "None"

        open_pos_put = "None"
        open_pos_call = "None"
        open_pos_put_buy = "None"

        position_requestUrl = "https://jri4df7kaa.execute-api.ap-south-1.amazonaws.com/prod/interactive/transactional/v1/portfolio/positions/expiry"
        response = requests.get(position_requestUrl, headers=self.headers)
        response.close()

        if response == []:
            return book_dict

        responseStatusCode = response.status_code
        responseMessage = response.json()

        if responseStatusCode != 200:
            return book_dict
        # else:
            # responseMessage = responseMessage["data"]

        # convert dict to string and manipulate
        responseMessage = str(responseMessage).replace('symbol', 'trading_symbol').replace('avg_sell_price', 'average_sell_price').replace('net_quantity',
                                                                                                                                           'quantity'). \
            replace('trade_price', 'average_sell_price').replace(
            'ltp', 'last_trade_price').replace('scrip_token', 'instrument_token').replace('order_id', 'orderId').replace('order_timestamp',
                                                                                                                         'trade_time').replace(
            'traded_quantity', 'quantity').replace('trade_timestamp', 'trade_time').replace('trade_quantity', 'quantity').replace('tradingsymbol',
                                                                                                                                  'trading_symbol').replace(
            'last_price', 'last_trade_price')

        # convert string to dict to List of Dict
        tempList = []
        responseMessage = json.loads(responseMessage.replace("'", "\""))
        tempList.append(responseMessage)
        responseMessage = tempList[0]
        responseMessage = responseMessage['data']
        responseMessage = [x for x in responseMessage if (x['exchange'] == 'NSE_FO' and x['quantity'] != 0)]

        PositionBookAPIData = responseMessage

        Npositions = 0
        # # print(PositionBookAPIData)
        for position_data in PositionBookAPIData:
            # # print(position_data)
            if position_data['trading_symbol'].lower() == self.trading_symbol.lower():
                Npositions = Npositions + 1
                if position_data['option_type'].lower() == 'ce':
                    stringcp = int(float(position_data.get('strike_price')))
                    book_dict['CP'] = str(stringcp)
                    book_dict['CQ'] = str(-position_data.get('quantity'))
                    book_dict['CAP'] = str(position_data.get('average_sell_price'))
                    book_dict['CLP'] = str(position_data.get('last_trade_price'))
                    open_pos_call = str(position_data['trading_symbol']) + str(position_data['expiry_date']) + str(position_data['strike_price'][:-3]) + str(
                        position_data['option_type'])


                elif (position_data['option_type'].lower() == 'pe' and position_data['quantity'] < 0):
                    stringpp = int(float(position_data.get('strike_price')))
                    book_dict['PP'] = str(stringpp)
                    book_dict['PQ'] = str(-position_data.get('quantity'))
                    book_dict['PAP'] = str(position_data.get('average_sell_price'))
                    book_dict['PLP'] = str(position_data.get('last_trade_price'))
                    # get last trade price from KITE as it gives correct data
                    open_pos_put = str(position_data['trading_symbol']) + str(position_data['expiry_date']) + str(position_data['strike_price'][:-3]) + str(
                        position_data['option_type'])

                elif (position_data['option_type'].lower() == 'pe' and position_data['quantity'] > 0):
                    stringpp_B = int(float(position_data.get('strike_price')))
                    book_dict['PP_B'] = str(stringpp_B)
                    book_dict['PQ_B'] = str(position_data.get('quantity'))
                    book_dict['PAP_B'] = str(position_data.get('avg_buy_price'))
                    book_dict['PLP_B'] = str(position_data.get('last_trade_price'))
                    open_pos_put_buy = str(position_data['trading_symbol']) + str(position_data['expiry_date']) + str(position_data['strike_price'][:-3]) + str(
                        position_data['option_type'])

        book_dict['NOP'] = str(Npositions)
        if str(self.strategy).lower() == "putiron":
            book_dict['OpenPOs'] = open_pos_call + "||" + open_pos_put + "||" + open_pos_put_buy
        else:
            book_dict['OpenPOs'] = open_pos_call + "||" + open_pos_put

        # return
        book_dict = self.markCellInRedAsPerRule(book_dict)
        return book_dict

    def dict_clean(self, items):
        result = {}
        for key, value in items:
            if value is None:
                value = 'None'
            result[key] = value
        return result

    def order_book_data(self):
        book_dict = {}
        book_dict['apiClientId'] = self.apiClientId
        book_dict['CSLP'] = "ncsl"
        book_dict['PSLP'] = "npsl"
        book_dict['CSL'] = "None"
        book_dict['CSLP'] = "None"
        book_dict['PSL'] = "None"
        book_dict['PSLP'] = "None"
        book_dict['NoSL'] = "None"
        book_dict['OpenSl'] = "None"

        # oredr data
        order_requestUrl = "https://jri4df7kaa.execute-api.ap-south-1.amazonaws.com/prod/interactive/transactional/v1/orders?limit=300&offset=1"
        response = requests.get(order_requestUrl, headers=self.headers)
        response.close()

        if response == []:
            return book_dict

        responseStatusCode = response.status_code
        responseMessage = response.json()

        if responseStatusCode != 200:
            return book_dict
        else:
            responseMessage =responseMessage['data']

        responseMessageLenMoreThanOneFlag = False
        if len(responseMessage) > 0:
            responseMessageLenMoreThanOneFlag = True

        # remove none to 'none'
        dict_str = json.dumps(responseMessage)
        responseMessage = json.loads(dict_str, object_pairs_hook=self.dict_clean)

        # convert dict to string and manipulate
        responseMessage = str(responseMessage).replace('symbol', 'trading_symbol').replace('avg_sell_price', 'average_sell_price').replace('net_quantity',
                                                                                                                                           'quantity').replace(
            'ltp', 'last_trade_price').replace('scrip_token', 'instrument_token').replace('order_id', 'orderId').replace('order_timestamp',
                                                                                                                         'trade_time').replace(
            'traded_quantity', 'quantity').replace('trade_timestamp', 'trade_time').replace('trade_quantity', 'quantity').replace('tradingsymbol',
                                                                                                                                  'trading_symbol').replace(
            'last_price', 'last_trade_price').replace('trade_price', 'average_sell_price')

        # convert string to dict to List of Dict
        tempList = []
        if '[]' not in responseMessage:
            if responseMessageLenMoreThanOneFlag:
                responseMessage = responseMessage.replace("'", "\"").replace("False", "\"False\"").replace("True", "\"True\"")
                responseMessage = json.loads(responseMessage)
            else:
                responseMessage = responseMessage.replace("'", "\"").replace("[{", "{").replace("}]", "}").replace("False", "\"False\"").replace("True",
                                                                                                                                                 "\"True\"")
                responseMessage = json.loads(responseMessage)
                tempList.append(responseMessage)
                responseMessage = tempList
        else:
            responseMessage = []
        # responseMessage["data"]
        if responseMessage == []:
            return book_dict

        responseMessage = [x for x in responseMessage if (x['status'] == 'PENDING' and x['exchange'] == 'NSE_FO' and x['error_reason'] == '')]
        OrderBookAPIData = responseMessage
        Norders = 0

        for order_data in OrderBookAPIData:
            Norders = Norders + 1
            if order_data['option_type'] == 'CE':
                book_dict['CSL'] = str(int(float(order_data.get('strike_price'))))
                # book_dict['clientId'] = str(order_data.get('placed_by'))
                open_order_call = str(order_data['trading_symbol']) + str(order_data['expiry_date']) + str(order_data['strike_price'][:-3]) + str(
                    order_data['option_type'])
                book_dict['CSLP'] = str(open_order_call) + " : " + str(order_data['total_quantity']) + " : " + str(
                    order_data.get('order_price')) + '/' + str(order_data.get('trigger_price'))

            if order_data['option_type'] == 'PE':
                # # print("inside pe")
                book_dict['PSL'] = str(int(float(order_data.get('strike_price'))))
                # book_dict['clientId'] = str(order_data.get('placed_by'))
                open_order_put = str(order_data['trading_symbol']) + str(order_data['expiry_date']) + str(order_data['strike_price'][:-3]) + str(
                    order_data['option_type'])

                book_dict['PSLP'] = str(open_order_put) + " : " + str(order_data['total_quantity']) + " : " + str(
                    order_data.get('order_price')) + '/' + str(order_data.get('trigger_price'))

        book_dict['NoSL'] = str(Norders)

        book_dict['OpenSl'] = book_dict['CSLP'] + "||" + book_dict['PSLP']
        # return
        book_dict = self.markCellInRedAsPerRule(book_dict)
        return book_dict

    def get_available_fund(self):
        book_dict = {}
        book_dict['apiClientId'] = self.apiClientId
        book_dict['AF'] = "None"

        available_fund_Url = "https://jri4df7kaa.execute-api.ap-south-1.amazonaws.com/prod/interactive/authentication/v1/user/balance"

        response = requests.get(available_fund_Url, headers=self.headers)
        response.close()
        if response == []:
            return book_dict

        responseStatusCode = response.status_code
        responseMessage = response.json()

        if responseStatusCode != 200:
            return book_dict

        book_dict['AF'] = str(round(float(responseMessage['data']['equity']['net_available']), 2))
        # return
        book_dict = self.markCellInRedAsPerRule(book_dict)
        return book_dict

    def markCellInRedAsPerRule(self, book_dict):
        if 'PQ' in book_dict.keys() and 'CQ' in book_dict.keys():
            if int(book_dict['PQ']) != int(book_dict['CQ']):
                book_dict['PQ'] = 'Y-' + str(book_dict['PQ'])
                book_dict['CQ'] = 'Y-' + str(book_dict['CQ'])

        if 'NoSL' in book_dict.keys():
            if str(self.strategy).lower() == "putiron":
                if str(book_dict['NoSL']) != '2':
                    book_dict['NoSL'] = 'R-' + str(book_dict['NoSL'])
            else:
                if str(book_dict['NoSL']) != '2':
                    book_dict['NoSL'] = 'R-' + str(book_dict['NoSL'])

        if 'NOP' in book_dict.keys():
            if str(self.strategy).lower() == "putiron":
                if str(book_dict['NOP']) != '3':
                    book_dict['NOP'] = 'R-' + str(book_dict['NOP'])
            else:
                if str(book_dict['NOP']) != '2':
                    book_dict['NOP'] = 'R-' + str(book_dict['NOP'])

        if 'CP' in book_dict.keys() and 'PP' in book_dict.keys() and 'PP_B' in book_dict.keys():
            if str(book_dict['CP']) == 'None' or str(book_dict['CP']) == '':
                book_dict['CP'] = 'R-' + str(book_dict['CP'])
            if str(book_dict['PP']) == 'None' or str(book_dict['PP']) == '':
                book_dict['PP'] = 'R-' + str(book_dict['PP'])
            if str(self.strategy).lower() == "putiron":
                if str(book_dict['PP_B']) == 'None' or str(book_dict['PP_B']) == '':
                    book_dict['PP_B'] = 'R-' + str(book_dict['PP_B'])

        if 'CSL' in book_dict.keys() and 'PSL' in book_dict.keys() and 'CSLP' in book_dict.keys() and 'PSLP' in book_dict.keys():
            if str(book_dict['CSL']) == 'None' or str(book_dict['CSL']) == '':
                book_dict['CSL'] = 'R-' + str(book_dict['CSL'])
            if str(book_dict['PSL']) == 'None' or str(book_dict['PSL']) == '':
                book_dict['PSL'] = 'R-' + str(book_dict['PSL'])
            if str(book_dict['CSLP']) == 'None' or str(book_dict['CSLP']) == '':
                book_dict['CSLP'] = 'R-' + str(book_dict['CSLP'])
            if str(book_dict['PSLP']) == 'None' or str(book_dict['PSLP']) == '':
                book_dict['PSLP'] = 'R-' + str(book_dict['PSLP'])

        # csl_per = ''
        # try:
        #     csl_val = book_dict['CSLP']
        #     csl = csl_val.split('/')
        #     csl1 = csl[1]
        #     csl_per = float(csl1) * 0.75
        # except:
        #     pass
        # if csl_per != '':
        #     if float(book_dict['CLP']) > float(csl_per):
        #         book_dict['CAP'] = 'R-' + str(book_dict['CAP'])
        #
        # psl_per = ''
        # try:
        #     psl_val = book_dict['PSLP']
        #     psl = psl_val.split('/')
        #     psl1 = psl[1]
        #     psl_per = float(psl1) * 0.75
        # except:
        #     pass
        #
        # if psl_per != '':
        #     if float(book_dict['PLP']) > float(psl_per):
        #         book_dict['PAP'] = 'R-' + str(book_dict['PAP'])
        if 'AF' in book_dict.keys():
            if book_dict['AF'] != "None":
                if int(float(book_dict['AF'])) < 0:
                    book_dict['AF'] = "R-" + book_dict['AF']

        return book_dict
    # def run(self):
    #     try:
    #         self.get_positionBook_data()
    #         self.order_book_data()  # order book
    #         self.get_available_fund()
    #         self.markCellInRedAsPerRule()
    #     except:
    #         pass
    #     return book_dict  # merged_data_dict

# print(Indira_API_RESPONSE("N7665","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJJZCI6OTA5MDkwLCJ1c2VyaWQiOjkwOTA5MCwidGVuYW50aWQiOjkwOTA5MCwibWVtYmVySW5mbyI6eyJ0ZW5hbnRJZCI6IjM4NSIsImdyb3VwSWQiOiJITyIsInVzZXJJZCI6IkFUMjIiLCJ0ZW1wbGF0ZUlkIjoiV0FWRSIsInVkSWQiOiIiLCJvY1Rva2VuIjoiMHgwMTlBRUYyNjA0N0QxMEFCNzgwM0VDRTAzNUI1RkUiLCJ1c2VyQ29kZSI6Ik5aT0pWIiwiZ3JvdXBDb2RlIjoiQUFBQUEiLCJhcGlrZXlEYXRhIjp7IlByb2R1Y3RTb3VyY2UiOiJXRUJBUEkiLCJzUGFydG5lckFwcElkIjoiMDFGMDBGIiwiQjJDIjoiWSIsIlB1Ymxpc2hlck5hbWUiOiJJbmRpcmEgU2VjdXJpdGllcyBQdnQgTHRkIC0gQjJDIiwic1B1Ymxpc2hlckNvZGUiOiJjdSIsIkN1c3RvbWVySWQiOiIzODUiLCJzQXBwbGljYXRpb25Ub2tlbiI6IkluZGlyYVNlY3VyaXRpZXNCMkMxMDcwNDY0ZGVlZiIsInVzZXJJZCI6IkFUMjIiLCJCcm9rZXJOYW1lIjoiSW5kaXJhIFNlY3VyaXRpZXMgUHZ0IEx0ZCIsImV4cCI6OTEyNTU5MjQ4MCwiaWF0IjoxNjYwNjMyNTA5fSwic291cmNlIjoiTU9CSUxFQVBJIn0sImV4cCI6MTY3MzU0ODE5OSwiaWF0IjoxNjczNDkxODAzfQ.YP73O6oSbf9ZS5sZfXAQHHFpRsSsZB91gaaGhxUHLsk"
#                           ,"putIron","Algoptions","BANKNIFTY","Indothai").get_positionBook_data())
# apiClientId, access_token, strategy, name, trading_symbol, Broker
