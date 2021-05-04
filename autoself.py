
# 업비트 API 로그인
import pyupbit						
import time		
import pprint
import pandas as pa
import plotly.express as px	
access = "4bAGnrGccIFCZ1nZyhgNGx7itfJNBmomDtF61i69"							    # 엑세스 키 입력					
secret = "ZzxALJxXMf71E4pmMFdSWxMuJo4nTx0hBIzJ0fFU"		
upbit = pyupbit.Upbit(access, secret)	


# 초기 세팅
tickers = pyupbit.get_tickers(fiat = "KRW")
#ticker = "KRW-BTC"   # 투자하고 싶은 코인의 티커 입력
total_weight = 20000  # 투자금액 설정

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
last_lp = 0
max_min_lp = 0
current_min_lp = 0
nlt = 0


# 반복문 실행
while True:  
    
    for ticker in tickers :
    
        ticker_balance = upbit.get_balance(ticker)	
        krw_balance = upbit.get_balance("KRW")
        abp = upbit.get_avg_buy_price(ticker)
        current_price = pyupbit.get_current_price(ticker)

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

        if o_1d_199 - c_1d_198 > 1 :
                           
            if ticker_balance > 0 :
                margin = (current_price - abp)/abp

            if abp == 0 :
                margin = 0    
    #########################################################################
    # 데이타 추출
    #########################################################################
        ticker_df_m30 = pyupbit.get_ohlcv(ticker,"minute30")
        ticker_df_m30['amount'] = ticker_df_m30['volume'] * ticker_df_m30['close']
        o_m30 = ticker_df_m30['open']
        h_m30 = ticker_df_m30['high']   
        l_m30 = ticker_df_m30['low']                                   
        c_m30 = ticker_df_m30['close']                                                    
        v_m30 = ticker_df_m30['volume']
        a_m30 = ticker_df_m30['amount']                  
        
        volume_check_range = a_m30.iloc[190:199]
        volume_check = int(volume_check_range.sum())

        o_m30_199 = o_m30[199]        
        h_m30_199 = h_m30[199]
        l_m30_199 = l_m30[199]
        c_m30_199 = c_m30[199]

        o_m30_198 = o_m30[198]        
        h_m30_198 = h_m30[198]
        l_m30_198 = l_m30[198]
        c_m30_198 = c_m30[198]

        buy_market = (o_m30_199 + ((h_m30_198 - l_m30_198)*0.5))

        m30_high_180_199 = h_m30.iloc[180:199]                                     
        m30_high_180_198 = h_m30.iloc[180:198]
        m30_high_180_197 = h_m30.iloc[180:197]

        m30_max_high_180_199 = m30_high_180_199.max(axis = 0)                     
        m30_max_high_180_198 = m30_high_180_198.max(axis = 0)
        m30_max_high_180_197 = m30_high_180_197.max(axis = 0)                      

        m30_low_180_199 = l_m30.iloc[180:199]
        m30_low_180_198 = l_m30.iloc[180:198]
        m30_min_low_180_199 = m30_low_180_199.min(axis = 0)
        m30_min_low_180_198 = m30_low_180_198.min(axis = 0)

        window5_m30 = c_m30.rolling(5)                                          
        ma5_m30 = window5_m30.mean()
        ma5_m30_199 = ma5_m30[199]
        ma5_m30_198 = ma5_m30[198]
        ma5_m30_197 = ma5_m30[197]
        ma5_m30_trend_199 = ma5_m30_199 - ma5_m30_198
        ma5_m30_trend_198 = ma5_m30_198 - ma5_m30_197
                                        
        window20_m30 = c_m30.rolling(20)                                          
        ma20_m30 = window20_m30.mean()
        ma20_m30_199 = ma20_m30[199]
        ma20_m30_198 = ma20_m30[198]
        ma20_m30_197 = ma20_m30[197]
        ma20_m30_trend_199 = ma20_m30_199 - ma20_m30_198
        ma20_m30_trend_198 = ma20_m30_198 - ma20_m30_197
    
    #########################################################################
    # 매 반복 시 출력 정보
    #########################################################################
        if last_candle_color == 1 :
            print('\033[30m', time.strftime('%m-%d %H:%M:%S'),"", 
         "무슨코인:",ticker,"",
         "최대수익률:", round(max_margin, 4),"",         
         "현재가격.매수평균가.손절가:", round(current_price),round(abp),round(loss_cut), "",
         "코인 잔고", round(ticker_balance * current_price),"",
         '\033[0m'
         )    
       
        else :
            print('\033[34m', time.strftime('%m-%d %H:%M:%S'),"", 
         "무슨코인:",ticker,"",
         "최대수익률:", round(max_margin, 4),"", 
         "현재가격.매수평균가.손절가:", round(current_price),round(abp),round(loss_cut), "",
         "코인 잔고", round(ticker_balance * current_price),"",
         '\033[0m'         
         )    
          
    #########################################################################
    # 매수 0조건. previous_min_lp와 ma5 상향 돌파 
    ######################################################################### 
        if ma5_m30_199 > ma20_m30_199  and current_price > buy_market :
            if ticker_balance >= 0 and ticker_balance * current_price <= 6000 :
                print("#############################################################")
                print("buy condition 0. New trigger. more simple")
                print("#############################################################")
                buy_record0 = upbit.buy_market_order(ticker, total_weight)
                        
                pprint.pprint(buy_record0) 
                print("-------------------------------------------------------------")

   

    #########################################################################
    # 익절 조건. 마진과 익절값 활용. 
    #########################################################################     
        if nlt == 1 and current_price >= abp * 1.01 :
            if ticker_balance * abp > 0 :
                print("#############################################################")
                print("sell condition 4. Profit realization")
                print("#############################################################")
                sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                pprint.pprint(sell_record0)  
                print("#############################################################")
            else :
                sell_record0 = upbit.sell_market_order(ticker, ticker_balance)

                nlt = 0

    #######################################################################
    # 손절 조건. 로스컷 도달 시 전량 매도
    #########################################################################          
        if current_price <= abp - (abp * 0.01) :
            if ticker_balance * abp > 0 :
                print("#############################################################")
                print("sell condition 3. Loss Cut by Loss Cut")
                print("#############################################################")
                sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                pprint.pprint(sell_record0)
                print("------------------------------------------------------------")
                print("sell_market_orders are condected")
                print("------------------------------------------------------------")

            
    #########################################################################
    # 자동 갱신 조건들. 매수평균가, 손절가, 최고수익률, 최고 최저가
    #########################################################################
   
time.sleep(10)
    
    