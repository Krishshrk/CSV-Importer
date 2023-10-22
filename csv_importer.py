import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit.components.v1 as components
import json
import pandas as pd

#google api configurations
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)


#streamlit section
st.set_page_config(
    page_title="CSV Importer",
    page_icon="https://w7.pngwing.com/pngs/757/387/png-transparent-brand-artikel-market-price-csv-text-photography-logo-thumbnail.png",
    layout="centered",
    initial_sidebar_state="expanded")

page_bg_img='''
    <style>
    .stApp{
    background-size:cover;
    background-image:url('https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhJoDsppA6x2JI7WQnTgfnYaoTFVW4W48Sg-VDTMjM_l5knjx7o0_pURlt0SDAfHU0mk_jZQPCZojgLiNFQYq9ak_2I2WsNwjrQ_c8OBc-w8f4ATsuq0nK3FmY8NfHZrhwPPatB9qM2Ugl4UjFQI4goBPqTTjJECavIYOgNCLDVlWkB4CBvcBeeCoHabQ/s2560/wallpaper-for-setup-gamer-2560x1440.jpg')
    }
    </style>
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)

components.html("""<h1><p class='font-family:Arial' style='color:white; margin-bottom:-40px'><u>CSV to Google Sheets (CSV Importer)</u></p></h1>""")

json_section,csv_section=st.columns(spec=[1,1],gap="large")

with json_section:
    st.subheader("Upload your google Service Accounts API Key")
    uploaded_json=st.file_uploader(label="Json File",type=["json"])
    if uploaded_json is not None:
        bytes_json=uploaded_json.getvalue()
        new_str=bytes_json.decode('utf-8')
        json_content=json.loads(new_str)
        st.subheader("Your client email is given below, add it to your google sheets share option")
        st.success(json_content["client_email"])
        json_object=json.dumps(json_content)
        with open("copy_file.json","w") as outfile:
            outfile.write(json_object)

with csv_section:
    st.subheader("Upload the CSV File")
    uploaded_csv=st.file_uploader(label="CSV File",type=["csv"])
    if uploaded_csv is not None:
        df=pd.read_csv(uploaded_csv)
        st.subheader("CSV Sample Data")
        st.write(df.head())
        columns=st.multiselect("Choose the columns",list(df.columns))
        columns_filter=st.multiselect("Choose the columns to filter",columns)
        operations_filter=st.multiselect("Choose the opertion to perform",["=",">","<"])
        values_filter=st.text_input("Enter the values seperated by spaces").split(" ")
        if len(columns)>0:
            df=df[columns]
            if len(columns_filter)>0 and len(operations_filter)==len(columns_filter) and len(values_filter)==len(operations_filter):
                index_col=[columns_filter.index(i) for i in columns if i in columns_filter]
                for i in index_col:
                    if operations_filter[i]=="=" and values_filter[i] != "":
                        if str(df[columns_filter[i]].dtype)=="object":
                            df=df[df[columns_filter[i]]==values_filter[i]]
                        else:
                            df=df[df[columns_filter[i]]==int(values_filter[i])]
                    elif operations_filter[i]=="<" and values_filter[i] != "":
                        df=df[df[columns_filter[i]]<int(values_filter[i])]
                    elif values_filter[i] is not None:
                        df=df[df[columns_filter[i]]>int(values_filter[i])]
                df=df.reset_index(drop=True)
                st.subheader("Filtered sample data")
                st.write(df.head())
        csv_file_name=st.text_input("Enter the CSV file name created in google sheets")
        click=st.button("Convert")
        if click:
            df.to_csv('output.csv',index=False)
            spreadsheet = client.open(csv_file_name)
            with open('output.csv', 'r') as file_obj:
                content = file_obj.read()
                client.import_csv(spreadsheet.id, data=content)
            st.success("Action Performed Successfully")
            
     
                
            
                
                
    
    
  