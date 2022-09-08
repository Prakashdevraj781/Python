##############################################################
# Author: Sarfraz
# Description: This script generates Money FLow Analysis sheet
# Email: sarfraz.contact@gmail.com
##############################################################

import os
import sys
import six
import pandas as pd
import numpy as np
from nsetools import Nse
from datetime import date, datetime
from requests import Session
from functools import partial
from nsepy.commons import URLFetch, unzip_str
import warnings
warnings.filterwarnings('ignore')


def get_price_list(dt):
    MMM = dt.strftime("%b").upper()
    yyyy = dt.strftime("%Y")
    res = derivative_price_list_url(yyyy, MMM, dt.strftime("%d%b%Y").upper())
    if res.status_code == 404:
        sys.exit("Bhavcopy not found")
    txt = unzip_str(res.content)
    fp = six.StringIO(txt)
    df = pd.read_csv(fp)
    del df['Unnamed: 15']
    return df

scrip = input("Enter stock/index symbol: ")
date_str = input("Enter date in yyyy-mm-dd format: ")
date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
# Get list of stocks that are in futures
nse = Nse()
fo_list = nse.get_fno_lot_sizes()

# Check if stock is in futures
if scrip not in fo_list:
    sys.exit('Not a FO index/stock')

# Get lot size
lot_size = fo_list.get(scrip)
    
if scrip in ['NIFTY', 'BANKNIFTY', 'FINNIFTY']:
    instrument = 'OPTIDX'
else:
    instrument = 'OPTSTK'

# Starting session to fetch bhavcopy
session = Session()

headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
           'Connection': 'keep-alive',
           'Host': 'www1.nseindia.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest',
           'Referer': 'https://www1.nseindia.com/products/content/derivatives/equities/historical_fo.htm'}

URLFetchSession = partial(URLFetch, session=session, headers=headers)

derivative_price_list_url = URLFetchSession(
    url="http://www1.nseindia.com/content/historical/DERIVATIVES/%s/%s/fo%sbhav.csv.zip")

data = get_price_list(date_obj)

# Filter for chosen instrument and symbol
data = data.loc[data['INSTRUMENT'] == instrument]
data = data.loc[data['SYMBOL'] == scrip]

# Check if day is thursday or not
if date_obj.isoweekday() == 4:
    data = data.loc[data['EXPIRY_DT'] > pd.to_datetime(data['EXPIRY_DT']).min().strftime('%d-%b-%Y')]

# Filter for latest series
data = data.loc[data['EXPIRY_DT'] == pd.to_datetime(data['EXPIRY_DT']).min().strftime('%d-%b-%Y')]

# Calculate derived columns
data['LOT_SIZE'] = lot_size
data['EXTRA'] = (data['STRIKE_PR'] * data['CONTRACTS'] * data['LOT_SIZE'])/100000
data['PREMIUM_TURNOVER'] = data['VAL_INLAKH'] - data['EXTRA']
data['EXTRA1'] = data['PREMIUM_TURNOVER'] * 100000
data['EXTRA2'] = data['EXTRA1'] / data['CONTRACTS']
data['VWAP'] = data['EXTRA2'] / data['LOT_SIZE']
data['OI/CONTRACTS'] = data['CHG_IN_OI'] / data['LOT_SIZE']
data['OPEN_INT/LOT_SIZE'] = data['OPEN_INT'] / data['LOT_SIZE']
data['VALUE_IN_LAKHS'] = (data['VWAP'] * data['CHG_IN_OI']) / 100000

# Sort by PREMIUM TURNOVER
data.sort_values(by=['PREMIUM_TURNOVER'], ascending=False, inplace=True)

# Get TOP 10 strike prices
top_10_strike_pr_list = data.head(10)['STRIKE_PR'].unique()

# Make pairs for the TOP 10
final_df = data.loc[data['STRIKE_PR'].isin(top_10_strike_pr_list)]

