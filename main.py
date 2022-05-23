import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib

conn = sqlite3.connect('data.db')
c = conn.cursor()

#database functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

#hash package functions
def make_hashes(password):
	return password

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# i need to add user input to show stocks *DONE
# i need to add revenue and profits dataset *DONE
# i need to add my personal analysis *DONE

st.header("**ANALYSIS OF LARGE CAP COMPANIES**")
st.subheader("2 YEARS WIDE DATA TAKEN FROM 28-02-2020 TO 28-02-2022")

st.sidebar.header('USER INPUT')

#Create logging system front end
menu = ["Home", "Sign Up", "Sign In","Show database"]
choice = st.sidebar.selectbox("MENU", menu)

def get_input():
    start_date = st.sidebar.text_input("Start Date", "28-02-2020", key='1')
    end_date = st.sidebar.text_input("End Date", "28-02-2022", key='2')
    stock_symbol = st.sidebar.text_input("Stock Symbol", "WIPR", key='3')
    return start_date, end_date, stock_symbol

def get_company_name(symbol):
    if symbol== 'WIPR':
        return 'WIPRO'
    elif symbol=='SBI':
        return 'SBI'
    elif symbol=='ASIANPAINT':
        return 'ASIAN PAINTS'
    elif symbol=='TATAMOTORS':
        return 'TATA MOTORS'
    elif symbol=='HDFCBANK':
        return 'HDFC BANK'
    elif symbol=='RELIANCE':
        return 'RELIANCE INDUSTRIES'
    elif symbol=='HINDUNILVR':
        return 'HINDUSTAN UNILEVER'
    elif symbol=='TCS':
        return 'TCS'
    elif symbol=='INFY':
        return 'INFOSYS'
    elif symbol=='ITC':
        return 'ITC LTD'
    else:
        'None'

def get_data(symbol,start,end):
    if symbol.upper()=='WIPR':
        df = pd.read_csv("WIPRO.csv")
        df_prom = pd.read_csv('WIPRO_PROM.csv')
        df_fin = pd.read_csv("WIPRO_financials.csv")
    elif symbol.upper()=='SBI':
        df = pd.read_csv("E:/SBIN.NS.csv")
        df_prom = pd.read_csv('SBI_PROM.csv')
        df_fin = pd.read_csv("SBI_financials.csv")
    elif symbol.upper()=='ASIANPAINT':
        df = pd.read_csv("E:/ASIANPAINT.NS.csv")
        df_prom = pd.read_csv('ASIANPAINT_PROM.csv')
        df_fin = pd.read_csv("ASIANPAINT_financials.csv")
    elif symbol.upper()=='INFY':
        df = pd.read_csv("E:/INFY.NS.csv")
        df_prom = pd.read_csv('INFY_PROM.csv')
        df_fin = pd.read_csv("INFY_financials.csv")
    elif symbol.upper()=='TCS':
        df = pd.read_csv("E:/TCS.NS.csv")
        df_prom = pd.read_csv('TCS_PROM.csv')
        df_fin = pd.read_csv("TCS_financials.csv")
    elif symbol.upper()=='TATAMOTORS':
        df = pd.read_csv("E:/TATAMOTORS.NS.csv")
        df_prom = pd.read_csv('TATAMOTORS_PROM.csv')
        df_fin = pd.read_csv("TATAMOTORS_financials.csv")
    elif symbol.upper()=='ITC':
        df = pd.read_csv("E:/ITC.NS.csv")
        df_prom = pd.read_csv('ITC_PROM.csv')
        df_fin = pd.read_csv("ITC_financials.csv")
    elif symbol.upper()=='HDFCBANK':
        df = pd.read_csv("E:/HDFCBANK.NS.csv")
        df_prom = pd.read_csv('HDFCBANK_PROM.csv')
        df_fin = pd.read_csv("HDFCBANK_financials.csv")
    elif symbol.upper()=='HINDUNILVR':
        df = pd.read_csv("E:/HINDUNILVR.NS.csv")
        df_prom = pd.read_csv('HINDUNILVR_PROM.csv')
        df_fin = pd.read_csv("HINDUNILVR_financials.csv")
    elif symbol.upper()=='RELIANCE':
        df = pd.read_csv("E:/RELIANCE.NS.csv")
        df_prom = pd.read_csv('RELIANCE_PROM.csv')
        df_fin = pd.read_csv("RELIANCE_financials.csv")

    else:
        df = pd.DataFrame(columns = ['Date','Close','Open','Volume','Adj Close','High','Low'])
        df_prom = pd.DataFrame(columns = ["COMPANY","PROMOTERS","PUBLIC","EMPLOYEE TRUSTS","STATUS","AS ON DATE","SUBMISSION DATE","REVISION DATE",])

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    start_row = 0
    end_row = 0

    for i in range(0, len(df)):
        if start <= pd.to_datetime(df['Date'][i]):
            start_row = i
            break

    for j in range(0, len(df)):
        if end <= pd.to_datetime(df['Date'][len(df) - 1 - j]):
            end_row = len(df) - 1 - j
            break

    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    return df.iloc[start_row:end_row+1, :],df_prom,df_fin

