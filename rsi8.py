
# 업비트 API 로그인
import numpy as np
import pyupbit	
import webbrowser					
import time
import requests		
import pprint
import pandas as pd	
access = "4bAGnrGccIFCZ1nZyhgNGx7itfJNBmomDtF61i69"							    # 엑세스 키 입력					
secret = "ZzxALJxXMf71E4pmMFdSWxMuJo4nTx0hBIzJ0fFU"		
upbit = pyupbit.Upbit(access, secret)	

#########################################################################
# 텔레그램 연결
#########################################################################
import telegram                                                                 
tlgm_token = '1770499141:AAGa1uvZnZs1nbgDGpxNuBhxZXaVr2jwf5Q'                    
tlgm_id = '1146999309'                                                          
bot = telegram.Bot(token = tlgm_token)                                          
updates = bot.getUpdates()                                                      
bot.sendMessage(chat_id = tlgm_id, text = '자동매매 시작') 

# 초기 세팅
tickers = pyupbit.get_tickers(fiat = "KRW")
#ticker = "KRW-ETH"   # 투자하고 싶은 코인의 티커 입력
total_weight = upbit.get_balance("KRW")  # 투자금액 설정

#########################################################################
# 종류별 코인 목록
#########################################################################
wave = []

# 실사용 중인 트리거
margin = 0
max_margin = 0	
previous_max_margin = 0
realized_profit = 0.004  # 익절값 설정
loss_cut_trigger = 0
realized_profit_amount = total_weight * 1/2    # 익절값 도달 시 익절 비중
loss_cut = 0
last_candle_color = 9
check_candle_color = 9
max_min_lp = 0
current_min_lp = 0
nlt = 0
pat = [ 100, 50, 0, 0, -20, -30, -10 ]
MAX_NUM_COIN = 2

#if __name__ == '__main__':

#    already_buy = {}
#    coin_noise = {}
#    coin_betting_ratio = {}
#    coin_investable = MAX_NUM_COIN



