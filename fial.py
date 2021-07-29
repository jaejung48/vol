
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
tlgm_token = '1770499141:AAGa1uvZnZs1nbgDGpxNuBhxZXaVr2jwf5Q'                   
tlgm_id = '1146999309'                                                          
bot = telegram.Bot(token = tlgm_token)                                          
updates = bot.getUpdates()                                                      
bot.sendMessage(chat_id = tlgm_id, text = 'Crypto Commando') 

# 초기 세팅
tickers = pyupbit.get_tickers(fiat = "KRW")
#ticker = "KRW-BTC"   # 투자하고 싶은 코인의 티커 입력
total_weight = 50000  # 투자금액 설정

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
        ticker_df_m3 = pyupbit.get_ohlcv(ticker,"minute60")
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
        v_m3_199 = v_m3[199]

        o_m3_198 = o_m3[198]        
        h_m3_198 = h_m3[198]
        l_m3_198 = l_m3[198]
        c_m3_198 = c_m3[198]
        v_m3_198 = v_m3[198]

        o_m3_197 = o_m3[197]        
        h_m3_197 = h_m3[197]
        l_m3_197 = l_m3[197]
        c_m3_197 = c_m3[197]
        v_m3_197 = v_m3[197]




           
    #########################################################################
    # 매 반복 시 출력 정보
    #########################################################################
     
         
    #########################################################################
    # 매수 0조건. previous_min_lp와 ma5 상향 돌파 
    ######################################################################### 
        if v_m3_197 * 7 < v_m3_198 and h_m3_198 < current_price :
            print(ticker, " 1st")

            bot.sendMessage(chat_id = tlgm_id, text = ticker+' ch')

        if ticker_balance > 0 :
            margin = (current_price - abp)/abp
            print(margin)
             

        if abp == 0 :
            margin = 0  
                                    
   
time.sleep(1)
    
    