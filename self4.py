# -*- coding: utf-8 -*-
"""

생존형퀀트의 경제적자유. https://blog.naver.com/starfox119

"""

 #########################################################################
 # 업비트 로그인
 #########################################################################
import pyupbit						
import time	
access = "4bAGnrGccIFCZ1nZyhgNGx7itfJNBmomDtF61i69"							    # 엑세스 키 입력					
secret = "ZzxALJxXMf71E4pmMFdSWxMuJo4nTx0hBIzJ0fFU"	
upbit = pyupbit.Upbit(access, secret)                                           # 로그인 

#########################################################################
# 텔레그램 연결
#########################################################################
import telegram                                                                 
tlgm_token = '1770499141:AAFGgivsAkLTLKnZU2bQb8cDxcNC1eCUr_o'                   
tlgm_id = '1146999309'                                                          
bot = telegram.Bot(token = tlgm_token)                                          
updates = bot.getUpdates()                                                      
bot.sendMessage(chat_id = tlgm_id, text = 'Crypto Commando')     
#########################################################################
# 변수 초기값
#########################################################################
abp = 0                                                                                    
current_price = 0
margin = 0
weight = 20000                                                                      

#########################################################################
# 전체 코인 티커 조회
#########################################################################
tickers = pyupbit.get_tickers(fiat = "KRW")

#########################################################################
# 종류별 코인 목록
#########################################################################
wave = []

