from tiingo import TiingoClient
import pandas as pd
from datetime import datetime as dt 
import datetime



client = TiingoClient({'api_key':'YOUR-KEY'})
start_date = dt.today() - datetime.timedelta(days=365)
end_date = str(dt.today().strftime('%Y-%m-%d'))



def get_tickers(tickers,start_date,end_date):
     
    ticker_dataframe = client.get_dataframe(tickers,
                                      frequency ='daily',
                                      metric_name = 'adjClose', 
                                      startDate = start_date,
                                      endDate = end_date)
    
    ticker_dataframe = ticker_dataframe.iloc[::-1]
    
    return ticker_dataframe



def rsc_algo_test(dataframe,timeframe):
    columns = list(dataframe)
    base_instrument = dataframe.columns.values[-1]
    sorted_symbols=[]
    
    for column in columns:
        if column == base_instrument:
            continue
        sorted_symbols.append(tuple((column,(dataframe[column][timeframe] / dataframe[base_instrument][timeframe])[::-1].pct_change().sum(),dataframe[column][0],
                                     round((dataframe[column][timeframe][::-1].pct_change().sum())*100,2),base_instrument))) # output tuple with ticker,rsc
        
        sorted_symbols.sort( key=lambda x: x[1],reverse=True)
    return sorted_symbols



# get the sector into the list of stocks 
def flatten(input_list):
    output_list = []
    for element in input_list:
        if type(element) == list:
            output_list.extend(flatten(element))
        else:
            output_list.append(element)
    return output_list



sectors = ['XLE','XLU','XLK','XLB','XLP','XLY','XLI','XLC','XLV','XLF','XLRE','SPY']
sectors_app_stocks = ['XLE','XLU','XLK','XLB','XLP','XLY','XLI','XLC','XLV','XLF','XLRE']



# update ticker holdings in sectors
sector_stock_list = ['xle','xlu','xlk','xlb','xlp','xly','xli','xlc','xlv','xlf','xlre']



# fetch the actual ticker holdings in the sectors and clean the list of unwanted strings
xle,xlu,xlk,xlb,xlp,xly,xli,xlc,xlv,xlf,xlre = (pd.read_csv('https://www.sectorspdr.com/sectorspdr/IDCO.Client.Spdrs.Portfolio/Export/ExportCsv?symbol='+str(x))
                                                            for x in sector_stock_list)

sector_csv_list  = [xle,xlu,xlk,xlb,xlp,xly,xli,xlc,xlv,xlf,xlre] 

xle_tickers,xlu_tickers,xlk_tickers,xlb_tickers,xlp_tickers,xly_tickers,xli_tickers,xlc_tickers,xlv_tickers,xlf_tickers,xlre_tickers =(list(x.index.get_level_values(0)) 
                                                                                                                                       for x in sector_csv_list)

ticker_list = [xle_tickers,xlu_tickers,xlk_tickers,xlb_tickers,xlp_tickers,xly_tickers,xli_tickers,xlc_tickers,xlv_tickers,xlf_tickers,xlre_tickers]


ticker_list_re = [xle_tickers,xlu_tickers,xlk_tickers,xlb_tickers,xlp_tickers,xly_tickers,xli_tickers,xlc_tickers,xlv_tickers,xlf_tickers,xlre_tickers]

xle_tickers,xlu_tickers,xlk_tickers,xlb_tickers,xlp_tickers,xly_tickers,xli_tickers,xlc_tickers,xlv_tickers,xlf_tickers,xlre_tickers = [i[1:] 
                                                                                                                                        for i in ticker_list_re]


stock_tickers = [xle_tickers,xlu_tickers,xlk_tickers,xlb_tickers,xlp_tickers,xly_tickers,xli_tickers,xlc_tickers,xlv_tickers,xlf_tickers,xlre_tickers ]

xle_tickers,xlu_tickers,xlk_tickers,xlb_tickers,xlp_tickers,xly_tickers,xli_tickers,xlc_tickers,xlv_tickers,xlf_tickers,xlre_tickers = map(list,zip(
                                                                                                                        stock_tickers,sectors_app_stocks))

stock_tickers_test = [xle_tickers,xlu_tickers,xlk_tickers,xlb_tickers,xlp_tickers,xly_tickers,xli_tickers,xlc_tickers,xlv_tickers,xlf_tickers,xlre_tickers ]

xle_tickers,xlu_tickers,xlk_tickers,xlb_tickers,xlp_tickers,xly_tickers,xli_tickers,xlc_tickers,xlv_tickers,xlf_tickers,xlre_tickers = [flatten(x) for x in stock_tickers_test]

stock_tickers = [xle_tickers,xlu_tickers,xlk_tickers,xlb_tickers,xlp_tickers,xly_tickers,xli_tickers,xlc_tickers,xlv_tickers,xlf_tickers,xlre_tickers ]

stock_tickers_clean = [[x for x in y if str(x) != 'nan'] for y in stock_tickers]

stock_tickers_final = [[x for x in y if x.isalpha()]for y in stock_tickers_clean]




#get stock data

xle_df,xlu_df,xlk_df,xlb_df,xlp_df,xly_df,xli_df,xlc_df,xlv_df,xlf_df,xlre_df = (get_tickers(x,start_date,end_date) for x in stock_tickers_final)



