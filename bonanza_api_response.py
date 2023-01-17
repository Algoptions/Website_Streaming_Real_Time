# import views

import requests

import json
import ast
# from Management.real_time_data.writeLogs import logsWrite
from datetime import date
class Bonanza_API_RESPONSE:
    def __init__(self,apiClientId, accessToken, strategy, name, trading_symbol, broker):
        execution_date = date.today()
        # logs = logsWrite(str(execution_date) + "_bonanza_api_response_")
        # self.logger = logs.get_logger('_Bonanza_API_RESPONSE_')
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
            'Authorization': '{accessToken}'.format(accessToken=accessToken)
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

        Position_requestUrl = "https://trading.bigul.co/interactive/portfolio/positions?dayOrNet=NetWise&clientID="+self.apiClientId

        apiClientId =self.apiClientId

        response = requests.get(Position_requestUrl, headers=self.headers, verify=False)
        responseStatusCode = response.status_code
        responseMessage = response.json()
        responseMessage = responseMessage['result']
        if responseStatusCode != 200 :
            return book_dict



        # convert dict to string and manipulate
        responseMessage = str(responseMessage).replace('TradingSymbol', 'trading_symbol').replace('SellAveragePrice', 'average_sell_price').replace('Quantity',
                                                                                                                                                    'quantity').replace(
            'ltp', 'last_trade_price').replace('ExchangeInstrumentId', 'instrument_token').replace('order_id', 'orderId').replace('order_timestamp',
                                                                                                                                  'trade_time').replace(
            'traded_quantity', 'quantity').replace('trade_timestamp', 'trade_time').replace('trade_quantity', 'quantity').replace('ExchangeSegment',
                                                                                                                                  'exchange').replace(
            'last_price', 'last_trade_price').replace('trade_price', 'average_sell_price')

        # convert string to dict to List of Dict
        tempList = []
        responseMessage = ast.literal_eval(responseMessage)
        tempList.append(responseMessage)
        responseMessage = tempList[0]
        responseMessage = [x for x in responseMessage['positionList'] if (x['exchange'] == 'NSEFO' and int(x['quantity']) != 0)]

        PositionBookAPIData = responseMessage

        self.Npositions = 0
        for position_data in PositionBookAPIData:
            self.Npositions = self.Npositions + 1
            if position_data['trading_symbol'].split(" ")[2].lower() == 'ce' and int(position_data['quantity']) < 0:
                stringcp = int(position_data['trading_symbol'].split(" ")[3])
                book_dict['CP'] = str(stringcp)
                book_dict['CQ'] = str(int(position_data.get('quantity')) * (- 1) )
                book_dict['CAP'] = str(round(float(position_data.get('average_sell_price')), 2))
                open_pos_call = str(position_data['trading_symbol']).replace(" ", "")


            elif (position_data['trading_symbol'].split(" ")[2].lower() == 'pe' and int(position_data['quantity']) < 0):
                stringpp = int(position_data['trading_symbol'].split(" ")[3])
                book_dict['PP'] = str(stringpp)
                book_dict['PQ'] = str(int(position_data.get('quantity')) * (- 1) )
                book_dict['PAP'] = str(round(float(position_data.get('average_sell_price')), 2))
                open_pos_put = str(position_data['trading_symbol']).replace(" ", "")


            elif (position_data['trading_symbol'].split(" ")[2].lower() == 'pe' and int(position_data['quantity']) > 0 ):
                stringpp_B = int(position_data['trading_symbol'].split(" ")[3])
                book_dict['PP_B'] = str(stringpp_B)
                book_dict['PQ_B'] = str(int(position_data.get('quantity')))
                book_dict['PAP_B'] = str(position_data.get('BuyAveragePrice'))
                open_pos_put_buy = str(position_data['trading_symbol']).replace(" ", "")



        book_dict['NOP'] = str(self.Npositions)
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
        Order_requestUrl = "https://trading.bigul.co/interactive/orders?clientID="+self.apiClientId



        response = requests.get(Order_requestUrl, headers=self.headers, verify=False)
        responseStatusCode = response.status_code
        responseMessage = response.json()
        responseMessage =  responseMessage ['result']
        if responseStatusCode == 200 :
            if responseMessage == []:
                return book_dict
        # # IMP NOTE:INDRA SECURITIES SENDS 404 for not having positions
        else:
            return book_dict
        # responseMessageLenMoreThanOneFlag = False
        # if len(responseMessage) > 0:
        #     responseMessageLenMoreThanOneFlag = True

        # remove none to 'none'
        dict_str = json.dumps(responseMessage)
        responseMessage = json.loads(dict_str, object_pairs_hook= self.dict_clean)

        responseMessageLenMoreThanOneFlag = False
        if len(responseMessage) > 0:
            responseMessageLenMoreThanOneFlag = True

        # remove none to 'none'
        dict_str = json.dumps(responseMessage)
        responseMessage = json.loads(dict_str, object_pairs_hook=self.dict_clean)

        # convert dict to string and manipulate
        responseMessage = str(responseMessage).replace('TradingSymbol', 'trading_symbol').replace('avg_sell_price', 'average_sell_price').replace('OrderQuantity',
                                                                                                                                                  'quantity').replace(
            'ltp', 'last_trade_price').replace('CancelRejectReason', 'error_reason').replace('ExchangeInstrumentID', 'instrument_token').replace('AppOrderID', 'orderId').replace('OrderGeneratedDateTime',
                                                                                                                                                                                  'trade_time').replace(
            'traded_quantity', 'quantity').replace('ExchangeTransactTime', 'trade_time').replace('trade_quantity', 'quantity').replace(
            'last_price', 'last_trade_price').replace('OrderAverageTradedPrice', 'average_sell_price').replace('OrderStatus', 'status').replace('ExchangeSegment', 'exchange')


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
        new_responseMessage = []
        for responseMessage_dict in responseMessage:
            if str(responseMessage_dict['status']).lower() == 'new':
                new_responseMessage.append(responseMessage_dict)

        OrderBookAPIData = new_responseMessage

        self.NoSL = 0


        for order_data in OrderBookAPIData:
            self.NoSL = self.NoSL + 1
            if order_data['trading_symbol'].split(" ")[2] == 'CE':

                book_dict['CSL'] = str(order_data['trading_symbol'].split(" ")[3])
                # orderbookApiDataDict['clientId'] = str(order_data.get('placed_by'))
                open_pos_call = str(order_data['trading_symbol']).replace(" ", "")
                book_dict['CSLP'] = str(open_pos_call)+ " : " + str(order_data['quantity']) + " : " +str(order_data.get('OrderPrice')) + '/' + str(order_data.get('OrderStopPrice'))


            elif order_data['trading_symbol'].split(" ")[2] == 'PE':
                # # print("inside pe")
                book_dict['PSL'] = str(order_data['trading_symbol'].split(" ")[3])
                # orderbookApiDataDict['clientId'] = str(order_data.get('placed_by'))
                open_pos_put = str(order_data['trading_symbol']).replace(" ", "")
                book_dict['PSLP'] = str(open_pos_put)+ " : " + str(order_data['quantity']) + " : " +str(order_data.get('OrderPrice')) + '/' + str(order_data.get('OrderStopPrice'))


        book_dict['NoSL'] = str(self.NoSL)


        book_dict["OpenSl"] = book_dict['CSLP'] + "||" + book_dict['PSLP']
        # return
        book_dict = self.markCellInRedAsPerRule(book_dict)
        return book_dict
    def get_available_fund(self):
        book_dict = {}
        book_dict['apiClientId'] = self.apiClientId
        book_dict['AF'] = "None"

        availableFundUrl = "https://trading.bigul.co/interactive/user/balance?clientID=*****"
        response = requests.get(availableFundUrl, headers=self.headers, verify=False)
        responseStatusCode = response.status_code
        responseMessage = response.json()
        if responseStatusCode != 200:
            return book_dict
        book_dict['AF'] = str(round(float(responseMessage["result"]["BalanceList"][0]['limitObject']['RMSSubLimits']['netMarginAvailable']), 2))
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
        #     psl_val = book_dict['PSLP']c
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
    #         self.order_book_data() #order book
    #         self.get_available_fund()
    #         self.markCellInRedAsPerRule()
    #     except:
    #         pass
    #     return book_dict #merged_data_dict



# a = Bonanza_API_RESPONSE("*****","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiJTWU1QMl9FMjgxQkU3QUZFMjdERTJBRjQxODE0IiwicHVibGljS2V5IjoiZTI4MWJlN2FmZT
# I3ZGUyYWY0MTgxNCIsImlhdCI6MTY3MzgzNTkwMiwiZXhwIjoxNjczOTIyMzAyfQ.7POLMNuN3bB3DLPQtY2XsjddrTsLMoguvN6JH58Ik18","putIron","BonanzaPRO2","BANKNIFTY","Symphony")
# print(a.order_book_data())

# self,apiClientId, accessToken, strategy, name, trading_symbol, broker):