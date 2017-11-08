#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#################################################################
## Auteur: Hervé-Gaël KOUAMO
## Date: 07/11/2017
## Version: 1.0
## Description: Script qui parse le JSON de coinmarketcap
## Exécution : MarketPrevision.py LEVEL CRYPTO
#################################################################
import urllib2, json
from urllib2 import urlopen
from json import load
import unicodedata
from sys import argv
from colored import fore, back, style

# unicodedata.normalize('NFKD', title).encode('ascii','ignore')

# response = urllib2.urlopen('https://api.instagram.com/v1/tags/pizza/media/XXXXXX')
# data = json.load(response)   


try:
    LEVEL = argv[1]
except IndexError as e:
    LEVEL = 2

try:
    NBC = argv[2]
except IndexError as e:
    NBC = 100


ALL = "http://api.coinmarketcap.com/v1/ticker/?convert=DOLLAR"
TOP50 = "http://api.coinmarketcap.com/v1/ticker/?convert=DOLLAR&limit=%s" %NBC

Cryptodict = dict()

# Seuil Achat Vente 7 Jour
SV_7D = 15
SA_7D = -20
SV_7D_R = 20  # Risque
SA_7D_R = -15 # Risque 

# Seuil Achat Vente 24h
SV_24H = -3
SA_24H = 3
SV_24H_R = -2 # Risque
SA_24H_R = 2 # Risque

# Seuil Achat Vente 1h
SV_1H = -0.5
SA_1H = 0.5


class JsonMarket(object):
    """docstring for JsonMarket"""
    def __init__(self, url):
        super(JsonMarket, self).__init__()
        self.url = url
        self.CryptodictBuy = dict()
        self.CryptodictSell = dict()

    def getDataJson(self):
        response = urlopen(self.url)
        data = load(response)
        return data

    def convertJsonDict(self,DataJson):
        print " ******* CRYPTO PREVISION - NORMAL ********* "
        print " *********************************************"
        for data in DataJson:
            name = unicodedata.normalize('NFKD', data['id']).encode('ascii','ignore')
            symbol = unicodedata.normalize('NFKD', data['symbol']).encode('ascii','ignore')
            price_usd = unicodedata.normalize('NFKD', data['price_usd']).encode('ascii','ignore')
            percent_change_1h = unicodedata.normalize('NFKD', data['percent_change_1h'] ).encode('ascii','ignore')
            percent_change_24h =  unicodedata.normalize('NFKD', data['percent_change_24h'] ).encode('ascii','ignore')
            try:
                percent_change_7d = unicodedata.normalize('NFKD', data['percent_change_7d'] ).encode('ascii','ignore')
            except TypeError as e:
                percent_change_7d = 1
            volume_24h = unicodedata.normalize('NFKD', data['24h_volume_dollar'] ).encode('ascii','ignore')

            Cryptodict[name] = [symbol, price_usd, percent_change_1h, percent_change_24h, percent_change_7d, volume_24h]

            ##### Algorithme de détermination d'achat/vente #####
            if (float(percent_change_7d) < SA_7D and float(percent_change_24h) > SA_24H):
                # print "Buy"
                # print name, Cryptodict[name]
                self.CryptodictBuy[name] = [symbol, price_usd, percent_change_1h, percent_change_24h, percent_change_7d, volume_24h]
            elif (float(percent_change_7d) > SV_7D and float(percent_change_24h) < SV_24H):
                # print "Sell"
                # print name, Cryptodict[name]
                self.CryptodictSell[name] = [symbol, price_usd, percent_change_1h, percent_change_24h, percent_change_7d, volume_24h]

        return Cryptodict, self.CryptodictSell, self.CryptodictBuy

    def convertJsonDict_risky(self,DataJson):
        print " ******* CRYPTO PREVISION - LITTLE RISKY ********* "
        print " **************************************************"
        for data in DataJson:
            name = unicodedata.normalize('NFKD', data['id']).encode('ascii','ignore')
            symbol = unicodedata.normalize('NFKD', data['symbol']).encode('ascii','ignore')
            price_usd = unicodedata.normalize('NFKD', data['price_usd']).encode('ascii','ignore')
            percent_change_1h = unicodedata.normalize('NFKD', data['percent_change_1h'] ).encode('ascii','ignore')
            percent_change_24h =  unicodedata.normalize('NFKD', data['percent_change_24h'] ).encode('ascii','ignore')
            try:
                percent_change_7d = unicodedata.normalize('NFKD', data['percent_change_7d'] ).encode('ascii','ignore')
            except TypeError as e:
                percent_change_7d = 1
            volume_24h = unicodedata.normalize('NFKD', data['24h_volume_dollar'] ).encode('ascii','ignore')

            Cryptodict[name] = [symbol, price_usd, percent_change_1h, percent_change_24h, percent_change_7d, volume_24h]

            ##### Algorithme de détermination d'achat/vente #####
            if (float(percent_change_7d) < SA_7D_R and float(percent_change_24h) > SA_24H_R):
                # print "Buy"
                # print name, Cryptodict[name]
                self.CryptodictBuy[name] = [symbol, price_usd, percent_change_1h, percent_change_24h, percent_change_7d, volume_24h]
            elif (float(percent_change_7d) > SV_7D_R and float(percent_change_24h) > SV_24H_R):
                # print "Sell"
                # print name, Cryptodict[name]
                self.CryptodictSell[name] = [symbol, price_usd, percent_change_1h, percent_change_24h, percent_change_7d, volume_24h]

        return Cryptodict, self.CryptodictSell, self.CryptodictBuy


    def convertJsonDict_norisky(self,DataJson):
        print " ******* CRYPTO PREVISION - NO RISK ********* "
        print " *********************************************"
        for data in DataJson:
            name = unicodedata.normalize('NFKD', data['id']).encode('ascii','ignore')
            symbol = unicodedata.normalize('NFKD', data['symbol']).encode('ascii','ignore')
            price_usd = unicodedata.normalize('NFKD', data['price_usd']).encode('ascii','ignore')
            percent_change_1h = unicodedata.normalize('NFKD', data['percent_change_1h'] ).encode('ascii','ignore')
            percent_change_24h =  unicodedata.normalize('NFKD', data['percent_change_24h'] ).encode('ascii','ignore')
            try:
                percent_change_7d = unicodedata.normalize('NFKD', data['percent_change_7d'] ).encode('ascii','ignore')
            except TypeError as e:
                percent_change_7d = 1
            volume_24h = unicodedata.normalize('NFKD', data['24h_volume_dollar'] ).encode('ascii','ignore')

            Cryptodict[name] = [symbol, price_usd, percent_change_1h, percent_change_24h, percent_change_7d, volume_24h]

            ##### Algorithme de détermination d'achat/vente #####
            if (float(percent_change_7d) < SA_7D and float(percent_change_24h) > SA_24H and float(percent_change_1h) > SA_1H):
                # print "Buy"
                # print name, Cryptodict[name]
                self.CryptodictBuy[name] = [symbol, price_usd, percent_change_1h, percent_change_24h, percent_change_7d, volume_24h]
            elif (float(percent_change_7d) > SV_7D and float(percent_change_24h) < SV_24H and float(percent_change_1h) < SV_1H):
                # print "Sell"
                # print name, Cryptodict[name]
                self.CryptodictSell[name] = [symbol, price_usd, percent_change_1h, percent_change_24h, percent_change_7d, volume_24h]

        return Cryptodict, self.CryptodictSell, self.CryptodictBuy

    def printResultDict(self, DataDict, color):
        print color
        for key, value in DataDict.iteritems():
            print "[[%s]]" %(key)
            #print "[[%s]] - %s" %(key,value)