#########################################################################
# 반복문 시작
#########################################################################
while True : 
    
    for ticker in tickers :
        
        abp = upbit.get_avg_buy_price(ticker)
        current_price = pyupbit.get_current_price(ticker)
        ticker_balance = upbit.get_balance(ticker)
        krw_balance = upbit.get_balance("KRW")

    if ticker_balance > 0 :
        margin = (current_price - abp)/abp

    if abp == 0 :
        margin = 0

        #########################################################################
        # 데이타 추출1. 
        #########################################################################
        ticker_df_m3 = pyupbit.get_ohlcv(ticker,"minute3")
        ticker_df_m3['amount'] = ticker_df_m3['volume'] * ticker_df_m3['close']
        o_m3 = ticker_df_m3['open']
        h_m3 = ticker_df_m3['high']   
        l_m3 = ticker_df_m3['low']                                   
        c_m3 = ticker_df_m3['close']                                                    
        v_m3 = ticker_df_m3['volume']
        a_m3 = ticker_df_m3['amount']                  
        
        volume_check_range = a_m3.iloc[190:199]
        volume_check = int(volume_check_range.sum())

        o_m3_199 = o_m3[199]        
        h_m3_199 = h_m3[199]
        l_m3_199 = l_m3[199]
        c_m3_199 = c_m3[199]

        m3_high_180_199 = h_m3.iloc[180:199]                                     
        m3_high_180_198 = h_m3.iloc[180:198]
        m3_high_180_197 = h_m3.iloc[180:197]

        m3_max_high_180_199 = m3_high_180_199.max(axis = 0)                     
        m3_max_high_180_198 = m3_high_180_198.max(axis = 0)
        m3_max_high_180_197 = m3_high_180_197.max(axis = 0)                      

        m3_low_180_199 = l_m3.iloc[180:199]
        m3_low_180_198 = l_m3.iloc[180:198]
        m3_min_low_180_199 = m3_low_180_199.min(axis = 0)
        m3_min_low_180_198 = m3_low_180_198.min(axis = 0)

        window5_m3 = c_m3.rolling(5)                                          
        ma5_m3 = window5_m3.mean()
        ma5_m3_199 = ma5_m3[199]
        ma5_m3_198 = ma5_m3[198]
        ma5_m3_197 = ma5_m3[197]
        ma5_m3_trend_199 = ma5_m3_199 - ma5_m3_198
        ma5_m3_trend_198 = ma5_m3_198 - ma5_m3_197
                                        
        window20_m3 = c_m3.rolling(20)                                          
        ma20_m3 = window20_m3.mean()
        ma20_m3_199 = ma20_m3[199]
        ma20_m3_198 = ma20_m3[198]
        ma20_m3_197 = ma20_m3[197]
        ma20_m3_trend_199 = ma20_m3_199 - ma20_m3_198
        ma20_m3_trend_198 = ma20_m3_198 - ma20_m3_197

        window60_m3 = c_m3.rolling(60)                                          
        ma60_m3 = window60_m3.mean()
        ma60_m3_199 = ma60_m3[199]
        ma60_m3_198 = ma60_m3[198]
        ma60_m3_197 = ma60_m3[197]
        ma60_m3_trend_199 = ma60_m3_199 - ma60_m3_198
        ma60_m3_trend_198 = ma60_m3_198 - ma60_m3_197

        window120_m3 = c_m3.rolling(120)                                          
        ma120_m3 = window120_m3.mean()
        ma120_m3_199 = ma120_m3[199]
        ma120_m3_198 = ma120_m3[198]
        ma120_m3_197 = ma120_m3[197]
        ma120_m3_trend_199 = ma120_m3_199 - ma120_m3_198
        ma120_m3_trend_198 = ma120_m3_198 - ma120_m3_197

        std20_m3 = window20_m3.std()

        window3_std20_m3 = std20_m3.rolling(20)
        ma20_std20_m3 = window3_std20_m3.mean()

        ma20_std20_m3_198 = ma20_std20_m3[198]  
        ma20_std20_m3_197 = ma20_std20_m3[197]

        std20_m3_150_199 = std20_m3.iloc[150:199]

        std20_m3_150_199[48]
        std20_m3_150_199[47]

        std20_m3_max_150_199 = std20_m3_150_199.max(axis =0)
        std20_m3_min_150_199 = std20_m3_150_199.min(axis =0)

        std20_m3_199 = std20_m3[199]
        bu20_m3_199 = ma20_m3_199 + std20_m3_199 * 2
        bd20_m3_199 = ma20_m3_199 - std20_m3_199 * 2

       # 블린저 폭발력 비율
        bolinger_width = bu20_m3_199 - bd20_m3_199

        explosion_width = h_m3_199 - bu20_m3_199
        explosion_width_current = current_price - bu20_m3_199

        drop_width = l_m3_199 - bd20_m3_199
        drop_width_current = current_price - bd20_m3_199

        if h_m3_199 > bu20_m3_199 :
            explosion_rate = explosion_width / bolinger_width
        else :
            explosion_rate = 0

        if current_price > bu20_m3_199 :
            explosion_rate_current = explosion_width_current / bolinger_width
        else :
            explosion_rate_current = 0

        if l_m3_199 < bd20_m3_199 :
            drop_rate = drop_width / bolinger_width
        else :
            drop_rate = 0
    
        if current_price < bd20_m3_199 :
            drop_rate_current = drop_width_current / bolinger_width
        else :
            drop_rate_current = 0
                                                      
                                                 
        #########################################################################
        # 출력 지점
        #########################################################################        
        #print(time.strftime('%m-%d %H:%M:%S'),ticker)
        print(time.strftime('%m-%d %H:%M:%S'),ticker.ljust(10),"MG:",str(round(margin,4)).ljust(7),"BL:",round(ticker_balance * current_price))      
        
        # 반등구간 진입
        if ticker_balance * current_price < 5000 :
            if m3_min_low_180_198 == m3_min_low_180_199 :
                if ma5_m3_trend_199 > 0 :
                    bot.sendMessage(chat_id = tlgm_id, text = ticker+' Operatino Started')
                    buy_record0 = upbit.buy_market_order(ticker, weight)
                    print(ticker, " Operatino Started")        

       # 수익 실현, 분할매도
        if ticker_balance * current_price > 5000 :
            if margin < profit_cut :
                if (ticker_balance * current_price)/2 > 6000 :
                    bot.sendMessage(chat_id = tlgm_id, text = ticker+'Operatino Started')
                    bot.sendMessage(chat_id = tlgm_id, text = abp)
                    bot.sendMessage(chat_id = tlgm_id, text = margin)
                    sell_record0 = upbit.sell_market_order(ticker, ticker_balance / 2)
                    print(ticker, 'Operatino Started')

        current_time = time.strftime("%H:%M")
        start_time = "23:55"
        end_time = "23:59"
        
        if (current_time >= start_time) and (current_time <= end_time) :
            dismissed = 1
        else :
            dismissed = 0

        if dismissed == 1 :
            if ticker_balance *current_price > 500 :
                sell_record0 = upbit.sell_market_order(ticker, ticker_balance)

        if ticker in wave :
           print(ticker, " wave")

        else :    
           if ticker_balance * current_price < 5000 and krw_balance > weight :
               if ma5_m3_trend_198 > 0 and ma20_m3_trend_198 > 0 :
                   if ma5_m3[199] > ma20_m3[199] and ma5_m3[198] > ma20_m3[198] :
                       if current_price > max_close_179_198 and current_price < max_high_179_198 :
                           if (current_price - close_price[195])/close_price[195] < 0.15 :
                               if (high_price[198] - current_price)/high_price[198] < 0.03 :
                                   bot.sendMessage(chat_id = tlgm_id, text = ticker+' Operatino Started')
                                   buy_record0 = upbit.buy_market_order(ticker, weight)
                                   print(ticker, " Operatino Started")          

       # 손절. 제네시스 캔들 저점 하향돌파
        if current_price < ma5_m3[199] and current_price < ma20_m3[199] :
            if c_m3[198] < ma5_m3[198] and c_m3[198] < ma20_m3[198] :
               if ticker in wave :
                   wave.remove(ticker)

               if ticker_balance * current_price > 5000 :
                    bot.sendMessage(chat_id = tlgm_id, text = ticker+' Operation Finished')
                    bot.sendMessage(chat_id = tlgm_id, text = abp)
                    bot.sendMessage(chat_id = tlgm_id, text = margin)
                    sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                    print(ticker, ' Operation Finished')

               if margin < 0.015 :
                    if ticker in wave :
                       bot.sendMessage(chat_id = tlgm_id, text = ticker+' wave')
                       bot.sendMessage(chat_id = tlgm_id, text = abp)
                       bot.sendMessage(chat_id = tlgm_id, text = margin)
                       sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                       print(ticker, ' wave')        
    
        #########################################################################
        # 0.1초 간격으로 티커별 현황조회
        #########################################################################          
        time.sleep(0.1)
        