# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 17:38:09 2021

@author: FarzanehAkhbar
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import random
import datetime
import os
import streamlit as st
import io
import base64

os.chdir('C:/Users/FarzanehAkhbar/Documents/FAAS/data')


                 
in_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False, type='csv')
if in_file is not None:
    # data = pd.read_csv(io.StringIO(in_file.read().decode('utf-8')), sep=';', index_col=0)
    data = pd.read_csv('BTC -for_customerdatagen.csv', delimiter=(';'))
    data['date'] = pd.to_datetime(data['date'])
    data['signal'] = data['signal'].astype(float)
    dfls = [data]
    st.header("Create Customer Data")
    
    customerno = st.number_input("Enter Number of your Customers", value=1)
    st.markdown(f"Current Session Id: **{customerno}**")
    
  

# customerno = 20

def plot(df, customerno):
    
    # df = pd.read_csv('sample.csv', delimiter=(';'))
    
   
    def makerandomnooforders(signal,customerno ):
        
        # p1 = customerno 
        total = 0
        max_no_order = (signal // customerno)
        nooforders = []
        for i in range(0, customerno):
            if total < signal:
                tempval = random.randint(0, max_no_order)
                nooforders.append(tempval)
                total = total + tempval
                leftover = signal - total
            elif total >= signal:
                nooforders.append(0)
        if total < signal:
            #print('no')
            deltaval = signal - total
            nooforders[0] = nooforders[0] + deltaval
        elif total > signal:
            #print('yes')
            v = 0
            deltaval = total - signal
            while nooforders[v] < deltaval:
                    #print(  v)
                    #print(nooforders[v])
                    v +=1 
        if total > signal:
            nooforders[v] = nooforders[v] - deltaval
        #print(nooforders)
        return nooforders
    
    
    
    
    customeridls = []
    orderdatels = []
    customerdb = pd.DataFrame(columns=['customer_id', 'order_date','sale'])
    
    for h in range(customerno):
        customerid = 'C' + str(h)
        customeridls.append(customerid)
    
    for db in (dfls):
        # print(db)
       
        sale = (db['signal']).tolist()
        date = db['date'].tolist()
        # print(sale)
        # print(date)
        for i, item in enumerate(sale):
            # print(i, item)
            dt = date[i]
            nooforders = makerandomnooforders(item, customerno)
            # print(nooforders)
            
            orderdatels = [dt] * customerno
            # print(customeridls)
            # print(orderdatels)
            # print(nooforders)
            d = {'customer_id':customeridls,'order_date':orderdatels,'sale': nooforders}
            customerdata_temp = pd.DataFrame(d) 
            # print(customerdata_temp)
            customerdb = customerdb.append(customerdata_temp)
        
    
        
    # def plot():
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xlabel('Date')
        ax.set_ylabel('Sale')
        ax.set_title('Sale Trend for Customers')
        for i in range (1,customerno):
            cusid = 'C' + str(i)
            cd = customerdb.loc[customerdb['customer_id'] == cusid]
            # ax.plot(data.Date, data.Close, color='tab:blue', label='price')
            ax.plot(cd['order_date'],cd['sale'].astype(float), label = cusid)
            ax.legend(loc="upper right")
            ax.grid(True)
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
                
        # def get_table_download_link(df):
        #     csv = df.to_csv(index=False)
        #     b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        #     href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
            
        # st.markdown(get_table_download_link(customerdb), unsafe_allow_html=True)
   
        csv = customerdb.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings
        linko= f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'
        st.markdown(linko, unsafe_allow_html=True)
          
        st.pyplot(fig)
    
    

if st.button('Plot '):
    plot(dfls, customerno)
    


