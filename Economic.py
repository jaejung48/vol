"""

생존형퀀트의 경제적자유. https://blog.naver.com/starfox119

overlapping previous high point


1분봉에서 
거래량 이평 5, 10, 20이 정배열이고, 
현재가가 구름대 위에 있고, 
전고점을 돌파했다면, 
오퍼레이션 데이터프레임 중 해당 열에 1 기록

1분봉 조건열이 1을 기록하고 있을 때
3분봉에서 동일 조건을 충족하면
오퍼레이션 데이터프레임 중 해당 열에 1 기록

이것을 5, 10, 15, 30, 60, 240, day까지 반복

취향에 따라 각 분봉별 조건 충족 시 분할매수.하면 괜찮을 듯.
진입 이후에는 1분봉 조건으로 매매하며
1퍼센트 단위로 분할매도. 분할매도 분량은 각자 설정.
1분봉에서 완전 하락 구간으로 전환 시 전량매도
이후 조건 충족 시 재진입

-----------
1분봉 5이평이 구름대 밑으로 하향돌파하면 리스트에서 제외






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
import telegram                                                                 # 델레그램 모듈 임포트
tlgm_token = '1770499141:AAGa1uvZnZs1nbgDGpxNuBhxZXaVr2jwf5Q'                   
tlgm_id = '1146999309'                                                        # 텔레그램 챗 아이디 입력
bot = telegram.Bot(token = tlgm_token)                                          # 봇 채팅방 접속
# updates = bot.getUpdates()                                                      # 내용 업데이트?
bot.sendMessage(chat_id = tlgm_id, text = 'Dark horse finder')                   # 프로그램 시작을 알리는 메세지 보내보기



#########################################################################
# 기타 모듈
#########################################################################
import pandas as pd
import openpyxl
# operation_df.to_excel('check.xlsx')


#########################################################################
# 변수 초기값
#########################################################################
weight = 200000   # 캘리비율 적용 시켜서 전체 보유금의 50%만 투입


#########################################################################
# 전체 코인 티커 조회
#########################################################################
tickers = pyupbit.get_tickers(fiat = "KRW")
#tickers = ['KRW-AXS']
#tickers = ("KRW-SXP")
tickers.remove("KRW-BTC")  
tickers.remove("KRW-ETH")  
tickers.remove("KRW-ADA") 
tickers.remove("KRW-EOS") 
tickers.remove("KRW-XRP") 
tickers.remove("KRW-LTC") 
tickers.remove("KRW-DOT") 
tickers.remove("KRW-ETC") 
tickers.remove("KRW-TRX") 

operation_df = pd.DataFrame(columns = ['ticker', 
                                       'min1',
                                       'min3',
                                       'min5',
                                       'min10',
                                       'min15',
                                       'min30',
                                       'min60',
                                       'min240',
                                       'start',
                                       'current',
                                       'day',
                                       'buy_trigger'])

operation_df['ticker'] = tickers
operation_df.fillna(0, inplace=True) 


#########################################################################
# 획기적 개선. 관리 데이터프레임
#########################################################################
#tickers = pyupbit.get_tickers(fiat = "KRW")
#operation_df.loc[(coin_df.ticker == 'KRW-BTC'),'max_margin']= 7
#crypto_commando = tickers 
#tickers.remove("KRW-XRP")
#tickers.append("KRW-XRP") 
#tickers = ['KRW-VET']   
abp = 0
current_price = 0
margin = 0

profit_or_loss = 0
compare_to_abp = 0

profit = 0
loss = 0

disparity = 0


#########################################################################
# 반복문 시작
#########################################################################
while True : 
     for ticker in tickers :
        
        ######################################################################
        # 반복문 내부 변수
        ###################################################################### 
        current_price = pyupbit.get_current_price(ticker)
        
        min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min1'])
        min3   = float(operation_df.loc[(operation_df.ticker == ticker), 'min3'])
        min5   = float(operation_df.loc[(operation_df.ticker == ticker), 'min5'])
        min10  = float(operation_df.loc[(operation_df.ticker == ticker), 'min10'])
        min15  = float(operation_df.loc[(operation_df.ticker == ticker), 'min15'])
        min30  = float(operation_df.loc[(operation_df.ticker == ticker), 'min30'])
        min60  = float(operation_df.loc[(operation_df.ticker == ticker), 'min60'])
        min240 = float(operation_df.loc[(operation_df.ticker == ticker), 'min240'])
        day    = float(operation_df.loc[(operation_df.ticker == ticker), 'day'])
        
               
                       
        
        ######################################################################
        # 1분봉데이터 가져오기
        ######################################################################
        ticker_df_m1   = pyupbit.get_ohlcv(ticker, "minute1") 
        open_price_m1  = ticker_df_m1['open']
        high_price_m1  = ticker_df_m1['high']
        low_price_m1   = ticker_df_m1['low']
        close_price_m1 = ticker_df_m1['close']
        volume_m1      = ticker_df_m1['volume']
        
        volume_checker = (volume_m1 [-1] + volume_m1 [-2] + volume_m1 [-3]) * current_price 
        
        ######################################################################
        # 거래량 이동평균과 추세 구하기
        ######################################################################
        vma5_m1     = ticker_df_m1['vma5']      = volume_m1.rolling(5).mean()
        vma10_m1    = ticker_df_m1['vma10']     = volume_m1.rolling(10).mean()
        vma20_m1    = ticker_df_m1['vma20']     = volume_m1.rolling(20).mean()
        

               
        ######################################################################
        # 1분봉 이동평균과 추세 구하기
        ###################################################################### 
        ma5_m1     = ticker_df_m1['ma5']      = close_price_m1.rolling(5).mean()
        ma20_m1    = ticker_df_m1['ma20']     = close_price_m1.rolling(20).mean()
        ma60_m1    = ticker_df_m1['ma60']     = close_price_m1.rolling(60).mean()
        ma120_m1   = ticker_df_m1['ma120']    = close_price_m1.rolling(120).mean()
        ma180_m1   = ticker_df_m1['ma180']    = close_price_m1.rolling(180).mean()
        
        ma5_trend_199_m1 = ma5_m1[199] - ma5_m1[198] 
        ma5_trend_198_m1 = ma5_m1[198] - ma5_m1[197] 
        
        ma20_trend_199_m1 = ma20_m1[199] - ma20_m1[198] 
        ma20_trend_198_m1 = ma20_m1[198] - ma20_m1[197] 
        
        
        ######################################################################
        # PRICE CHANNEL 상한선, 하한선, 중앙선 구하기
        ######################################################################   
        max_high_20_m1     = ticker_df_m1['max_high_20']  =  high_price_m1.rolling(20, axis = 0 ).max()    
        max_close_20_m1    = ticker_df_m1['max_close_20'] =  close_price_m1.rolling(20, axis = 0 ).max() 
        min_low_20_m1      = ticker_df_m1['min_low_20']   =  low_price_m1.rolling(20, axis = 0).min() 
        middle_20_m1       = ticker_df_m1['middle_20']    =  (ticker_df_m1['max_high_20'] + ticker_df_m1['min_low_20'])/2
        
        
        ######################################################################
        # PRICE CHANNEL 활용. 일목균형표로 변환
        ######################################################################
        max_high_9_m1      = ticker_df_m1['max_high_9']     =  high_price_m1.rolling(9, axis = 0 ).max()   
        min_low_9_m1       = ticker_df_m1['min_low_9']      =  low_price_m1.rolling(9, axis = 0).min()
        
        max_high_26_m1     = ticker_df_m1['max_high_26']    =  high_price_m1.rolling(26, axis = 0 ).max()   
        min_low_26_m1      = ticker_df_m1['min_low_26']     =  low_price_m1.rolling(26, axis = 0).min()
        
        max_high_52_m1     = ticker_df_m1['max_high_52']    =  high_price_m1.rolling(52, axis = 0 ).max()   
        min_low_52_m1      = ticker_df_m1['min_low_52']     =  low_price_m1.rolling(52, axis = 0).min()
        
        conversion_line_m1 = ticker_df_m1['middle_9']       =  (ticker_df_m1['max_high_9'] + ticker_df_m1['min_low_9'])/2
        base_line_m1       = ticker_df_m1['middle_26']      =  (ticker_df_m1['max_high_26'] + ticker_df_m1['min_low_26'])/2
        
        leading_spanA_m1   = (ticker_df_m1['middle_9'] + ticker_df_m1['middle_26'])/2      # 199 - 26
        leading_spanB_m1   = (ticker_df_m1['max_high_52'] + ticker_df_m1['min_low_52'])/2   # 199 - 26
        
        
        
        
        
        ######################################################################
        # 3분봉데이터 가져오기
        ######################################################################
        ticker_df_m3   = pyupbit.get_ohlcv(ticker, "minute3") 
        open_price_m3  = ticker_df_m3['open']
        high_price_m3  = ticker_df_m3['high']
        low_price_m3   = ticker_df_m3['low']
        close_price_m3 = ticker_df_m3['close']
        volume_m3      = ticker_df_m3['volume']
        
        
        ######################################################################
        # 거래량 이동평균과 추세 구하기
        ######################################################################
        vma5_m3     = ticker_df_m3['vma5']      = volume_m3.rolling(5).mean()
        vma10_m3    = ticker_df_m3['vma10']     = volume_m3.rolling(10).mean()
        vma20_m3    = ticker_df_m3['vma20']     = volume_m3.rolling(20).mean()
        
        
        ######################################################################
        # 3분봉 이동평균과 추세 구하기
        ###################################################################### 
        ma5_m3     = ticker_df_m3['ma5']      = close_price_m3.rolling(5).mean()
        ma20_m3    = ticker_df_m3['ma20']     = close_price_m3.rolling(20).mean()
        ma60_m3    = ticker_df_m3['ma60']     = close_price_m3.rolling(60).mean()
        ma120_m3   = ticker_df_m3['ma120']    = close_price_m3.rolling(120).mean()
        ma180_m3   = ticker_df_m3['ma180']    = close_price_m3.rolling(180).mean()
        
        ma5_trend_199_m3 = ma5_m3[199] - ma5_m3[198] 
        ma5_trend_198_m3 = ma5_m3[198] - ma5_m3[197] 
        
        ma20_trend_199_m3 = ma20_m3[199] - ma20_m3[198] 
        ma20_trend_198_m3 = ma20_m3[198] - ma20_m3[197] 
        
        
        ######################################################################
        # PRICE CHANNEL 상한선, 하한선, 중앙선 구하기
        ######################################################################   
        max_high_20_m3     = ticker_df_m3['max_high_20']  =  high_price_m3.rolling(20, axis = 0 ).max()    
        max_close_20_m3    = ticker_df_m3['max_close_20'] =  close_price_m3.rolling(20, axis = 0 ).max() 
        min_low_20_m3      = ticker_df_m3['min_low_20']   =  low_price_m3.rolling(20, axis = 0).min() 
        middle_20_m3       = ticker_df_m3['middle_20']    =  (ticker_df_m3['max_high_20'] + ticker_df_m3['min_low_20'])/2
        
        
        ######################################################################
        # PRICE CHANNEL 활용. 일목균형표로 변환
        ######################################################################
        max_high_9_m3      = ticker_df_m3['max_high_9']     =  high_price_m3.rolling(9, axis = 0 ).max()   
        min_low_9_m3       = ticker_df_m3['min_low_9']      =  low_price_m3.rolling(9, axis = 0).min()
        
        max_high_26_m3     = ticker_df_m3['max_high_26']    =  high_price_m3.rolling(26, axis = 0 ).max()   
        min_low_26_m3      = ticker_df_m3['min_low_26']     =  low_price_m3.rolling(26, axis = 0).min()
        
        max_high_52_m3     = ticker_df_m3['max_high_52']    =  high_price_m3.rolling(52, axis = 0 ).max()   
        min_low_52_m3      = ticker_df_m3['min_low_52']     =  low_price_m3.rolling(52, axis = 0).min()
        
        conversion_line_m3 = ticker_df_m3['middle_9']       =  (ticker_df_m3['max_high_9'] + ticker_df_m3['min_low_9'])/2
        base_line_m3       = ticker_df_m3['middle_26']      =  (ticker_df_m3['max_high_26'] + ticker_df_m3['min_low_26'])/2
        
        leading_spanA_m3   = (ticker_df_m3['middle_9'] + ticker_df_m3['middle_26'])/2      # 199 - 26
        leading_spanB_m3   = (ticker_df_m3['max_high_52'] + ticker_df_m3['min_low_52'])/2   # 199 - 26
        
        
        
        
        
        
        
          
        
        
        ######################################################################
        # 5분봉데이터 가져오기
        ######################################################################
        ticker_df_m5   = pyupbit.get_ohlcv(ticker, "minute5") 
        open_price_m5  = ticker_df_m5['open']
        high_price_m5  = ticker_df_m5['high']
        low_price_m5   = ticker_df_m5['low']
        close_price_m5 = ticker_df_m5['close']
        volume_m5      = ticker_df_m5['volume']
        
        
        ######################################################################
        # 거래량 이동평균과 추세 구하기
        ######################################################################
        vma5_m5     = ticker_df_m5['vma5']      = volume_m5.rolling(5).mean()
        vma10_m5    = ticker_df_m5['vma10']     = volume_m5.rolling(10).mean()
        vma20_m5    = ticker_df_m5['vma20']     = volume_m5.rolling(20).mean()
        
        
        ######################################################################
        # 3분봉 이동평균과 추세 구하기
        ###################################################################### 
        ma5_m5     = ticker_df_m5['ma5']      = close_price_m5.rolling(5).mean()
        ma20_m5    = ticker_df_m5['ma20']     = close_price_m5.rolling(20).mean()
        ma60_m5    = ticker_df_m5['ma60']     = close_price_m5.rolling(60).mean()
        ma120_m5   = ticker_df_m5['ma120']    = close_price_m5.rolling(120).mean()
        ma180_m5   = ticker_df_m5['ma180']    = close_price_m5.rolling(180).mean()
        
        ma5_trend_199_m5 = ma5_m5[199] - ma5_m5[198] 
        ma5_trend_198_m5 = ma5_m5[198] - ma5_m5[197] 
        
        ma20_trend_199_m5 = ma20_m5[199] - ma20_m5[198] 
        ma20_trend_198_m5 = ma20_m5[198] - ma20_m5[197] 
        
        
        ######################################################################
        # PRICE CHANNEL 상한선, 하한선, 중앙선 구하기
        ######################################################################   
        max_high_20_m5     = ticker_df_m5['max_high_20']  =  high_price_m5.rolling(20, axis = 0 ).max()    
        max_close_20_m5    = ticker_df_m5['max_close_20'] =  close_price_m5.rolling(20, axis = 0 ).max() 
        min_low_20_m5      = ticker_df_m5['min_low_20']   =  low_price_m5.rolling(20, axis = 0).min() 
        middle_20_m5       = ticker_df_m5['middle_20']    =  (ticker_df_m5['max_high_20'] + ticker_df_m5['min_low_20'])/2
        
        
        ######################################################################
        # PRICE CHANNEL 활용. 일목균형표로 변환
        ######################################################################
        max_high_9_m5      = ticker_df_m5['max_high_9']     =  high_price_m5.rolling(9, axis = 0 ).max()   
        min_low_9_m5       = ticker_df_m5['min_low_9']      =  low_price_m5.rolling(9, axis = 0).min()
        
        max_high_26_m5     = ticker_df_m5['max_high_26']    =  high_price_m5.rolling(26, axis = 0 ).max()   
        min_low_26_m5      = ticker_df_m5['min_low_26']     =  low_price_m5.rolling(26, axis = 0).min()
        
        max_high_52_m5     = ticker_df_m5['max_high_52']    =  high_price_m5.rolling(52, axis = 0 ).max()   
        min_low_52_m5      = ticker_df_m5['min_low_52']     =  low_price_m5.rolling(52, axis = 0).min()
        
        conversion_line_m5 = ticker_df_m5['middle_9']       =  (ticker_df_m5['max_high_9'] + ticker_df_m5['min_low_9'])/2
        base_line_m5       = ticker_df_m5['middle_26']      =  (ticker_df_m5['max_high_26'] + ticker_df_m5['min_low_26'])/2
        
        leading_spanA_m5   = (ticker_df_m5['middle_9'] + ticker_df_m5['middle_26'])/2      # 199 - 26
        leading_spanB_m5   = (ticker_df_m5['max_high_52'] + ticker_df_m5['min_low_52'])/2   # 199 - 26
        
        
        
        
        
        
        ######################################################################
        # 10분봉데이터 가져오기
        ######################################################################
        ticker_df_m10   = pyupbit.get_ohlcv(ticker, "minute10") 
        open_price_m10  = ticker_df_m10['open']
        high_price_m10  = ticker_df_m10['high']
        low_price_m10   = ticker_df_m10['low']
        close_price_m10 = ticker_df_m10['close']
        volume_m10      = ticker_df_m10['volume']
        
        
        ######################################################################
        # 거래량 이동평균과 추세 구하기
        ######################################################################
        vma5_m10     = ticker_df_m10['vma5']      = volume_m10.rolling(5).mean()
        vma10_m10    = ticker_df_m10['vma10']     = volume_m10.rolling(10).mean()
        vma20_m10    = ticker_df_m10['vma20']     = volume_m10.rolling(20).mean()
        
        
                       
        ######################################################################
        # 10분봉 이동평균과 추세 구하기
        ###################################################################### 
        ma5_m10    = ticker_df_m10['ma5']      = close_price_m10.rolling(5).mean()
        ma20_m10   = ticker_df_m10['ma20']     = close_price_m10.rolling(20).mean()
        ma60_m10   = ticker_df_m10['ma60']     = close_price_m10.rolling(60).mean()
        ma120_m10  = ticker_df_m10['ma120']    = close_price_m10.rolling(120).mean()
        ma180_m10  = ticker_df_m10['ma180']    = close_price_m10.rolling(180).mean()
        
        ma5_trend_199_m10 = ma5_m10[199] - ma5_m10[198] 
        ma5_trend_198_m10 = ma5_m10[198] - ma5_m10[197] 
        
        ma20_trend_199_m10 = ma20_m10[199] - ma20_m10[198] 
        ma20_trend_198_m10 = ma20_m10[198] - ma20_m10[197] 
        
        
        ######################################################################
        # PRICE CHANNEL 상한선, 하한선, 중앙선 구하기
        ######################################################################   
        max_high_20_m10     = ticker_df_m10['max_high_20']  =  high_price_m10.rolling(20, axis = 0 ).max()    
        max_close_20_m10    = ticker_df_m10['max_close_20'] =  close_price_m10.rolling(20, axis = 0 ).max() 
        min_low_20_m10      = ticker_df_m10['min_low_20']   =  low_price_m10.rolling(20, axis = 0).min() 
        middle_20_m10       = ticker_df_m10['middle_20']    =  (ticker_df_m10['max_high_20'] + ticker_df_m10['min_low_20'])/2
        
        
        ######################################################################
        # PRICE CHANNEL 활용. 일목균형표로 변환
        ######################################################################
        max_high_9_m10      = ticker_df_m10['max_high_9']     =  high_price_m10.rolling(9, axis = 0 ).max()   
        min_low_9_m10       = ticker_df_m10['min_low_9']      =  low_price_m10.rolling(9, axis = 0).min()
        
        max_high_26_m10     = ticker_df_m10['max_high_26']    =  high_price_m10.rolling(26, axis = 0 ).max()   
        min_low_26_m10      = ticker_df_m10['min_low_26']     =  low_price_m10.rolling(26, axis = 0).min()
        
        max_high_52_m10     = ticker_df_m10['max_high_52']    =  high_price_m10.rolling(52, axis = 0 ).max()   
        min_low_52_m10      = ticker_df_m10['min_low_52']     =  low_price_m10.rolling(52, axis = 0).min()
        
        conversion_line_m10 = ticker_df_m10['middle_9']       =  (ticker_df_m10['max_high_9'] + ticker_df_m10['min_low_9'])/2
        base_line_m10       = ticker_df_m10['middle_26']      =  (ticker_df_m10['max_high_26'] + ticker_df_m10['min_low_26'])/2
        
        leading_spanA_m10   = (ticker_df_m10['middle_9'] + ticker_df_m10['middle_26'])/2      # 199 - 26
        leading_spanB_m10   = (ticker_df_m10['max_high_52'] + ticker_df_m10['min_low_52'])/2   # 199 - 26
        
        
        
        
        
        
        
        
        
        
        
        ######################################################################
        # 15분봉데이터 가져오기
        ######################################################################
        ticker_df_m15   = pyupbit.get_ohlcv(ticker, "minute15") 
        open_price_m15  = ticker_df_m15['open']
        high_price_m15  = ticker_df_m15['high']
        low_price_m15   = ticker_df_m15['low']
        close_price_m15 = ticker_df_m15['close']
        volume_m15      = ticker_df_m15['volume']
        
        
        ######################################################################
        # 거래량 이동평균과 추세 구하기
        ######################################################################
        vma5_m15     = ticker_df_m15['vma5']      = volume_m15.rolling(5).mean()
        vma10_m15    = ticker_df_m15['vma10']     = volume_m15.rolling(10).mean()
        vma20_m15    = ticker_df_m15['vma20']     = volume_m15.rolling(20).mean()
        
                       
        ######################################################################
        # 15분봉 이동평균과 추세 구하기
        ###################################################################### 
        ma5_m15    = ticker_df_m15['ma5']      = close_price_m15.rolling(5).mean()
        ma20_m15   = ticker_df_m15['ma20']     = close_price_m15.rolling(20).mean()
        ma60_m15   = ticker_df_m15['ma60']     = close_price_m15.rolling(60).mean()
        ma120_m15  = ticker_df_m15['ma120']    = close_price_m15.rolling(120).mean()
        ma180_m15  = ticker_df_m15['ma180']    = close_price_m15.rolling(180).mean()
        
        ma5_trend_199_m15 = ma5_m15[199] - ma5_m15[198] 
        ma5_trend_198_m15 = ma5_m15[198] - ma5_m15[197] 
        
        ma20_trend_199_m15 = ma20_m15[199] - ma20_m15[198] 
        ma20_trend_198_m15 = ma20_m15[198] - ma20_m15[197] 
        
        
        ######################################################################
        # PRICE CHANNEL 상한선, 하한선, 중앙선 구하기
        ######################################################################   
        max_high_20_m15     = ticker_df_m15['max_high_20']  =  high_price_m15.rolling(20, axis = 0 ).max()    
        max_close_20_m15    = ticker_df_m15['max_close_20'] =  close_price_m15.rolling(20, axis = 0 ).max() 
        min_low_20_m15      = ticker_df_m15['min_low_20']   =  low_price_m15.rolling(20, axis = 0).min() 
        middle_20_m15       = ticker_df_m15['middle_20']    =  (ticker_df_m15['max_high_20'] + ticker_df_m15['min_low_20'])/2
        
        
        ######################################################################
        # PRICE CHANNEL 활용. 일목균형표로 변환
        ######################################################################
        max_high_9_m15      = ticker_df_m15['max_high_9']     =  high_price_m15.rolling(9, axis = 0 ).max()   
        min_low_9_m15       = ticker_df_m15['min_low_9']      =  low_price_m15.rolling(9, axis = 0).min()
        
        max_high_26_m15     = ticker_df_m15['max_high_26']    =  high_price_m15.rolling(26, axis = 0 ).max()   
        min_low_26_m15      = ticker_df_m15['min_low_26']     =  low_price_m15.rolling(26, axis = 0).min()
        
        max_high_52_m15     = ticker_df_m15['max_high_52']    =  high_price_m15.rolling(52, axis = 0 ).max()   
        min_low_52_m15      = ticker_df_m15['min_low_52']     =  low_price_m15.rolling(52, axis = 0).min()
        
        conversion_line_m15 = ticker_df_m15['middle_9']       =  (ticker_df_m15['max_high_9'] + ticker_df_m15['min_low_9'])/2
        base_line_m15       = ticker_df_m15['middle_26']      =  (ticker_df_m15['max_high_26'] + ticker_df_m15['min_low_26'])/2
        
        leading_spanA_m15   = (ticker_df_m15['middle_9'] + ticker_df_m15['middle_26'])/2      # 199 - 26
        leading_spanB_m15   = (ticker_df_m15['max_high_52'] + ticker_df_m15['min_low_52'])/2   # 199 - 26
        
        
        
        
        
        
        
        
        
        ######################################################################
        # 30분봉데이터 가져오기
        ######################################################################
        ticker_df_m30   = pyupbit.get_ohlcv(ticker, "minute30") 
        open_price_m30  = ticker_df_m30['open']
        high_price_m30  = ticker_df_m30['high']
        low_price_m30   = ticker_df_m30['low']
        close_price_m30 = ticker_df_m30['close']
        volume_m30      = ticker_df_m30['volume']
        
        
        ######################################################################
        # 거래량 이동평균과 추세 구하기
        ######################################################################
        vma5_m30     = ticker_df_m30['vma5']      = volume_m30.rolling(5).mean()
        vma10_m30    = ticker_df_m30['vma10']     = volume_m30.rolling(10).mean()
        vma20_m30    = ticker_df_m30['vma20']     = volume_m30.rolling(20).mean()
        
                       
        ######################################################################
        # 30분봉 이동평균과 추세 구하기
        ###################################################################### 
        ma5_m30    = ticker_df_m30['ma5']      = close_price_m30.rolling(5).mean()
        ma20_m30   = ticker_df_m30['ma20']     = close_price_m30.rolling(20).mean()
        ma60_m30   = ticker_df_m30['ma60']     = close_price_m30.rolling(60).mean()
        ma120_m30  = ticker_df_m30['ma120']    = close_price_m30.rolling(120).mean()
        ma180_m30  = ticker_df_m30['ma180']    = close_price_m30.rolling(180).mean()
        
        ma5_trend_199_m30 = ma5_m30[199] - ma5_m30[198] 
        ma5_trend_198_m30 = ma5_m30[198] - ma5_m30[197] 
        
        ma20_trend_199_m30 = ma20_m30[199] - ma20_m30[198] 
        ma20_trend_198_m30 = ma20_m30[198] - ma20_m30[197] 
        
        
        ######################################################################
        # PRICE CHANNEL 상한선, 하한선, 중앙선 구하기
        ######################################################################   
        max_high_20_m30     = ticker_df_m30['max_high_20']  =  high_price_m30.rolling(20, axis = 0 ).max()    
        max_close_20_m30    = ticker_df_m30['max_close_20'] =  close_price_m30.rolling(20, axis = 0 ).max() 
        min_low_20_m30      = ticker_df_m30['min_low_20']   =  low_price_m30.rolling(20, axis = 0).min() 
        middle_20_m30       = ticker_df_m30['middle_20']    =  (ticker_df_m30['max_high_20'] + ticker_df_m30['min_low_20'])/2
        
        
        ######################################################################
        # PRICE CHANNEL 활용. 일목균형표로 변환
        ######################################################################
        max_high_9_m30      = ticker_df_m30['max_high_9']     =  high_price_m30.rolling(9, axis = 0 ).max()   
        min_low_9_m30       = ticker_df_m30['min_low_9']      =  low_price_m30.rolling(9, axis = 0).min()
        
        max_high_26_m30     = ticker_df_m30['max_high_26']    =  high_price_m30.rolling(26, axis = 0 ).max()   
        min_low_26_m30      = ticker_df_m30['min_low_26']     =  low_price_m30.rolling(26, axis = 0).min()
        
        max_high_52_m30     = ticker_df_m30['max_high_52']    =  high_price_m30.rolling(52, axis = 0 ).max()   
        min_low_52_m30      = ticker_df_m30['min_low_52']     =  low_price_m30.rolling(52, axis = 0).min()
        
        conversion_line_m30 = ticker_df_m30['middle_9']       =  (ticker_df_m30['max_high_9'] + ticker_df_m30['min_low_9'])/2
        base_line_m30       = ticker_df_m30['middle_26']      =  (ticker_df_m30['max_high_26'] + ticker_df_m30['min_low_26'])/2
        
        leading_spanA_m30   = (ticker_df_m30['middle_9'] + ticker_df_m30['middle_26'])/2      # 199 - 26
        leading_spanB_m30   = (ticker_df_m30['max_high_52'] + ticker_df_m30['min_low_52'])/2   # 199 - 26
        
        
        
        
        
        
        
        
        
        
        
        ######################################################################
        # 60분봉데이터 가져오기
        ######################################################################
        ticker_df_m60   = pyupbit.get_ohlcv(ticker, "minute60") 
        open_price_m60  = ticker_df_m60['open']
        high_price_m60  = ticker_df_m60['high']
        low_price_m60   = ticker_df_m60['low']
        close_price_m60 = ticker_df_m60['close']
        volume_m60      = ticker_df_m60['volume']
        
        
        ######################################################################
        # 거래량 이동평균과 추세 구하기
        ######################################################################
        vma5_m60     = ticker_df_m60['vma5']      = volume_m60.rolling(5).mean()
        vma10_m60    = ticker_df_m60['vma10']     = volume_m60.rolling(10).mean()
        vma20_m60    = ticker_df_m60['vma20']     = volume_m60.rolling(20).mean()
        
                       
        ######################################################################
        # 60분봉 이동평균과 추세 구하기
        ###################################################################### 
        ma5_m60    = ticker_df_m60['ma5']      = close_price_m60.rolling(5).mean()
        ma20_m60   = ticker_df_m60['ma20']     = close_price_m60.rolling(20).mean()
        ma60_m60   = ticker_df_m60['ma60']     = close_price_m60.rolling(60).mean()
        ma120_m60  = ticker_df_m60['ma120']    = close_price_m60.rolling(120).mean()
        ma180_m60  = ticker_df_m60['ma180']    = close_price_m60.rolling(180).mean()
        
        ma5_trend_199_m60 = ma5_m60[199] - ma5_m60[198] 
        ma5_trend_198_m60 = ma5_m60[198] - ma5_m60[197] 
        
        ma20_trend_199_m60 = ma20_m60[199] - ma20_m60[198] 
        ma20_trend_198_m60 = ma20_m60[198] - ma20_m60[197] 
        
        
        ######################################################################
        # PRICE CHANNEL 상한선, 하한선, 중앙선 구하기
        ######################################################################   
        max_high_20_m60     = ticker_df_m60['max_high_20']  =  high_price_m60.rolling(20, axis = 0 ).max()    
        max_close_20_m60    = ticker_df_m60['max_close_20'] =  close_price_m60.rolling(20, axis = 0 ).max() 
        min_low_20_m60      = ticker_df_m60['min_low_20']   =  low_price_m60.rolling(20, axis = 0).min() 
        middle_20_m60       = ticker_df_m60['middle_20']    =  (ticker_df_m60['max_high_20'] + ticker_df_m60['min_low_20'])/2
        
        
        ######################################################################
        # PRICE CHANNEL 활용. 일목균형표로 변환
        ######################################################################
        max_high_9_m60      = ticker_df_m60['max_high_9']     =  high_price_m60.rolling(9, axis = 0 ).max()   
        min_low_9_m60       = ticker_df_m60['min_low_9']      =  low_price_m60.rolling(9, axis = 0).min()
        
        max_high_26_m60     = ticker_df_m60['max_high_26']    =  high_price_m60.rolling(26, axis = 0 ).max()   
        min_low_26_m60      = ticker_df_m60['min_low_26']     =  low_price_m60.rolling(26, axis = 0).min()
        
        max_high_52_m60     = ticker_df_m60['max_high_52']    =  high_price_m60.rolling(52, axis = 0 ).max()   
        min_low_52_m60      = ticker_df_m60['min_low_52']     =  low_price_m60.rolling(52, axis = 0).min()
        
        conversion_line_m60 = ticker_df_m60['middle_9']       =  (ticker_df_m60['max_high_9'] + ticker_df_m60['min_low_9'])/2
        base_line_m60       = ticker_df_m60['middle_26']      =  (ticker_df_m60['max_high_26'] + ticker_df_m60['min_low_26'])/2
        
        leading_spanA_m60   = (ticker_df_m60['middle_9'] + ticker_df_m60['middle_26'])/2      # 199 - 26
        leading_spanB_m60   = (ticker_df_m60['max_high_52'] + ticker_df_m60['min_low_52'])/2   # 199 - 26
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        ######################################################################
        # 240분봉데이터 가져오기
        ######################################################################
        ticker_df_m240   = pyupbit.get_ohlcv(ticker, "minute240") 
        open_price_m240  = ticker_df_m240['open']
        high_price_m240  = ticker_df_m240['high']
        low_price_m240   = ticker_df_m240['low']
        close_price_m240 = ticker_df_m240['close']
        volume_m240      = ticker_df_m240['volume']
        
        
        ######################################################################
        # 거래량 이동평균과 추세 구하기
        ######################################################################
        vma5_m240     = ticker_df_m240['vma5']      = volume_m240.rolling(5).mean()
        vma10_m240    = ticker_df_m240['vma10']     = volume_m240.rolling(10).mean()
        vma20_m240    = ticker_df_m240['vma20']     = volume_m240.rolling(20).mean()
        
                       
        ######################################################################
        # 240분봉 이동평균과 추세 구하기
        ###################################################################### 
        ma5_m240    = ticker_df_m240['ma5']      = close_price_m240.rolling(5).mean()
        ma20_m240   = ticker_df_m240['ma20']     = close_price_m240.rolling(20).mean()
        ma60_m240   = ticker_df_m240['ma60']     = close_price_m240.rolling(60).mean()
        ma120_m240  = ticker_df_m240['ma120']    = close_price_m240.rolling(120).mean()
        ma180_m240  = ticker_df_m240['ma180']    = close_price_m240.rolling(180).mean()
        
        ma5_trend_199_m240 = ma5_m240[199] - ma5_m240[198] 
        ma5_trend_198_m240 = ma5_m240[198] - ma5_m240[197] 
        
        ma20_trend_199_m240 = ma20_m240[199] - ma20_m240[198] 
        ma20_trend_198_m240 = ma20_m240[198] - ma20_m240[197] 
        
        
        ######################################################################
        # PRICE CHANNEL 상한선, 하한선, 중앙선 구하기
        ######################################################################   
        max_high_20_m240     = ticker_df_m240['max_high_20']  =  high_price_m240.rolling(20, axis = 0 ).max()    
        max_close_20_m240    = ticker_df_m240['max_close_20'] =  close_price_m240.rolling(20, axis = 0 ).max() 
        min_low_20_m240      = ticker_df_m240['min_low_20']   =  low_price_m240.rolling(20, axis = 0).min() 
        middle_20_m240       = ticker_df_m240['middle_20']    =  (ticker_df_m240['max_high_20'] + ticker_df_m240['min_low_20'])/2
        
        
        ######################################################################
        # PRICE CHANNEL 활용. 일목균형표로 변환
        ######################################################################
        max_high_9_m240      = ticker_df_m240['max_high_9']     =  high_price_m240.rolling(9, axis = 0 ).max()   
        min_low_9_m240       = ticker_df_m240['min_low_9']      =  low_price_m240.rolling(9, axis = 0).min()
        
        max_high_26_m240     = ticker_df_m240['max_high_26']    =  high_price_m240.rolling(26, axis = 0 ).max()   
        min_low_26_m240      = ticker_df_m240['min_low_26']     =  low_price_m240.rolling(26, axis = 0).min()
        
        max_high_52_m240     = ticker_df_m240['max_high_52']    =  high_price_m240.rolling(52, axis = 0 ).max()   
        min_low_52_m240      = ticker_df_m240['min_low_52']     =  low_price_m240.rolling(52, axis = 0).min()
        
        conversion_line_m240 = ticker_df_m240['middle_9']       =  (ticker_df_m240['max_high_9'] + ticker_df_m240['min_low_9'])/2
        base_line_m240       = ticker_df_m240['middle_26']      =  (ticker_df_m240['max_high_26'] + ticker_df_m240['min_low_26'])/2
        
        leading_spanA_m240   = (ticker_df_m240['middle_9'] + ticker_df_m240['middle_26'])/2      # 199 - 26
        leading_spanB_m240   = (ticker_df_m240['max_high_52'] + ticker_df_m240['min_low_52'])/2   # 199 - 26
        
        
        
        
        
        
        
        
        
        
        
        
        ######################################################################
        # 일봉봉데이터 가져오기
        ######################################################################
        ticker_df_day   = pyupbit.get_ohlcv(ticker) 
        open_price_day  = ticker_df_day['open']
        high_price_day  = ticker_df_day['high']
        low_price_day   = ticker_df_day['low']
        close_price_day = ticker_df_day['close']
        volume_day      = ticker_df_day['volume']
        
        
        ######################################################################
        # 거래량 이동평균과 추세 구하기
        ######################################################################
        vma5_day     = ticker_df_day['vma5']      = volume_day.rolling(5).mean()
        vma10_day    = ticker_df_day['vma10']     = volume_day.rolling(10).mean()
        vma20_day    = ticker_df_day['vma20']     = volume_day.rolling(20).mean()
        
                       
        ######################################################################
        # 일봉 이동평균과 추세 구하기
        ###################################################################### 
        ma5_day    = ticker_df_day['ma5']      = close_price_day.rolling(5).mean()
        ma20_day   = ticker_df_day['ma20']     = close_price_day.rolling(20).mean()
        ma60_day   = ticker_df_day['ma60']     = close_price_day.rolling(60).mean()
        ma120_day  = ticker_df_day['ma120']    = close_price_day.rolling(120).mean()
        ma180_day  = ticker_df_day['ma180']    = close_price_day.rolling(180).mean()
        
        ma5_trend_199_day = ma5_day[-1] - ma5_day[-2] 
        ma5_trend_198_day = ma5_day[-2] - ma5_day[-3] 
        
        ma20_trend_199_day = ma20_day[-1] - ma20_day[-2] 
        ma20_trend_198_day = ma20_day[-2] - ma20_day[-3]
        
        
        ######################################################################
        # PRICE CHANNEL 상한선, 하한선, 중앙선 구하기
        ######################################################################   
        max_high_20_day     = ticker_df_day['max_high_20']  =  high_price_day.rolling(20, axis = 0 ).max()    
        max_close_20_day    = ticker_df_day['max_close_20'] =  close_price_day.rolling(20, axis = 0 ).max() 
        min_low_20_day      = ticker_df_day['min_low_20']   =  low_price_day.rolling(20, axis = 0).min() 
        middle_20_day       = ticker_df_day['middle_20']    =  (ticker_df_day['max_high_20'] + ticker_df_day['min_low_20'])/2
        
        
        ######################################################################
        # PRICE CHANNEL 활용. 일목균형표로 변환
        ######################################################################
        max_high_9_day      = ticker_df_day['max_high_9']     =  high_price_day.rolling(9, axis = 0 ).max()   
        min_low_9_day       = ticker_df_day['min_low_9']      =  low_price_day.rolling(9, axis = 0).min()
        
        max_high_26_day     = ticker_df_day['max_high_26']    =  high_price_day.rolling(26, axis = 0 ).max()   
        min_low_26_day      = ticker_df_day['min_low_26']     =  low_price_day.rolling(26, axis = 0).min()
        
        max_high_52_day     = ticker_df_day['max_high_52']    =  high_price_day.rolling(52, axis = 0 ).max()   
        min_low_52_day      = ticker_df_day['min_low_52']     =  low_price_day.rolling(52, axis = 0).min()
        
        conversion_line_day = ticker_df_day['middle_9']       =  (ticker_df_day['max_high_9'] + ticker_df_day['min_low_9'])/2
        base_line_day       = ticker_df_day['middle_26']      =  (ticker_df_day['max_high_26'] + ticker_df_day['min_low_26'])/2
        
        leading_spanA_day   = (ticker_df_day['middle_9'] + ticker_df_day['middle_26'])/2      # 199 - 26
        leading_spanB_day   = (ticker_df_day['max_high_52'] + ticker_df_day['min_low_52'])/2   # 199 - 26
        
        
        
        
        
        
        ######################################################################
        # 전고점 돌파 여부 확인 
        ######################################################################
        min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min1'])
        min3   = float(operation_df.loc[(operation_df.ticker == ticker), 'min3'])
        min5   = float(operation_df.loc[(operation_df.ticker == ticker), 'min5'])
        min10  = float(operation_df.loc[(operation_df.ticker == ticker), 'min10'])
        min15  = float(operation_df.loc[(operation_df.ticker == ticker), 'min15'])
        min30  = float(operation_df.loc[(operation_df.ticker == ticker), 'min30'])
        min60  = float(operation_df.loc[(operation_df.ticker == ticker), 'min60'])
        min240 = float(operation_df.loc[(operation_df.ticker == ticker), 'min240'])
        day    = float(operation_df.loc[(operation_df.ticker == ticker), 'day'])
        
        
        if (min1 == 0 and
            vma5_m1[-1] > vma10_m1[-1] and
            vma10_m1[-1] > vma20_m1[-1] and
            current_price > leading_spanA_m1[-26] and 
            current_price > leading_spanB_m1[-26]) :
            if (high_price_m1[-1] > max_high_20_m1[-2] or
                max_high_20_m1[-1] > max_high_20_m1[-2]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min1'] = 1
                min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min1'])
                bot.sendMessage(chat_id = tlgm_id, text = 
                                '\nCO: '+ticker+
                                '\nCD: min1 UP' +  
                                '\nCP: ' + str(round(current_price,2)))
            
        if (min3 == 0 and 
            vma5_m3[-1] > vma10_m3[-1] and
            vma10_m3[-1] > vma20_m3[-1] and
            current_price > leading_spanA_m3[-26] and 
            current_price > leading_spanB_m3[-26] and 
            min1 == 1 ) :
            if (high_price_m3[-1] > max_high_20_m3[-2] or
                max_high_20_m3[-1] > max_high_20_m3[-2]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min3'] = 1
                min3   = float(operation_df.loc[(operation_df.ticker == ticker), 'min3'])
                bot.sendMessage(chat_id = tlgm_id, text = 
                                '\nCO: '+ticker+
                                '\nCD: min3 UP' +  
                                '\nCP: ' + str(round(current_price,2)))
            
        if (min5 == 0 and
            vma5_m5[-1] > vma10_m5[-1] and
            vma10_m5[-1] > vma20_m5[-1] and
            current_price > leading_spanA_m5[-26] and 
            current_price > leading_spanB_m5[-26] and
            min3 == 1 ) :
            if (high_price_m5[-1] > max_high_20_m5[-2] or
                max_high_20_m5[-1] > max_high_20_m5[-2]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min5'] = 1
                min5   = float(operation_df.loc[(operation_df.ticker == ticker), 'min5'])
                bot.sendMessage(chat_id = tlgm_id, text = 
                                '\nCO: '+ticker+
                                '\nCD: min5 UP' +  
                                '\nCP: ' + str(round(current_price,2)))
            
        if (min10 == 0 and
            vma5_m10[-1] > vma10_m10[-1] and
            vma10_m10[-1] > vma20_m10[-1] and
            current_price > leading_spanA_m10[-26] and 
            current_price > leading_spanB_m10[-26] and
            min5 == 1 ) :
            if (high_price_m10[-1] > max_high_20_m10[-2] or
                max_high_20_m10[-1] > max_high_20_m10[-2]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min10'] = 1
                min10   = float(operation_df.loc[(operation_df.ticker == ticker), 'min10'])
                bot.sendMessage(chat_id = tlgm_id, text = 
                                '\nCO: '+ticker+
                                '\nCD: min10 UP' +  
                                '\nCP: ' + str(round(current_price,2)))
            
        if (min15 == 0 and
            vma5_m15[-1] > vma10_m15[-1] and
            vma10_m15[-1] > vma20_m15[-1] and
            current_price > leading_spanA_m15[-26] and 
            current_price > leading_spanB_m15[-26] and
            min10 == 1 ) :
            if (high_price_m15[-1] > max_high_20_m15[-2] or
                max_high_20_m15[-1] > max_high_20_m15[-2]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min15'] = 1
                min15   = float(operation_df.loc[(operation_df.ticker == ticker), 'min15'])
                bot.sendMessage(chat_id = tlgm_id, text = 
                                '\nCO: '+ticker+
                                '\nCD: min15 UP' +  
                                '\nCP: ' + str(round(current_price,2)))
            
        if (min30 == 0 and
            vma5_m30[-1] > vma10_m30[-1] and
            vma10_m30[-1] > vma20_m30[-1] and
            current_price > leading_spanA_m30[-26] and 
            current_price > leading_spanB_m30[-26] and
            min15 == 1 ) :
            if (high_price_m30[-1] > max_high_20_m30[-2] or
                max_high_20_m30[-1] > max_high_20_m30[-2]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min30'] = 1
                min30   = float(operation_df.loc[(operation_df.ticker == ticker), 'min30'])
                bot.sendMessage(chat_id = tlgm_id, text = 
                                '\nCO: '+ticker+
                                '\nCD: min30 UP' +  
                                '\nCP: ' + str(round(current_price,2)))
            
        if (min60 == 0 and
            vma5_m60[-1] > vma10_m60[-1] and
            vma10_m60[-1] > vma20_m60[-1] and
            current_price > leading_spanA_m60[-26] and 
            current_price > leading_spanB_m60[-26] and
            min30 == 1 ) :
            if (high_price_m60[-1] > max_high_20_m60[-2] or
                max_high_20_m60[-1] > max_high_20_m60[-2]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min60'] = 1
                min60   = float(operation_df.loc[(operation_df.ticker == ticker), 'min60'])
                bot.sendMessage(chat_id = tlgm_id, text = 
                                '\nCO: '+ticker+
                                '\nCD: min60 UP' +  
                                '\nCP: ' + str(round(current_price,2)))
            
        if (min240 == 0 and
            vma5_m240[-1] > vma10_m240[-1] and
            vma10_m240[-1] > vma20_m240[-1] and
            current_price > leading_spanA_m240[-26] and 
            current_price > leading_spanB_m240[-26] and
            min60 == 1 ) :
            if (high_price_m240[-1] > max_high_20_m240[-2] or
                max_high_20_m240[-1] > max_high_20_m240[-2]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min240'] = 1
                min240   = float(operation_df.loc[(operation_df.ticker == ticker), 'min240'])
                bot.sendMessage(chat_id = tlgm_id, text = 
                                '\nCO: '+ticker+
                                '\nCD: min240 UP' +  
                                '\nCP: ' + str(round(current_price,2)))
            
        if (day == 0 and
            vma5_day[-1] > vma10_day[-1] and
            vma10_day[-1] > vma20_day[-1] and
            current_price > leading_spanA_day[-26] and 
            current_price > leading_spanB_day[-26] and
            min240 == 1 ) :
            if (high_price_day[-1] > max_high_20_day[-2] or
                max_high_20_day[-1] > max_high_20_day[-2]) :
                operation_df.loc[(operation_df.ticker == ticker), 'day'] = 1
                day   = float(operation_df.loc[(operation_df.ticker == ticker), 'day'])
                bot.sendMessage(chat_id = tlgm_id, text = 
                                '\nCO: '+ticker+
                                '\nCD: day UP' +  
                                '\nCP: ' + str(round(current_price,2)))

            
            
        
        ######################################################################
        # 하락추세 전환 확인
        ######################################################################
        if (min1 == 1 and
            current_price < leading_spanA_m1[-26] and 
            current_price < leading_spanB_m1[-26] and
            current_price < middle_20_m1[-1]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min1'] = 0
                min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min1'])
                
        
        if (min3 == 1 and
            current_price < leading_spanA_m3[-26] and 
            current_price < leading_spanB_m3[-26] and
            current_price < middle_20_m3[-1]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min3'] = 0
                min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min3'])
                
        if (min5 == 1 and
            current_price < leading_spanA_m5[-26] and 
            current_price < leading_spanB_m5[-26] and
            current_price < middle_20_m5[-1]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min5'] = 0
                min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min5'])
                
        if (min10 == 1 and
            current_price < leading_spanA_m10[-26] and 
            current_price < leading_spanB_m10[-26] and
            current_price < middle_20_m10[-1]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min10'] = 0
                min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min10'])
                
        if (min15 == 1 and
            current_price < leading_spanA_m15[-26] and 
            current_price < leading_spanB_m15[-26] and
            current_price < middle_20_m15[-1]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min15'] = 0
                min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min15'])
                
        if (min30 == 1 and
            current_price < leading_spanA_m30[-26] and 
            current_price < leading_spanB_m30[-26] and
            current_price < middle_20_m30[-1]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min30'] = 0
                min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min30'])
                
        if (min60 == 1 and
            current_price < leading_spanA_m60[-26] and 
            current_price < leading_spanB_m60[-26] and
            current_price < middle_20_m60[-1]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min60'] = 0
                min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min60'])
                
        if (min240 == 1 and
            current_price < leading_spanA_m240[-26] and 
            current_price < leading_spanB_m240[-26] and
            current_price < middle_20_m240[-1]) :
                operation_df.loc[(operation_df.ticker == ticker), 'min240'] = 0
                min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'min240'])
                
        if (day == 1 and
            current_price < leading_spanA_day[-26] and 
            current_price < leading_spanB_day[-26] and
            current_price < middle_20_m240[-1]) :
                operation_df.loc[(operation_df.ticker == ticker), 'day'] = 0
                min1   = float(operation_df.loc[(operation_df.ticker == ticker), 'day'])
        
        
        
        
        
        d1 = ((max_high_20_m1[-2] - current_price)/current_price)*100
        d3 = ((max_high_20_m3[-2] - current_price)/current_price)*100
        d5 = ((max_high_20_m5[-2] - current_price)/current_price)*100
        d10 = ((max_high_20_m10[-2] - current_price)/current_price)*100
        d15 = ((max_high_20_m15[-2] - current_price)/current_price)*100
        d30 = ((max_high_20_m30[-2] - current_price)/current_price)*100
        d60 = ((max_high_20_m60[-2] - current_price)/current_price)*100
        d240 = ((max_high_20_m240[-2] - current_price)/current_price)*100
        dday = ((max_high_20_day[-2] - current_price)/current_price)*100
        
        disparity = ((d1+d3+d5+d10+d15+d30+d60+d240+dday)/9)
        
        ######################################################################
        # 정규 출력
        ###################################################################### 
        print(time.strftime('%H:%M:%S'), 
              ticker.ljust(10), 
              "VC:", str(round(volume_checker/1000000)).rjust(5),
              " ",
              
              round(min1), 
              round(min3), 
              round(min5), 
              round(min10), 
              round(min15), 
              round(min30), 
              round(min60), 
              round(min240), 
              round(day),
              " ",
              "DP:",str(round(disparity,1)).ljust(5),
              str(round(((max_high_20_m1[-2] - current_price)/current_price)*100)).rjust(3),
              str(round(((max_high_20_m3[-2] - current_price)/current_price)*100)).rjust(3),
              str(round(((max_high_20_m5[-2] - current_price)/current_price)*100)).rjust(3),
              str(round(((max_high_20_m10[-2] - current_price)/current_price)*100)).rjust(3),
              str(round(((max_high_20_m15[-2] - current_price)/current_price)*100)).rjust(3),
              str(round(((max_high_20_m30[-2] - current_price)/current_price)*100)).rjust(3),
              str(round(((max_high_20_m60[-2] - current_price)/current_price)*100)).rjust(3),
              str(round(((max_high_20_m240[-2] - current_price)/current_price)*100)).rjust(3),
              str(round(((max_high_20_day[-2] - current_price)/current_price)*100)).rjust(3),
              " ",
              "CH:", str(round(((high_price_day[-1] - current_price)/current_price)*100,1)).rjust(5),
              " ",
              "OH:", str(round(((high_price_day[-1] - open_price_day[-1])/open_price_day[-1])*100, 1)).rjust(5)
              )
        if ticker == "KRW-NEO" :
            print('---------------------------------------------------------------------------------------------------------------------------')
        
            
        
        #print(round(min1), round(min3), round(min5), round(min10), round(min15), round(min30), round(min60), round(min240), round(day))
        #print("CP   :",str(current_price)) 
        
        '''
        # 값 일치 여부 확인을 위한 프린트
        print("거래량 5이평", round(vma5_m1[-1],2))
        print("거래량10이평", round(vma10_m1[-1],2))
        print("거래량20이평", round(vma20_m1[-1],2))
        print("선행스팬1   ", round(leading_spanA_m1[-26],2))
        print("선행스팬2   ", round(leading_spanB_m1[-26],2))
        print("현재고가    ", round(high_price_m1[-1],2))
        print("전고점      ", round(max_high_20_m1[-2],2))
        
    
        
        print("01   :",
              "%:", 
              str(round(((max_high_20_m1[198] - current_price)/current_price)*100,2)).ljust(7),
              "   05T:",
              1 if ma5_trend_199_m1 > 0 else 0,
              "   05M:",
              1 if ma5_m1[-1] > middle_20_m1[198] else 0, 
              "   05C:",
              1 if current_price > leading_spanA_m1[-26] and current_price > leading_spanB_m1[-26] else 0,    
              "   VAA:",
              1 if vma5_m1[-1] > vma10_m1[-1] and vma10_m1[-1] > vma20_m1[-1] else 0,
              "   PCU:", 
              str(round(max_high_20_m1[198],2)).ljust(12)              
              ) 
        
        
        
        print("03   :",
              "%:", 
              str(round(((max_high_20_m3[198] - max_high_20_m1[198])/max_high_20_m1[198]),2)).ljust(7),
              "   05T:", 
              1 if ma5_trend_199_m3 > 0 else 0, 
              "   05M:",
              1 if ma5_m3[-1] > middle_20_m3[198] else 0, 
              "   05C:",
              1 if current_price > leading_spanA_m3[-26] and current_price > leading_spanB_m3[-26] else 0, 
              "   VAA:",
              1 if vma5_m3[-1] > vma10_m3[-1] and vma10_m3[-1] > vma20_m3[-1] else 0,
              "   PCU:",
              str(round(max_high_20_m3[198],2)).ljust(11)              
              ) 
                       
        
        print("05   :",
              "%:", 
              str(round(((max_high_20_m5[198] - max_high_20_m1[198])/max_high_20_m1[198]),2)).ljust(7),
              "   05T:", 
              1 if ma5_trend_199_m5 > 0 else 0, 
              "   05M:",
              1 if ma5_m5[-1] > middle_20_m5[198] else 0, 
              "   05C:",
              1 if current_price > leading_spanA_m5[-26] and current_price > leading_spanB_m5[-26] else 0, 
              "   VAA:",
              1 if vma5_m5[-1] > vma10_m5[-1] and vma10_m5[-1] > vma20_m5[-1] else 0,
              "   PCU:",
              str(round(max_high_20_m5[198],2)).ljust(11)              
              ) 
        
        
        print("10   :",
              "%:", 
              str(round(((max_high_20_m10[198] - max_high_20_m1[198])/max_high_20_m1[198]),2)).ljust(7),
              "   05T:", 
              1 if ma5_trend_199_m10 > 0 else 0, 
              "   05M:",
              1 if ma5_m10[-1] > middle_20_m10[198] else 0, 
              "   05C:",
              1 if current_price > leading_spanA_m10[-26] and current_price > leading_spanB_m10[-26] else 0, 
              "   VAA:",
              1 if vma5_m10[-1] > vma10_m10[-1] and vma10_m10[-1] > vma20_m10[-1] else 0,
              "   PCU:",
              str(round(max_high_20_m10[198],2)).ljust(11)              
              ) 
        
        
        print("15   :",
              "%:", 
              str(round(((max_high_20_m15[198] - max_high_20_m1[198])/max_high_20_m1[198]),2)).ljust(7),
              "   05T:", 
              1 if ma5_trend_199_m15 > 0 else 0, 
              "   05M:",
              1 if ma5_m15[-1] > middle_20_m15[198] else 0, 
              "   05C:",
              1 if current_price > leading_spanA_m15[-26] and current_price > leading_spanB_m15[-26] else 0, 
              "   VAA:",
              1 if vma5_m15[-1] > vma10_m15[-1] and vma10_m15[-1] > vma20_m15[-1] else 0,
              "   PCU:",
              str(round(max_high_20_m15[198],2)).ljust(11)              
              ) 
        
        
        print("30   :",
              "%:", 
              str(round(((max_high_20_m30[198] - max_high_20_m1[198])/max_high_20_m1[198]),2)).ljust(7),
              "   05T:", 
              1 if ma5_trend_199_m30 > 0 else 0, 
              "   05M:",
              1 if ma5_m30[-1] > middle_20_m30[198] else 0, 
              "   05C:",
              1 if current_price > leading_spanA_m30[-26] and current_price > leading_spanB_m30[-26] else 0, 
              "   VAA:",
              1 if vma5_m30[-1] > vma10_m30[-1] and vma10_m30[-1] > vma20_m30[-1] else 0,
              "   PCU:",
              str(round(max_high_20_m30[198],2)).ljust(11)              
              ) 
        
        
        print("60   :",
              "%:", 
              str(round(((max_high_20_m60[198] - max_high_20_m1[198])/max_high_20_m1[198]),2)).ljust(7),
              "   05T:", 
              1 if ma5_trend_199_m60 > 0 else 0, 
              "   05M:",
              1 if ma5_m60[-1] > middle_20_m60[198] else 0, 
              "   05C:",
              1 if current_price > leading_spanA_m60[-26] and current_price > leading_spanB_m60[-26] else 0, 
              "   VAA:",
              1 if vma5_m60[-1] > vma10_m60[-1] and vma10_m60[-1] > vma20_m60[-1] else 0,
              "   PCU:",
              str(round(max_high_20_m60[198],2)).ljust(11)              
              ) 
        
        
        print("240  :",
              "%:", 
              str(round(((max_high_20_m240[198] - max_high_20_m1[198])/max_high_20_m1[198]),2)).ljust(7),
              "   05T:", 
              1 if ma5_trend_199_m240 > 0 else 0, 
              "   05M:",
              1 if ma5_m240[-1] > middle_20_m240[198] else 0, 
              "   05C:",
              1 if current_price > leading_spanA_m240[-26] and current_price > leading_spanB_m240[-26] else 0, 
              "   VAA:",
              1 if vma5_m240[-1] > vma10_m240[-1] and vma10_m240[-1] > vma20_m240[-1] else 0,
              "   PCU:",
              str(round(max_high_20_m240[198],2)).ljust(11)              
              ) 
        
        
        print("DAY  :",
              "%:", 
              str(round(((max_high_20_day[-2] - max_high_20_m1[-2])/max_high_20_m1[198]),2)).ljust(7),
              "   05T:", 
              1 if ma5_trend_199_day > 0 else 0, 
              "   05M:",
              1 if ma5_day[-1] > middle_20_day[-2] else 0, 
              "   05C:",
              1 if current_price > leading_spanA_day[-26] and current_price > leading_spanB_day[-26] else 0, 
              "   VAA:",
              1 if vma5_day[-1] > vma10_day[-1] and vma10_day[-1] > vma20_day[-1] else 0,
              "   PCU:",
              str(round(max_high_20_day[-2],2)).ljust(11)              
              ) 
        
        
        #print(1 if current_price > middle_20_day[-2] and current_price > leading_spanA_day[173] and current_price > leading_spanB_day[173] else 0)
        '''
        #print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
        
        
        
        ######################################################################
        # 0.5초 간격으로 티커별 현황조회
        ######################################################################  
        time.sleep(0.5)
        
        