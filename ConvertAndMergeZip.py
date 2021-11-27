# pip install openpyxl
import pandas as pd
import streamlit as st
import zipfile
import base64
import os
import io


# Web App Title
st.markdown('''
# **Excel File Merger**
This is the **Excel File Merger App** created in Python using the Streamlit library.
Created by Huru Algayeva---
''')

# Excel file merge function
def excel_file_merge(zip_file_name):
    df=pd.DataFrame()
    archive = zipfile.ZipFile(zip_file_name, 'r')
    with zipfile.ZipFile(zip_file_name, "r") as f:
        for file in f.namelist():
          xlfile = archive.open(file)
          if file.endswith('.xlsx'):
            # Add a note indicating the file name that this dataframe originates from
            df_xl = pd.read_excel(xlfile, engine='openpyxl')
            if len(df_xl.columns)==8:
                df_xl.drop([0,1,2,3],axis=0,inplace=True)
                df_xl.reset_index(drop=True, inplace=True)
                df_xl = df_xl.set_axis( ['Tarix', 'Açılma vaxtı','Kassa nömrəsi','Qəbzin nömrəsi','Məhsul','şərh',' Məbləğ','məhsulların orta miqdarı'],axis=1)
                df_xl= df_xl.fillna(method='ffill')
                df_xl=df_xl[df_xl['Qəbzin nömrəsi'].astype('string').str.contains(' ')!= True ]
                st.write(df_xl.head())
            elif len(df_xl.columns)==7:
                df_xl.drop([0,1,2,3],axis=0,inplace=True)
                df_xl.reset_index(drop=True, inplace=True)
                df_xl = df_xl.set_axis( ['Tarix', 'Açılma vaxtı','Kassa nömrəsi','Qəbzin nömrəsi','Məhsul',' Məbləğ','məhsulların orta miqdarı'],axis=1)
                df_xl.insert(5, 'şərh', 'Null')
                df_xl= df_xl.fillna(method='ffill')
                df_xl=df_xl[df_xl['Qəbzin nömrəsi'].astype('string').str.contains(' ')!= True]
                st.write(df_xl.head())

                # Appends content of each Excel file iteratively
            df=df.append(df_xl, ignore_index=True).drop_duplicates(subset=['Tarix','Qəbzin nömrəsi','Məhsul',' Məbləğ'],keep='first')
            
        return df

# Upload CSV data
with st.sidebar.header('1. Upload your ZIP file'):
    uploaded_file = st.sidebar.file_uploader("Excel-containing ZIP file", type=["zip"])
    

# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_file.csv">Download Merged File as CSV</a>'
    return href
    
def xldownload(df):
    df.to_excel('data.xlsx', index=False)
    data = open('data.xlsx', 'rb').read()
    b64 = base64.b64encode(data).decode('UTF-8')
    #b64 = base64.b64encode(xl.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/xls;base64,{b64}" download="merged_file.xlsx">Download Merged File as XLSX</a>'
    return href

# Main panel
if st.sidebar.button('Submit'):
    #@st.cache
    df = excel_file_merge(uploaded_file)
    st.header('**Merged data**')
    st.markdown(filedownload(df), unsafe_allow_html=True)
    st.markdown(xldownload(df), unsafe_allow_html=True)
else:
    st.info('Awaiting for ZIP file to be uploaded.')