# 반복문 실행
while True:  
    
    for ticker in tickers :

    
        ticker_balance = upbit.get_balance(ticker)	
        krw_balance = upbit.get_balance("KRW")
        abp = upbit.get_avg_buy_price(ticker)
        current_price = pyupbit.get_current_price(ticker)
        
        if ticker_balance > 0 :
            margin = (current_price - abp)/abp

        if abp == 0 :
            margin = 0  
            
        #if ticker_balance > 0 :
            #margin = (current_price - abp)/abp
            
            

        #if abp == 0 :
            #margin = 0 

                        

    #########################################################################
    # 데이타 추출
    #########################################################################
        ticker_df = pyupbit.get_ohlcv(ticker, "1d",10)
        ticker_df['amount'] = ticker_df['volume'] * ticker_df['close']
        o_1d = ticker_df['open']           
        c_1d = ticker_df['close']                                                    
        h_1d = ticker_df['high']   
        l_1d = ticker_df['low']                                   
        c_1d = ticker_df['close']
        v_1d = ticker_df['volume']
        a_1d = ticker_df['amount']

            
        volume_check_range = a_1d.iloc[0:9]
        volume_check = int(volume_check_range.sum())                                                    

        o_1d_199 = o_1d[9]        
        h_1d_199 = h_1d[9]
        l_1d_199 = l_1d[9]
        c_1d_199 = c_1d[9]

        o_1d_198 = o_1d[8]        
        h_1d_198 = h_1d[8]
        l_1d_198 = l_1d[8]
        c_1d_198 = c_1d[8]        

        d_open_180_199 = o_1d.iloc[0:9]
        d_open_180_198 = o_1d.iloc[0:8]
        d_open_180_197 = o_1d.iloc[0:7]

        d_open_180_199 = d_open_180_199.max(axis = 0)                     
        d_open_180_198 = d_open_180_198.max(axis = 0)
        d_open_180_197 = d_open_180_197.max(axis = 0)                      

        d_close_180_199 = c_1d.iloc[0:9]
        d_close_180_198 = c_1d.iloc[0:8]

        d_open_close_180_199 = d_close_180_199.min(axis = 0)
        d_open_close_180_198 = d_close_180_198.min(axis = 0)

        ticker_df_m5 = pyupbit.get_ohlcv(ticker,"minute30")
        ticker_df_m5['amount'] = ticker_df_m5['volume'] * ticker_df_m5['close']
        o_m5 = ticker_df_m5['open']
        h_m5 = ticker_df_m5['high']   
        l_m5 = ticker_df_m5['low']                                   
        c_m5 = ticker_df_m5['close']                                                    
        v_m5 = ticker_df_m5['volume']
        a_m5 = ticker_df_m5['amount']                  
            
        volume_check_range = a_m5.iloc[190:199]
        volume_check = int(volume_check_range.sum())

        o_m5_199 = o_m5[199]        
        h_m5_199 = h_m5[199]
        l_m5_199 = l_m5[199]
        c_m5_199 = c_m5[199]
        v_m5_199 = v_m5[199]

        o_m5_198 = o_m5[198]        
        h_m5_198 = h_m5[198]
        l_m5_198 = l_m5[198]
        c_m5_198 = c_m5[198]
        v_m5_198 = v_m5[198]
                
        o_m5_197 = o_m5[197]        
        h_m5_197 = h_m5[197]
        l_m5_197 = l_m5[197]
        c_m5_197 = c_m5[197]

        up_m5_197 = h_m5_197 - c_m5_197
        mid_m5_197 = c_m5_197 - o_m5_197
        down_m5_197 = o_m5_197 - l_m5_197

        up_m5_198 = h_m5_198 - c_m5_198
        mid_m5_198 = c_m5_198 - o_m5_198
        down_m5_198 = o_m5_198 - l_m5_198


        buy_market = (o_m5_199 + ((h_m5_198 - l_m5_198)*0.5))

        m5_high_180_199 = h_m5.iloc[180:199]                                     
        m5_high_180_198 = h_m5.iloc[180:198]
        m5_high_180_197 = h_m5.iloc[180:197]

        m5_max_high_180_199 = m5_high_180_199.max(axis = 0)                     
        m5_max_high_180_198 = m5_high_180_198.max(axis = 0)
        m5_max_high_180_197 = m5_high_180_197.max(axis = 0)                      

        m5_low_180_199 = l_m5.iloc[180:199]
        m5_low_180_198 = l_m5.iloc[180:198]
        m5_min_low_180_199 = m5_low_180_199.min(axis = 0)
        m5_min_low_180_198 = m5_low_180_198.min(axis = 0)

        m5_close_180_198 = c_m5.iloc[180:198]
        m5_max_close_180_198 = m5_close_180_198.max(axis = 0)
                

        window5_m5 = c_m5.rolling(5)                                          
        ma5_m5 = window5_m5.mean()
        ma5_m5_199 = ma5_m5[199]
        ma5_m5_198 = ma5_m5[198]
        ma5_m5_197 = ma5_m5[197]
        ma5_m5_trend_199 = ma5_m5_199 - ma5_m5_198
        ma5_m5_trend_198 = ma5_m5_198 - ma5_m5_197
                                                
        window20_m5 = c_m5.rolling(20)                                          
        ma20_m5 = window20_m5.mean()
        ma20_m5_199 = ma20_m5[199]
        ma20_m5_198 = ma20_m5[198]
        ma20_m5_197 = ma20_m5[197]
        ma20_m5_trend_199 = ma20_m5_199 - ma20_m5_198
        ma20_m5_trend_198 = ma20_m5_198 - ma20_m5_197

        window60_m5 = c_m5.rolling(60)                                          
        ma60_m5 = window20_m5.mean()
        ma60_m5_199 = ma60_m5[199]
        ma60_m5_198 = ma60_m5[198]
        ma60_m5_197 = ma60_m5[197]
        ma60_m5_trend_199 = ma60_m5_199 - ma60_m5_198
        ma60_m5_trend_198 = ma60_m5_198 - ma60_m5_197

        window60_m5 = c_m5.rolling(180)                                          
        ma180_m5 = window20_m5.mean()
        ma180_m5_199 = ma180_m5[199]
        ma180_m5_198 = ma180_m5[198]
        ma180_m5_197 = ma180_m5[197]
        ma180_m5_trend_199 = ma180_m5_199 - ma180_m5_198
        ma180_m5_trend_198 = ma180_m5_198 - ma180_m5_197
                
            # 블린저 밴드 구하기 *** 떨어지는 낙폭? 표준편차값보다 더 낮게 떨어지면
        std20_m5 = window20_m5.std()

        window3_std20_m5 = std20_m5.rolling(20)
        ma20_std20_m5 = window3_std20_m5.mean()

        ma20_std20_m5_198 = ma20_std20_m5[198]  
        ma20_std20_m5_197 = ma20_std20_m5[197]

        std20_m5_150_199 = std20_m5.iloc[150:199]

        std20_m5_150_199[48]
        std20_m5_150_199[47]

        std20_m30_max_150_199 = std20_m5_150_199.max(axis =0)
        std20_m30_min_150_199 = std20_m5_150_199.min(axis =0)

        std20_m5_199 = std20_m5[199]
        std20_m5_198 = std20_m5[198]
        std20_m5_197 = std20_m5[197]

        bu20_m5_199 = ma20_m5_199 + std20_m5_199 * 2
        bu20_m5_198 = ma20_m5_198 + std20_m5_198 * 2
        bd20_m5_199 = ma20_m5_199 - std20_m5_199 * 2
        bd20_m5_198 = ma20_m5_198 - std20_m5_198 * 2         
        bd20_m5_197 = ma20_m5_197 - std20_m5_197 * 2

            #########################################################################
            # price channel 최소값 활용. 이거 잘 될거 같아!!!
            #########################################################################


        def rsi(ticker_df_m5, period: int = 7):
            c_m5 = ticker_df_m5['close']
            delta = c_m5.diff()
            
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
            
            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
            
            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")
        rsi = rsi(ticker_df_m5, 7).iloc[-1]

        def rsi1(ticker_df_m5, period: int = 7):
            c_m5 = ticker_df_m5['close']
            delta = c_m5.diff()
            
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
            
            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
            
            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")    
        rsi1 = rsi1(ticker_df_m5, 7).iloc[-2]

        def rsi2(ticker_df_m5, period: int = 7):
            c_m5 = ticker_df_m5['close']
            delta = c_m5.diff()
            
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
            
            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
            
            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")    
        rsi2 = rsi2(ticker_df_m5, 7).iloc[-3]

        rsiup = rsi1 - rsi2
        rsiup1 = rsi - rsi1





        #########################################################################
        # 매수 0조건. previous_min_lp와 ma5 상향 돌파 
        ######################################################################### 
        if rsi > 30 and ma60_m5_trend_199 > 0 :
            if ma5_m5_trend_199 > 0 and ma20_m5_trend_199 > 0 :
                if ma60_m5_198 > current_price and ma60_m5_199 < current_price:
                    if ma180_m5_199 < ma60_m5_199 :
                                    
                        bot.sendMessage(chat_id = tlgm_id, text = ticker+' 매수')
                        buy_record0 = upbit.buy_market_order(ticker, total_weight)
                        nlt = 0
                        pprint.pprint(buy_record0)
                        #already_buy[ticker] = True
                        #coin_investable -= 1



                #########################################################################
                # 익절 조건. 마진과 익절값 활용. 
                #########################################################################     
        if ticker_balance * current_price > 5000 :

            if  margin > 0.03 :
                sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                pprint.pprint(sell_record0)
                bot.sendMessage(chat_id = tlgm_id, text = ticker+' 수익실현')
                bot.sendMessage(chat_id = tlgm_id, text = margin)

            if  current_price <  ma20_m5_199 :
                sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                pprint.pprint(sell_record0)
                bot.sendMessage(chat_id = tlgm_id, text = ticker+' 수익실현')
                bot.sendMessage(chat_id = tlgm_id, text = margin)
                                    
                        
                    #######################################################################
                    # 손절 조건. 로스컷 도달 시 전량 매
                    #########################################################################          
    # 자동 갱신 조건들. 매수평균가, 손절가, 최고수익률
    #########################################################################
        if abp > 0 :
            balance_trigger = 1
            margin = (current_price - abp)/abp

            if margin > max_margin :
                max_margin = margin	
                    
        else :
            balance_trigger = 0
            
 

                                    
    #########################################################################
    # 자동 갱신 조건들. 매수평균가, 손절가, 최고수익률, 최고 최저가
    #########################################################################   
time.sleep(1)

