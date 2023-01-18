import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from test import test_decode_file
df = pd.read_csv('decoded_data_7_aout.csv')
#df.set_index('time', inplace=True)

st.title('FormUL Dashboard')

left_column, right_column = st.columns(2)

log = st.file_uploader("Upload a log_file", type="txt", key=1)

dbc_file = st.file_uploader("Upload a dbc_file", type="dbc", key=2)
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
        df.columns.to_list()[1:], key=3,
        max_selections=5)
    second_option_left = st.selectbox(
        'Choose a way of showing data',
        ['Line Chart', "Dataframe"], key=4)

    if option_left == []:
        option_left = [df.columns.to_list()[1]]

    if second_option_left == 'Line Chart':
        
        p = figure(
                    title='Data',
                    x_axis_label='time',
                    y_axis_label='y')
        possible_colors = ['red', 'blue', 'green', 'yellow', 'black']
        for n, i in enumerate(option_left):
            graph_data = df[['time', i]].dropna()

            #p.line(graph_data['time'], graph_data[i], legend_label=i, line_width=2)
            #Change color
            p.line(graph_data['time'], graph_data[i], legend_label=i, line_width=2, color=possible_colors[n])
        st.bokeh_chart(p, use_container_width=True)

        graph_data = df[['time', option_left[0]]].dropna()
        st.subheader(option_left)
    else:
        if type(option_left) == list and len(option_left) > 1:
            st.subheader(option_left)
            st.dataframe(df[option_left].dropna())
        else:
            data = pd.DataFrame()
            st.write("TODO")

with right_column:
    option_right = st.multiselect(
        'Choose a variable',
        df.columns.to_list()[1:], key=6,
        max_selections=5)
    second_option_right = st.selectbox(
        'Choose a way of showing data',
        ['Line Chart', "Dataframe"], key=7)

    if option_right == []:
        option_right = [df.columns.to_list()[2]]

    if second_option_right == 'Line Chart':
        
        p_right = figure(
                    title='Data',
                    x_axis_label='time',
                    y_axis_label='y')
        possible_colors = possible_colors[::-1]
        for n, i in enumerate(option_right):
            graph_data = df[['time', i]].dropna()

            #p.line(graph_data['time'], graph_data[i], legend_label=i, line_width=2)
            #Change color
            p_right.line(graph_data['time'], graph_data[i], legend_label=i, line_width=2, color=possible_colors[n])
        st.bokeh_chart(p_right, use_container_width=True)

        graph_data = df[['time', option_right[0]]].dropna()
        st.subheader(option_right)
    else:
        if type(option_right) == list and len(option_right) > 1:
            st.subheader(option_right)
            st.dataframe(df[option_right].dropna())
        else:
            data = pd.DataFrame()
            st.write("TODO")