def get_technical_analysis(df,df_prom,df_fin):
    flag = 0 #0 is positive
    rating = 0
    holding = np.array(df_prom['PROMOTERS'])

    if holding[7]>=70:
        st.write("PROMOTER HOLDING IS VERY HIGH :",holding[7])
        rating+=20
    elif (holding[7]>=60) & (holding[7]<=70):
        st.write("PROMOTER HOLDING IS HIGH :",holding[7])
        rating+=18
    elif (holding[7]>=60) & (holding[7]<=70):
        st.write("PROMOTER HOLDING IS HIGH ENOUGH:",holding[7])
        rating+=18
    elif (holding[7]>=50) & (holding[7]<=60):
        st.write("PROMOTER HOLDING IS VERY DECENT :",holding[7])
        rating+=16
    elif (holding[7]>=40) & (holding[7]<=50):
        st.write("PROMOTER HOLDING IS POSITIVELY SIGNIFICANT :",holding[7])
        rating+=12
    elif (holding[7]>=20) & (holding[7]<=40):
        st.write("PROMOTER HOLDING IS LOW :",holding[7])
        rating+=9
    elif (holding[7]>=10) & (holding[7]<=20):
        st.write("PROMOTER HOLDING IS VERY LOW :",holding[7])
        rating+=5
    else:
        st.write("PROMOTER HOLDING IS NEGLIGIBLE :",holding[7])
        rating+=0

    #Volatility analysis
    if company_name=="WIPRO":
        flag = 0
        rating+=20

    elif company_name=="SBI":
        flag = 0
        rating+=20

    elif company_name == "RELIANCE":
        flag = 0
        rating += 20

    elif company_name == "HDFC BANK":
        flag = 0
        rating += 20

    #financials analysis
    revenue_arr = np.array(df_fin["Revenue(in Crores)"])
    profits_arr = np.array(df_fin["Profits(in Crores)"])
    revenue_growth_YoY = [0,0,0,0]
    profit_growth_YoY = [0,0,0,0]
    avg_revenue_growth , avg_profit_growth= 0.00,0.00

    for i in range(0,4):
        revenue_growth_YoY[i] = ((revenue_arr[i+4]-revenue_arr[i])/revenue_arr[i])* 100
        profit_growth_YoY[i] = ((profits_arr[i+4]-profits_arr[i])/profits_arr[i])* 100

    for i in range(0,4):
        avg_revenue_growth = avg_revenue_growth +revenue_growth_YoY[i]
        avg_profit_growth = avg_profit_growth + profit_growth_YoY[i]

    avg_profit_growth = avg_profit_growth/4
    avg_revenue_growth = avg_revenue_growth/4

    #include growth in revenue and  profits

    original_title = '<p style="Arial:Courier; color:Gold; font-size: 20px;">FINANCIAL ANALYSIS(REVENUE AND PROFIT GROWTH)</p>'
    st.markdown(original_title, unsafe_allow_html=True)

    if revenue_arr[3]<revenue_arr[7]:
        st.write("YEAR ON YEAR GROWTH IN REVENUE:",avg_revenue_growth.round(2),"%")
        rating +=20
    else:
        st.write("YEAR ON YEAR GROWTH IN REVENUE:(",avg_revenue_growth.round(2),")%")

    if profits_arr[3]<profits_arr[7]:
        st.write("YEAR ON YEAR GROWTH IN PROFITS:",avg_profit_growth.round(2),"%")
        rating +=20
    else:
        st.write("YEAR ON YEAR GROWTH IN PROFITS: (",avg_profit_growth.round(2),")%")

    st.write("REVENUE GROWTH IN LAST 4 QUATERS:")
    st.write(revenue_growth_YoY)

    st.write("PROFIT GROWTH IN LAST 4 QUATERS:")
    st.write(profit_growth_YoY)

    return rating


#returns offered by company
def returns(df):
    price = np.array(df['Open'])
    initial_price = price[2]
    price_at_1_year = price[140]
    price_at_last_month = price[24]
    final_price = price[294]

    return_in_2years = ((final_price -initial_price)/ initial_price) * 100
    return_in_1year = ((final_price - price_at_1_year) / price_at_1_year) * 100
    return_in_1Month = ((final_price - price_at_last_month) / price_at_last_month) * 100

    return round(return_in_2years,2),round(return_in_1year,2),round(return_in_1Month,2)

