

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
total_weight = 15000  # 투자금액 설정

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

        #########################################################################
        # 데이타 추출1. 
        #########################################################################
        ticker_df_m5 = pyupbit.get_ohlcv(ticker,"minute5")
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
        h_m5_198 = h_m5[198]
        l_m5_198 = l_m5[198]
        v_m5_198 = v_m5[198]
        v_m5_199 = v_m5[199]

        m5_high_190_199 = h_m5.iloc[190:199]                                     
        m5_high_190_198 = h_m5.iloc[190:198]
        m5_high_190_197 = h_m5.iloc[190:197]

        m5_max_high_190_199 = m5_high_190_199.max(axis = 0)                     
        m5_max_high_190_198 = m5_high_190_198.max(axis = 0)
        m5_max_high_190_197 = m5_high_190_197.max(axis = 0)                      

        m5_low_190_199 = l_m5.iloc[190:199]
        m5_low_189_198 = l_m5.iloc[189:198]
        m5_low_188_197 = l_m5.iloc[188:197]
        m5_min_low_190_199 = m5_low_190_199.min(axis = 0)
        m5_min_low_189_198 = m5_low_189_198.min(axis = 0)
        m5_min_low_188_197 = m5_low_188_197.min(axis = 0)

        m5_close_190_198 = c_m5.iloc[190:198]
        m5_max_close_190_198 = m5_close_190_198.max(axis = 0)

        buy_market = (o_m5_199 + ((h_m5_198 - l_m5_198)*0.5))

        # 이동평균과 추세
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
        

     # 블린저 밴드 구하기 *** 떨어지는 낙폭? 표준편차값보다 더 낮게 떨어지면
        std20_m5 = window20_m5.std()
        window3_std20_m5 = std20_m5.rolling(20)
        ma20_std20_m5 = window3_std20_m5.mean()

        ma20_std20_m5_198 = ma20_std20_m5[198]  
        ma20_std20_m5_197 = ma20_std20_m5[197]

        std20_m5_180_199 = std20_m5.iloc[180:199]

        std20_m5_180_199[18]
        std20_m5_180_199[17]

        std20_m5_max_180_199 = std20_m5_180_199.max(axis =0)
        std20_m5_min_180_199 = std20_m5_180_199.min(axis =0)

        std20_m5_199 = std20_m5[199]
        bu20_m5_199 = ma20_m5_199 + std20_m5_199 * 2
        bd20_m5_199 = ma20_m5_199 - std20_m5_199 * 2 
                                   
        if ticker_balance > 0 :
            margin = (current_price - abp)/abp

        if abp == 0 :
            margin = 0     
    #########################################################################
    # 데이타 추출
    #########################################################################

           
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
        if ma5_m5_199 > ma5_m5_198 and ma20_m5_199 > ma20_m5_198 :
            if current_price < m5_max_high_190_199 and current_price > h_m5_198 :
                if v_m5_199 > v_m5_198 *2 :
                    print(ticker)
                    buy_record0 = upbit.buy_market_order(ticker, total_weight)
                    pprint.pprint(buy_record0) 

    #########################################################################
    # 익절 조건. 마진과 익절값 활용. 
    #########################################################################     
        if ticker_balance * current_price > 5000 :
            if current_price > abp * 1.01 :
                sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                pprint.pprint(sell_record0)  
                print("#############################################################")

                nlt = 0

    #######################################################################
    # 손절 조건. 로스컷 도달 시 전량 매도
    #########################################################################          
        if current_price < l_m5_198 :
            
            sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
            pprint.pprint(sell_record0)
 
            
    #########################################################################
    # 자동 갱신 조건들. 매수평균가, 손절가, 최고수익률, 최고 최저가
    #########################################################################
   
time.sleep(1)