ticker_dataframe = [xle_df,xlu_df,xlk_df,xlb_df,xlp_df,xly_df,xli_df,xlc_df,xlv_df,xlf_df,xlre_df]


# get sectors data

sectors_df = get_tickers(sectors,start_date,end_date)



daily = slice(0,2)
weekly = slice(0,6)
monthly = slice(0,31)
yearly = slice(0,366)



#run the rsc algo on sectors

sector_daily = rsc_algo_test(sectors_df,daily) 
sector_weekly = rsc_algo_test(sectors_df,weekly)
sector_monthly = rsc_algo_test(sectors_df,monthly) 
sector_yearly = rsc_algo_test(sectors_df,yearly)



# algo ouput into dataframe 

sector_daily_df =  pd.DataFrame(sector_daily,columns=['Ticker','RSC','Price','Percent Change','Index'])
sector_weekly_df =  pd.DataFrame(sector_weekly,columns=['Ticker','RSC','Price','Percent Change','Index'])
sector_monthly_df =  pd.DataFrame(sector_monthly,columns=['Ticker','RSC','Price','Percent Change','Index'])
sector_yearly_df =  pd.DataFrame(sector_yearly,columns=['Ticker','RSC','Price','Percent Change','Index'])



# Stock Tickers rsc algo > to dataframe



xle_daily,xlu_daily,xlk_daily,xlb_daily,xlp_daily,xly_daily,xli_daily,xlc_daily,xlv_daily,xlf_daily,xlre_daily = (rsc_algo_test(x,daily) for x in ticker_dataframe)

tickers_daily = [xle_daily,xlu_daily,xlk_daily,xlb_daily,xlp_daily,xly_daily,xli_daily,xlc_daily,xlv_daily,xlf_daily,xlre_daily]

xle_daily_df,xlu_daily_df,xlk_daily_df,xlb_daily_df,xlp_daily_df,xly_daily_df,xli_daily_df,xlc_daily_df,xlv_daily_df,xlf_daily_df,xlre_daily_df = (pd.DataFrame(x,columns=['Ticker','RSC','Price','Percent Change','Index'])
                                                                                                                                                   for x in tickers_daily)



xle_weekly,xlu_weekly,xlk_weekly,xlb_weekly,xlp_weekly,xly_weekly,xli_weekly,xlc_weekly,xlv_weekly,xlf_weekly,xlre_weekly = (rsc_algo_test(x,weekly) for x in ticker_dataframe)

tickers_weekly = [xle_weekly,xlu_weekly,xlk_weekly,xlb_weekly,xlp_weekly,xly_weekly,xli_weekly,xlc_weekly,xlv_weekly,xlf_weekly,xlre_weekly]

xle_weekly_df,xlu_weekly_df,xlk_weekly_df,xlb_weekly_df,xlp_weekly_df,xly_weekly_df,xli_weekly_df,xlc_weekly_df,xlv_weekly_df,xlf_weekly_df,xlre_weekly_df = (pd.DataFrame(x,columns=['Ticker','RSC','Price','Percent Change','Index'])
                                                                                                                                                   for x in tickers_weekly)



xle_monthly,xlu_monthly,xlk_monthly,xlb_monthly,xlp_monthly,xly_monthly,xli_monthly,xlc_monthly,xlv_monthly,xlf_monthly,xlre_monthly = (rsc_algo_test(x,monthly) for x in ticker_dataframe)

tickers_monthly = [xle_monthly,xlu_monthly,xlk_monthly,xlb_monthly,xlp_monthly,xly_monthly,xli_monthly,xlc_monthly,xlv_monthly,xlf_monthly,xlre_monthly]

xle_monthly_df,xlu_monthly_df,xlk_monthly_df,xlb_monthly_df,xlp_monthly_df,xly_monthly_df,xli_monthly_df,xlc_monthly_df,xlv_monthly_df,xlf_monthly_df,xlre_monthly_df = (pd.DataFrame(x,columns=['Ticker','RSC','Price','Percent Change','Index'])
                                                                                                                                                   for x in tickers_monthly)



xle_yearly,xlu_yearly,xlk_yearly,xlb_yearly,xlp_yearly,xly_yearly,xli_yearly,xlc_yearly,xlv_yearly,xlf_yearly,xlre_yearly = (rsc_algo_test(x,yearly) for x in ticker_dataframe)

tickers_yearly = [xle_yearly,xlu_yearly,xlk_yearly,xlb_yearly,xlp_yearly,xly_yearly,xli_yearly,xlc_yearly,xlv_yearly,xlf_yearly,xlre_yearly]

xle_yearly_df,xlu_yearly_df,xlk_yearly_df,xlb_yearly_df,xlp_yearly_df,xly_yearly_df,xli_yearly_df,xlc_yearly_df,xlv_yearly_df,xlf_yearly_df,xlre_yearly_df = (pd.DataFrame(x,columns=['Ticker','RSC','Price','Percent Change','Index'])
                                                                                                                                                   for x in tickers_yearly)
print(sector_daily_df)



pd.set_option('display.max_rows', None)