if __name__ == '__main__':

    AllCrypto = JsonMarket(TOP50)
    print fore.LIGHT_YELLOW
    print """This Program is developed By KKhg.
    The program Gives prevision of CryptoCurrency Market.
    It Tell you when you buy and when you sell

    If your are interested Send me an email at : herve.esir@gmail.com
    """
    DataJson = AllCrypto.getDataJson()
    if int(LEVEL) == 0:
        print "Prévision With No Risk - LEVEL:%s" %LEVEL
        DataDict, CryptodictSell, CryptodictBuy = AllCrypto.convertJsonDict_norisky(DataJson)
    elif int(LEVEL) == 1:
        print "Normal prevision - LEVEL:%s" %LEVEL
        DataDict, CryptodictSell, CryptodictBuy = AllCrypto.convertJsonDict(DataJson)
    elif int(LEVEL) == 2:
        print "Prevision With litle Risk - LEVEL:%s" %LEVEL
        DataDict, CryptodictSell, CryptodictBuy = AllCrypto.convertJsonDict_risky(DataJson)
    else:
        print "Normal prevision - LEVEL:%s" %LEVEL
        DataDict, CryptodictSell, CryptodictBuy = AllCrypto.convertJsonDict(DataJson)


    print fore.LIGHT_GREEN
    print " ******* CRYPTO TO BUY - CRYPTO A ACHETER ********* "
    AllCrypto.printResultDict(CryptodictBuy,fore.LIGHT_GREEN)

    print fore.LIGHT_RED
    print " ******* CRYPTO TO SELL - CRYPTO A VENDRE  ********* "
    AllCrypto.printResultDict(CryptodictSell,fore.LIGHT_RED)