# Calculate derived columns
final_df = final_df.assign(BREAKEVEN=np.nan)
final_df.loc[final_df['OPTION_TYP'] == 'CE', ['BREAKEVEN']] = round(final_df['STRIKE_PR'] + final_df['VWAP'], 2)
final_df.loc[final_df['OPTION_TYP'] == 'PE', ['BREAKEVEN']] = round(final_df['STRIKE_PR'] - final_df['VWAP'], 2)

# Add support/resistance labels
final_df.sort_values(by=['PREMIUM_TURNOVER'], ascending=False, inplace=True)
final_df = final_df.assign(IMPORTANT_LEVELS='')

final_df.at[final_df.loc[final_df['OPTION_TYP'] == 'CE'].index[0], 'IMPORTANT_LEVELS'] = 'Resistance 1'
final_df.at[final_df.loc[final_df['OPTION_TYP'] == 'CE'].index[1], 'IMPORTANT_LEVELS'] = 'Resistance 2'
final_df.at[final_df.loc[final_df['OPTION_TYP'] == 'CE'].index[2], 'IMPORTANT_LEVELS'] = 'Resistance 3'

final_df.at[final_df.loc[final_df['OPTION_TYP'] == 'PE'].index[0], 'IMPORTANT_LEVELS'] = 'Support 1'
final_df.at[final_df.loc[final_df['OPTION_TYP'] == 'PE'].index[1], 'IMPORTANT_LEVELS'] = 'Support 2'
final_df.at[final_df.loc[final_df['OPTION_TYP'] == 'PE'].index[2], 'IMPORTANT_LEVELS'] = 'Support 3'

# Remove unnecessary columns
del final_df['EXTRA']
del final_df['EXTRA1']
del final_df['EXTRA2']

# File path
file_path = 'EOD_Report/'+date_str + '/'

# Create folder if the folder does not exists
if not os.path.exists(file_path):
    os.makedirs(file_path)

filename = file_path + scrip + '_Money_Flow_' + date_str + '.xlsx'

# Create a Pandas Excel writer using XlsxWriter as the engine
writer = pd.ExcelWriter(filename, engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
final_df.to_excel(writer, sheet_name='Sheet1', index=False)

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Add background colors to support and resistance
cell_format = workbook.add_format()
cell_format.set_bg_color('#B60A1C')
row_number, col_number = np.where(final_df == 'Resistance 1')
worksheet.write('W' + str(row_number[0]+2), 'Resistance 1', cell_format)

cell_format = workbook.add_format()
cell_format.set_bg_color('#E03531')
row_number, col_number = np.where(final_df == 'Resistance 2')
worksheet.write('W' + str(row_number[0]+2), 'Resistance 2', cell_format)

cell_format = workbook.add_format()
cell_format.set_bg_color('#FF684C')
row_number, col_number = np.where(final_df == 'Resistance 3')
worksheet.write('W' + str(row_number[0]+2), 'Resistance 3', cell_format)

cell_format = workbook.add_format()
cell_format.set_bg_color('#309143')
row_number, col_number = np.where(final_df == 'Support 1')
worksheet.write('W' + str(row_number[0]+2), 'Support 1', cell_format)

cell_format = workbook.add_format()
cell_format.set_bg_color('#51B364')
row_number, col_number = np.where(final_df == 'Support 2')
worksheet.write('W' + str(row_number[0]+2), 'Support 2', cell_format)

cell_format = workbook.add_format()
cell_format.set_bg_color('#8ACE7E')
row_number, col_number = np.where(final_df == 'Support 3')
worksheet.write('W' + str(row_number[0]+2), 'Support 3', cell_format)

# Left align the headers
header_format = workbook.add_format({
    'bold':     True,
    'align':    'left',
    'valign':   'vcenter',
})
worksheet.write_row('A1', final_df.columns, header_format)

writer.save()
print('Money Flow Report Successfully Generated')
