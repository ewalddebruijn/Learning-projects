# -*- coding: utf-8 -*-
from datetime import timedelta, date, timezone
from datetime import datetime as dt
import json
from matplotlib import style
import matplotlib.pyplot as plt
import os
import pandas as pd
import pickle
import requests
from collections import OrderedDict, Counter
import matplotlib.dates as mdates

class ccwrapper():
    
    def __init__(self, cryptos, timeframe='hour'):
        """
        For all the given names in cryptos, this class calls on the crypto-
        compare API and fetches data for that coin from its inception until
        the current date. 
        
        The time difference between now and the 3-1-2009 is split up into 
        smaller packets. The crypto compare API only returns 2000 results, so 
        every 2000 units we have to initiate a new API call. We call until
        the oldest date in the site, which is 03-01-2009 for BTC. 
        
        We save the data of both steps continiously, so with each step, we
        check earlier calls. 
        
        @cryptos: which names we are interested in. Can only process 
        abbreviated names, such as BTC, ETC or LTC
        @timeframe: currently only accepts hour, but later minute and daily
        will be added
        """
        if timeframe == 'hour':
            self.timeframe = timeframe
            self.interval = 2000*60*60
            self.cryptos = {c:self.callAPI(c) for c in cryptos}
        print(self.cryptos)
        
    def callAPI(self, c):
        if '{}-USD.md'.format(c) not in os.listdir():
            dframes = []
            datecalls = self.timediv('03/01/2009 0:00',  
                                     dt.now().strftime('%d/%m/%Y %H:%M'))
        else:
            dframes = [pd.read_pickle('{}-USD.md'.format(c))]
            datecalls = self.timediv(dframes[0].tail(1).index[0], 
                                     dt.now().strftime('%d/%m/%Y %H:%M'))
    
        for d in datecalls:  
            USD_html = 'https://min-api.cryptocompare.com/data/histohour?aggregate=1&extraParams=CryptoCompare&fsym={}&limit=2000&tryConversion=false&tsym=USD&toTs={}'.format(c, d)
            response = requests.get(USD_html).json()
            for n, x in enumerate(response['Data']):
                response['Data'][n]['time'] = dt.fromtimestamp(response['Data'][n]['time']).strftime('%d/%m/%Y %H:%M')
            if response['Data'] != []:
                df = pd.DataFrame(response['Data'])
                df = df.set_index('time')          
                dframes.append(df)
        
        if len(dframes) > 0:
            result = pd.concat(dframes)
            result = result[~result.index.duplicated(keep='last')]
            result.to_pickle('{}-USD.md'.format(c))
        else:
            print('coin needs to be done by using BTC as a benchmark for price')
            result = []
        return result
            
    def timediv(self, start, end):
        start = int(dt.strptime(start, "%d/%m/%Y %H:%M").timestamp())
        end = int(dt.strptime(end, "%d/%m/%Y %H:%M").timestamp())
        
        return sorted([x for x in range(end, start, -self.interval)])

ccwrapper(['BTC', 'LTC', 'NEO', 'ETH', 'STRAT', 'IOTA'])
        
                