def stock_details(company_name):
    if company_name=="WIPRO":
        st.write("MARKET CAP :______2.65LCr   ")
        st.write("P/E RATIO :_______21.8 ")
        st.write("DIV YIELD :_______1.24%")
        st.write("BOOK VALUE :______119 RUPEE")
        st.write("ROCE :____________21.1%")
        st.write("FACE VALUE :______2 RUPEE")
        st.write("ROE :_____________20.3%")
        st.write("HIGH/LOW :________161/720 ")
        st.write("CDP SCORE :_______A")

    elif company_name=="SBI":
        st.write("MARKET CAP :______4.13LCr   ")
        st.write("P/E RATIO :_______11.1 ")
        st.write("DIV YIELD :_______0.86%")
        st.write("BOOK VALUE :______309 RUPEE")
        st.write("ROCE :____________4.53%")
        st.write("FACE VALUE :______1 RUPEE")
        st.write("ROE :_____________8.21%")
        st.write("HIGH/LOW :________360/549 ")
        st.write("CDP SCORE :_______C")


    elif company_name=="HDFC BANK":
        st.write("MARKET CAP :______7.23LCr   ")
        st.write("P/E RATIO :_______19.0 ")
        st.write("DIV YIELD :_______1.19%")
        st.write("BOOK VALUE :______378 RUPEE")
        st.write("ROCE :____________6.36%")
        st.write("FACE VALUE :______1 RUPEE")
        st.write("ROE :_____________18.1%")
        st.write("HIGH/LOW :________1292/1725 ")
        st.write("CDP SCORE :_______B")

    elif company_name=="RELIANCE INDUSTRIES":
        st.write("MARKET CAP :______16.2LCr   ")
        st.write("P/E RATIO :_______27.7 ")
        st.write("DIV YIELD :_______0.29%")
        st.write("BOOK VALUE :______1152 RUPEE")
        st.write("ROCE :____________9.63%")
        st.write("FACE VALUE :______10 RUPEE")
        st.write("ROE :_____________8.15%")
        st.write("HIGH/LOW :________1906/2856 ")
        st.write("CDP SCORE :_______A")

    elif company_name=="TCS":
        st.write("MARKET CAP :______12.47LCr   ")
        st.write("P/E RATIO :_______32.6 ")
        st.write("DIV YIELD :_______1.11%")
        st.write("BOOK VALUE :______244 RUPEE")
        st.write("ROCE :____________54.9%")
        st.write("FACE VALUE :______1 RUPEE")
        st.write("ROE :_____________43.6%")
        st.write("HIGH/LOW :________3036/4046 ")
        st.write("CDP SCORE :_______A")

    elif company_name=="INFOSYS":
        st.write("MARKET CAP :______6.34LCr   ")
        st.write("P/E RATIO :_______28.9 ")
        st.write("DIV YIELD :_______2.05%")
        st.write("BOOK VALUE :______179 RUPEE")
        st.write("ROCE :____________37.1%")
        st.write("FACE VALUE :______5 RUPEE")
        st.write("ROE :_____________29.0%")
        st.write("HIGH/LOW :________1311/1957 ")
        st.write("CDP SCORE :_______A")
    elif company_name=="ITC LTD":
        st.write("MARKET CAP :______3.11LCr   ")
        st.write("P/E RATIO :_______21.1 ")
        st.write("DIV YIELD :_______4.25%")
        st.write("BOOK VALUE :______49.4 RUPEE")
        st.write("ROCE :____________28.6%")
        st.write("FACE VALUE :______1 RUPEE")
        st.write("ROE :_____________21.0%")
        st.write("HIGH/LOW :________201/273 ")
        st.write("CDP SCORE :_______A-")

    elif company_name=="ASIAN PAINTS":
        st.write("MARKET CAP :______2.91LCr   ")
        st.write("P/E RATIO :_______93.7 ")
        st.write("DIV YIELD :_______0.63%")
        st.write("BOOK VALUE :______144 RUPEE")
        st.write("ROCE :____________30%")
        st.write("FACE VALUE :______1 RUPEE")
        st.write("ROE :_____________23.4%")
        st.write("HIGH/LOW :________2530/3590 ")
        st.write("CDP SCORE :_______C")

    elif company_name=="HINDUSTAN UNILEVER":
        st.write("MARKET CAP :______5.02LCr   ")
        st.write("P/E RATIO :_______56.4 ")
        st.write("DIV YIELD :_______1.59%")
        st.write("BOOK VALUE :______209 RUPEE")
        st.write("ROCE :____________24.6%")
        st.write("FACE VALUE :______1 RUPEE")
        st.write("ROE :_____________18.4%")
        st.write("HIGH/LOW :________1902/2859 ")
        st.write("CDP SCORE :_______A")

    elif company_name=="TATA MOTORS":
        st.write("MARKET CAP :______1.32LCr   ")
        st.write("P/E RATIO :_______0 ")
        st.write("DIV YIELD :_______0.00%")
        st.write("BOOK VALUE :______166 RUPEE")
        st.write("ROCE :____________1.49%")
        st.write("FACE VALUE :______2 RUPEE")
        st.write("ROE :_____________-20.7%")
        st.write("HIGH/LOW :________268/537 ")
        st.write("CDP SCORE :_______C")
    else:
        pass

