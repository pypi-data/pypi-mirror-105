import pandas as pd
import numpy as np
import streamlit as st
import time
import plotly.express as px

import getpass
# pwd = getpass.getpass("passsword:")
from toolkit_w.snowflake.snowflakeq import Snowflakeq
SQ = Snowflakeq()

st.title('My first app')

# df = SQ.exec_sf_q('SELECT * FROM ORDERS','SAFARI_LTD',pwd,role='')
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)