
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
        v_1d_199 = v_1d[9]
        

        o_1d_198 = o_1d[8]        
        h_1d_198 = h_1d[8]
        l_1d_198 = l_1d[8]
        c_1d_198 = c_1d[8]
        v_1d_198 = v_1d[8]        

        o_1d_197 = o_1d[7]        
        h_1d_197 = h_1d[7]
        l_1d_197 = l_1d[7]
        c_1d_197 = c_1d[7]
        v_1d_197 = v_1d[7]

        o_1d_196 = o_1d[6]        
        h_1d_196 = h_1d[6]
        l_1d_196 = l_1d[6]
        c_1d_196 = c_1d[6]
        v_1d_196 = v_1d[6]

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

        vol = v_1d_196  - (v_1d_197/8)

        #########################################################################
        # 매수 0조건. previous_min_lp와 ma5 상향 돌파 
        ######################################################################### 
        if v_1d_196  - (v_1d_197/8) < 0:
            if current_price > h_1d_198 :
                bot.sendMessage(chat_id = tlgm_id, text = ticker+'2차매수' + str(round(current_price,2)))

 

                                    
    #########################################################################
    # 자동 갱신 조건들. 매수평균가, 손절가, 최고수익률, 최고 최저가
    #########################################################################   
    time.sleep(1)