def include_profit_margin(df_fin):
    revenue_arr = np.array(df_fin["Revenue(in Crores)"])
    profits_arr = np.array(df_fin["Profits(in Crores)"])
    profit_margin = [0,0,0,0,0,0,0,0]

    for i in range(0,8):
        profit_margin[i] = (profits_arr[i]/revenue_arr[i]) * 100

    df_fin_updated =df_fin
    df_fin_updated["Net Profit Margin"] = profit_margin

    return df_fin_updated

#starting the program

if choice == "Home":
    start, end, symbol = get_input()
    df, df_prom,df_fin = get_data(symbol, start, end)
    df_prom = df_prom.filter(items=["COMPANY", "PROMOTERS", "PUBLIC", "EMPLOYEE TRUSTS", "AS ON DATE"], axis=1)

    company_name = get_company_name(symbol.upper())

    # display STOCK PRICE
    st.subheader("CHART PATTERN OF "+ company_name)
    st.line_chart(df['Adj Close'])

    # details of stock
    stock_details(company_name)
    # display VOLUME CHART
    st.subheader("VOLUME CHART")
    st.line_chart(df['Volume'])

    original_title = '<p style="font-family:Courier; color:Blue; font-size: 15px;">STOCK VOLATILITY IS LOWER THAN AVERAGE MARKET VOLATILITY</p>'
    st.markdown(original_title, unsafe_allow_html=True)

    # display statistics
    st.write("STATISTICS OF ", company_name)
    st.write(df)

    # display shareholding pattern
    st.header("SHAREHOLDING PATTERN")
    st.write(df_prom)

    #display Revenue and profits
    st.subheader("QUATERLY RESULTS")
    df_fin = include_profit_margin(df_fin)
    st.write(df_fin)
    # display technical analysis
    st.header("TECHNICAL ANALYSIS")
    rating = get_technical_analysis(df, df_prom,df_fin)

    #display returns offered:
    st.subheader("RETURNS OFFERED BY "+company_name)
    return_in_2years, return_in_1year, return_in_1Month = returns(df)

    if return_in_1year>=8:

        original_title = '<p style="Arial:Courier; color:blue; font-size: 18px;">STOCK GENERATES BETTER RETURNS THAN FIXED DEPOSITS  IN A YEAR</p>'
        st.markdown(original_title, unsafe_allow_html=True)

    else:
        original_title = '<p style="Arial:Courier; color:red; font-size: 18px">STOCK DOES NOT GENERATES BETTER RETURNS THAN FIXED DEPOSITS IN A YEAR</p>'
        st.markdown(original_title, unsafe_allow_html=True)

    st.write("RETURNS OFFERED IN 2 YEARs:", return_in_2years)
    st.write("RETURNS OFFERED IN 1 YEAR :", return_in_1year)
    st.write("RETURNS OFFERED IN 1 MONTH:", return_in_1Month)

    #display Rating:
    st.subheader("ANALYST RATING FOR THIS STOCK:")
    st.write("RATING FOR THIS STOCK IS:", rating, " OUT OF 100")

elif choice == "Sign In":
    st.subheader("This is sign in page")
    user = st.text_input('Username')
    passwd = st.text_input('Password', type='password')

    create_usertable()
    hashed_pswd = make_hashes(passwd)
    result = login_user(user, check_hashes(passwd, hashed_pswd))
    if result:
        st.success("Logged In as {}".format(user))
    else:
        st.warning("Incorrect ID or password")


elif choice == "Sign Up":
    st.subheader("This is sign Up page")
    new_user = st.text_input("Username")
    new_passwd = st.text_input("Password",type='password')
    if st.button("SIGN UP"):
        create_usertable()
#this is makehash(new_passwd)
        add_userdata(new_user, new_passwd)
        st.success("You have successfully created an account.Go to the Sign In page")

elif choice == "Show database":
    user_data = view_all_users()
    Clean_data = pd.DataFrame(user_data,columns=["USERNAME","PASSWORD"])
    st.dataframe(Clean_data)