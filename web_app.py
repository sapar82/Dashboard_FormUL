import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from test import test_decode_file
df = pd.read_csv('decoded_data_7_aout.csv')
#df.set_index('time', inplace=True)

st.title('FormUL Dashboard')

left_column, right_column = st.columns(2)

log = st.file_uploader("Upload a log_file", type="txt", key=6)

dbc_file = st.file_uploader("Upload a dbc_file", type="dbc", key=7)
if dbc_file is None:
    dbc_file = 'dbc/formul_16_jan.dbc'

if log is not None:
    try:
        df = test_decode_file(log, dbc_file)
        st.write('File uploaded')
        st.dataframe(df)
    except Exception as e:
        print(e)
        st.write('Error in file')
        st.write(dbc_file)
        st.write(e)
else: 
    df = pd.read_csv('decoded_data_7_aout.csv')
    st.write('No file uploaded, default file is used')

with left_column:
    option_left = st.multiselect(
        'Choose a variable',
        df.columns.to_list()[1:], key=15)
    second_option_left = st.selectbox(
        'Choose a way of showing data',
        ['Line Chart', "Dataframe"], key=3)

    if option_left == []:
        option_left = [df.columns.to_list()[1]]

    if second_option_left == 'Line Chart':
        if type(option_left) == list and len(option_left) > 1:
            fig, ax = plt.subplots()

            for i in option_left:
                graph_data = df[i].dropna()
                ax.plot(graph_data, label=i)
            ax.legend()
            st.pyplot(fig)
        else:
            graph_data = df[option_left].dropna()
            st.subheader(option_left)
            st.line_chart(graph_data,y=option_left)
    else:
        if type(option_left) == list and len(option_left) > 1:
            st.subheader(option_left)
            st.dataframe(df[option_left].dropna())
        else:
            data = pd.DataFrame()
            st.write("TODO")

with right_column:

    option_right = st.selectbox(
        'Choose a variable',
        df.columns.to_list()[1:], key=2)

    second_option_right = st.selectbox(
        'Choose a way of showing data',
        ['Line Chart', "Dataframe"], key=4)
    
    if second_option_right == 'Line Chart':
        graph_data = df[option_right].dropna()
        st.subheader(option_right)
        st.line_chart(graph_data, y=option_right)
    else:
        st.subheader(option_right)
        st.dataframe(df[option_right].dropna())
