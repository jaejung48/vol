

# 업비트 API 로그인
import pyupbit						
import time		
import pprint
import pandas as pa
import plotly.express as px	
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
total_weight = 6000  # 투자금액 설정

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

        m3_close_180_198 = c_m3.iloc[180:198]
        m3_max_close_180_198 = m3_close_180_198.max(axis = 0)

        # 이동평균과 추세
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

        window20_m30 = c_m30.rolling(60)                                          
        ma60_m30 = window20_m30.mean()
        ma60_m30_199 = ma60_m30[199]
        ma60_m30_198 = ma60_m30[198]
        ma60_m30_197 = ma60_m30[197]
        ma60_m30_trend_199 = ma60_m30_199 - ma60_m30_198
        ma60_m30_trend_198 = ma60_m30_198 - ma60_m30_197
        
        

           
    #########################################################################
    # 매 반복 시 출력 정보
    #########################################################################

          
    #########################################################################
    # 매수 0조건. previous_min_lp와 ma5 상향 돌파 
    ######################################################################### 
        if ma5_m30_trend_198 > 0 and ma20_m30_trend_198 > 0 and ma60_m30_trend_199 > 0:
            print("첫번째 :", ticker)
            if ma5_m30[199] > ma20_m30[199] and ma5_m30[198] > ma20_m30[198] :
                print("두번째 :", ticker)
                if current_price > m30_max_close_180_198 and current_price < m30_max_high_180_198 :
                    if (current_price - c_m30[195])/c_m30[195] < 0.15 :
                        if (h_m30[198] - current_price)/h_m30[198] < 0.03 :
                            bot.sendMessage(chat_id = tlgm_id, text = ticker+' 선택')
                            print(ticker, " 화이팅")
                            profit = (ma5_m30_199 - ma20_m30_199) / ma20_m30_199
                            
                            if ticker in wave :                     
                                print(ticker, "Wave")
                    
                            else:
                                wave.append(ticker)

                                buy_record0 = upbit.buy_market_order(ticker, total_weight)
                                pprint.pprint(buy_record0) 

    #########################################################################
    # 익절 조건. 마진과 익절값 활용. 
    #########################################################################     
                            if ticker_balance * current_price > 5000 :
            #if current_price > abp * 1.05 :
             #   sell_record0 = upbit.sell_market_order(ticker, ticker_balance/2)
              #  pprint.pprint(sell_record0) 
                                if current_price > abp * 1.03 :
                                    bot.sendMessage(chat_id = tlgm_id, text = ticker+'축하')
                                    bot.sendMessage(chat_id = tlgm_id, text = margin)
                                    sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                                    pprint.pprint(sell_record0)  
                                    print("수익 완료", ticker, margin)
                                    nlt = 0 
                                   
           
    #######################################################################
    # 손절 조건. 로스컷 도달 시 전량 매
    #########################################################################          
                            if current_price < ma20_m30[199] :
                                bot.sendMessage(chat_id = tlgm_id, text = ticker+' 손절')
                                sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                                pprint.pprint(sell_record0)
                                    
    #########################################################################
    # 자동 갱신 조건들. 매수평균가, 손절가, 최고수익률, 최고 최저가
    #########################################################################
   
time.sleep(1)
