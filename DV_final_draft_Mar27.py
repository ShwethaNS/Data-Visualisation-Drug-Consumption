"""
# Tutorial: Building data apps with Streamlit
Created by Natkamon Tovanich - version 2022-03-01
"""
# from curses import use_default_colors
from pydoc import cli
import openpyxl
import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
import plotly.express as px
import plotly.graph_objs as go
from ipywidgets import Output, VBox
from streamlit_plotly_events import plotly_events
from streamlit.state.session_state import SessionState
#from vega_datasets import data
#from streamlit_vega_lite import vega_lite_component, altair_component
import time
import warnings
st.set_page_config(layout="wide")


# warnings.simplefilter("ignore", UserWarning)
showWarningOnDirectExecution = False

'''
# Visualization of Drug Consumption Behavior

## Dataframe'''


# Load Gapminder data
# @st.cache decorator skip reloading the code when the apps rerun.
@st.cache
def loadData():
    df = pd.read_excel('C:/Users/youji/Desktop/T2/DV/Dataset 4 Drug Consumption Dataset_cleaned.xlsx')
    return df

df = loadData()

# Use st.write() to render any objects on the web app
st.write(df)

# Magic command: Streamlit automatically writes a variable 
# or a literal value to your app using st.write().


# Select year


# Create an Altair chart
st.write('## Chart')
'''


'''
# Create the bubble chart with selection
drug_list = ['Alcohol', 'Amphet', 'Amyl', 'Benzos', 'Caffeine',
       'Cannabis', 'Choc', 'Cocaine', 'Crack', 'Ecstacy', 'Heroin', 'Ketamine',
       'Legalh', 'LSD', 'Methadone', 'Mushroom', 'Nicotine', 'Semer', 'VSA']

sel1, sel2 = st.columns(2)

with sel1:
    drug = st.sidebar.selectbox('drugs', drug_list)
with sel2:
    options = st.sidebar.radio("Choose the category to see:", ('Age(class)', 'Education', 'Country'))
    
    
keys = dict()
keys_1 = dict()
keys['drug'] = drug
keys['options'] = options
keys_1['options'] = options

#source = df[df[keys['drug']] == 'CL0'][[keys['options'], 'ID']].groupby(keys['options']).count()
# source[keys['options']] = source.index
#X = df[df[keys['drug']] == 'CL1'][[keys['options'], 'ID']].groupby(keys['options']).count().transform(lambda x: 100*x/x.sum())
#X = X.merge(source, on=keys['options'])
#print(X)

# @st.cache(allow_output_mutation=True)
# def Main_chart(df, keys):
    # selected = alt.selection_multi(encodings=['x', 'y', 'size'])
consum_dict = dict()
consum_dict = {0: "CL0", 1:"CL1", 2:"CL2", 3:"CL3", 4: "CL4", 5:'CL6'}
source_1 = df[df[keys['drug']] == 'CL0'][[keys['options'], 'ID']].groupby(keys['options']).count().transform(
    lambda x: 100 * x / x.sum())
source_2 = df[df[keys['drug']] == 'CL1'][[keys['options'], 'ID']].groupby(keys['options']).count().transform(
    lambda x: 100 * x / x.sum())
X = source_1.merge(source_2, on=keys['options'])
source_3 = df[df[keys['drug']] == 'CL2'][[keys['options'], 'ID']].groupby(keys['options']).count().transform(
    lambda x: 100 * x / x.sum())
X = X.merge(source_3, on=keys['options'])

data = [  # Portfolio (inner donut)
    go.Pie(values=list(X['ID_x']),
            labels=X.index.values.tolist(),
            domain={'x': [0.3, 0.7], 'y': [0.2, 0.8]},
            hole=0.5,
            direction='clockwise',
            sort=False,
            marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
                        line=dict(color='#000000', width=2)),

            ),
    # Individual components (outer donut)
    go.Pie(values=list(X['ID_y']),
            labels=X.index.values.tolist(),
            domain={'x': [0.2, 0.8], 'y': [0.1, 0.9]},
            hole=0.65,
            direction='clockwise',
            sort=False,
            marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
                        line=dict(color='#000000', width=2)),
            showlegend=False),
    go.Pie(values=list(X['ID']),
            labels=X.index.values.tolist(),
            # domain={'x': [0.1, 0.9], 'y': [0, 1]},
            hole=0.75,
            direction='clockwise',
            sort=False,
            marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
                        line=dict(color='#000000', width=2)),
            showlegend=False)
]

fig = go.Figure(data=data, layout={'title': 'Percentage distribution of people in a category'})

st.session_state['click'] = plotly_events(fig)
    # return fig

# st.plotly_chart(Main_chart(df, keys))
try:
    st.session_state['name'] = consum_dict[st.session_state['click'][0]['curveNumber']]
except:
    st.session_state['name'] = "CL0"


'''


'''

# st.plotly_chart(Main_chart(df, keys))

# stacked pie chart: https://stackoverflow.com/questions/33019879/hierarchic-pie-donut-chart-from-pandas-dataframe-using-bokeh-or-matplotlib/33046810
# nested pie chart : https://matplotlib.org/stable/gallery/pie_and_polar_charts/nested_pie.html#sphx-glr-gallery-pie-and-polar-charts-nested-pie-py

# @st.cache(allow_output_mutation=True)
def sub_chart1(df, keys):
    
    
    source2 = df[df[keys['drug']] == st.session_state['name']]

    chart = alt.Chart(source2).mark_bar().encode(  
    
        x=alt.X('Gender', title = None, axis = alt.Axis(labels = False)),
        y=alt.Y('count(ID):Q',title = 'Number of people'),

        color=alt.Color('Gender', scale=alt.Scale(
 
                range=['#F1948A', '#5DADE2']
        )),
        column=alt.Column(keys['options']
        ),
        tooltip = [keys['options'], 'Gender', 'count(ID)']
        ).properties(height=410
        ).configure_legend(orient='bottom'
)
        
    return chart

# @st.cache(allow_output_mutation=True)
def sub_chart2(df, keys):
    
    source2 = df[df[keys['drug']] == st.session_state['name']]
    chart = alt.Chart(source2).transform_fold(
        keys['scores'],
        as_ = ['Personal_trait', 'value']
    ).transform_density(
        density='value',
        bandwidth=0.3,
        groupby=['Personal_trait'],
        extent= [15, 65],
        counts = True,
        steps=200
    ).mark_area().encode(
        alt.X('value:Q'),
        alt.Y('density:Q', stack='zero'),
        alt.Color('Personal_trait:N'),
        alt.OpacityValue(0.4)
        
    )
    return chart


col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.write("#### Number of people in selected category")
        st.write("Selected Category:", options)
        st.altair_chart(sub_chart1(df, keys), use_container_width=False) 

with col2:
        with st.container():
            st.write("#### Distribution of personal trait over selected category and drug")
            st.write("Selected category and drug: ", options, ",", drug)
            scores = st.multiselect(
            'Select the scores for personal trait:',
            ['Nscore', 'Escore', 'Oscore', 'Ascore', 'Cscore'], ['Nscore', 'Escore', 'Oscore', 'Ascore', 'Cscore'])
            
            keys['scores'] = scores
            '''
            
            








            '''
            st.altair_chart(sub_chart2(df, keys), use_container_width=True) 
