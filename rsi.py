
# 업비트 API 로그인
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
tlgm_token = '1770499141:AAFGgivsAkLTLKnZU2bQb8cDxcNC1eCUr_o'                   
tlgm_id = '1146999309'                                                          
bot = telegram.Bot(token = tlgm_token)                                          
updates = bot.getUpdates()                                                      
bot.sendMessage(chat_id = tlgm_id, text = 'Crypto Commando') 

# 초기 세팅
tickers = pyupbit.get_tickers(fiat = "KRW")
#ticker = "KRW-BTC"   # 투자하고 싶은 코인의 티커 입력
total_weight = 100000  # 투자금액 설정

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
        
        o_m30_197 = o_m30[197]        
        h_m30_197 = h_m30[197]
        l_m30_197 = l_m30[197]
        c_m30_197 = c_m30[197]

        up_m30_197 = h_m30_197 - c_m30_197
        mid_m30_197 = c_m30_197 - o_m30_197
        down_m30_197 = o_m30_197 - l_m30_197

        up_m30_198 = h_m30_198 - c_m30_198
        mid_m30_198 = c_m30_198 - o_m30_198
        down_m30_198 = o_m30_198 - l_m30_198


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

        m30_close_180_198 = c_m30.iloc[180:198]
        m30_max_close_180_198 = m30_close_180_198.max(axis = 0)
        

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

        window60_m30 = c_m30.rolling(60)                                          
        ma60_m30 = window20_m30.mean()
        ma60_m30_199 = ma60_m30[199]
        ma60_m30_198 = ma60_m30[198]
        ma60_m30_197 = ma60_m30[197]
        ma60_m30_trend_199 = ma60_m30_199 - ma60_m30_198
        ma60_m30_trend_198 = ma60_m30_198 - ma60_m30_197
        
     # 블린저 밴드 구하기 *** 떨어지는 낙폭? 표준편차값보다 더 낮게 떨어지면
        std20_m30 = window20_m30.std()

        window3_std20_m30 = std20_m30.rolling(20)
        ma20_std20_m30 = window3_std20_m30.mean()

        ma20_std20_m30_198 = ma20_std20_m30[198]  
        ma20_std20_m30_197 = ma20_std20_m30[197]

        std20_m30_150_199 = std20_m30.iloc[150:199]

        std20_m30_150_199[48]
        std20_m30_150_199[47]

        std20_m30_max_150_199 = std20_m30_150_199.max(axis =0)
        std20_m30_min_150_199 = std20_m30_150_199.min(axis =0)

        std20_m30_199 = std20_m30[199]
        std20_m30_198 = std20_m30[198]
        std20_m30_197 = std20_m30[197]

        bu20_m30_199 = ma20_m30_199 + std20_m30_199 * 2
        bu20_m30_198 = ma20_m30_198 + std20_m30_198 * 2
        bd20_m30_199 = ma20_m30_199 - std20_m30_199 * 2
        bd20_m30_198 = ma20_m30_198 - std20_m30_198 * 2         
        bd20_m30_197 = ma20_m30_197 - std20_m30_197 * 2


        def rsi(ticker_df_m30, period: int = 14):
            c_m30 = ticker_df_m30['close']
            delta = c_m30.diff()
    
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
    
            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    
            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")
    
        rsi = rsi(ticker_df_m30, 14).iloc[-3]
           
    #########################################################################
    # 매 반복 시 출력 정보
    #########################################################################
     
         
    #########################################################################
    # 매수 0조건. previous_min_lp와 ma5 상향 돌파 
    ######################################################################### 
        if rsi < 60 and c_m30_197 < bd20_m30_197 :
            print(ticker, "첫번째")
            if o_m30_197 > c_m30_197 and o_m30_198 < c_m30_198 :
                print(ticker, "두번째")
                if (o_m30_197 - c_m30_197) / 2 > c_m30_198 :
                    if ticker in wave :                     
                        print(ticker, "Wave")
                    
                    else:
                        wave.append(ticker)

                    buy_record0 = upbit.buy_market_order(ticker, total_weight)
                    pprint.pprint(buy_record0)


                if ticker_balance > 0 :
                    margin = (current_price - abp)/abp
                    print(margin)
             

                if abp == 0 :
                    margin = 0  
    #########################################################################
    # 익절 조건. 마진과 익절값 활용. 
    #########################################################################     
                if ticker_balance * current_price > 5000 :

                    if  l_m30_197 > current_price :
                        sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                        pprint.pprint(sell_record0)
                        print("수익 완료", ticker, margin)
                        nlt = 0 
                        abp = 0
                        margin = 0
                                   
           
    #######################################################################
    # 손절 조건. 로스컷 도달 시 전량 매
    #########################################################################          
        #if margin < 0.05 :
            #bot.sendMessage(chat_id = tlgm_id, text = ticker+' 손절')
            #sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
            #pprint.pprint(sell_record0)
                                    
    #########################################################################
    # 자동 갱신 조건들. 매수평균가, 손절가, 최고수익률, 최고 최저가
    #########################################################################
   
time.sleep(1)
    
    