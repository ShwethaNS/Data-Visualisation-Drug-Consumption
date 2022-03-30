"""
# Tutorial: Building data apps with Streamlit
Created by Natkamon Tovanich - version 2022-03-01
"""
import openpyxl
import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
import plotly.express as px
import plotly.graph_objs as go
#from vega_datasets import data
#from streamlit_vega_lite import vega_lite_component, altair_component
import time
st.set_page_config(layout="wide")
'''
# Visualization of Drug Consumption Behavior

## Dataframe'''


# Load Gapminder data
# @st.cache decorator skip reloading the code when the apps rerun.
@st.cache
def loadData():
    df = pd.read_excel('Dataset 4 Drug Consumption Dataset_cleaned.xlsx')
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


@st.cache(allow_output_mutation=True)
def Main_chart(df, keys):
    # selected = alt.selection_multi(encodings=['x', 'y', 'size'])
    source_1 = df[df[keys['drug']] == 'CL0'][[keys['options'], 'ID']].groupby(keys['options']).count().transform(
        lambda x: 100 * x / x.sum())
    source_2 = df[df[keys['drug']] == 'CL1'][[keys['options'], 'ID']].groupby(keys['options']).count().transform(
        lambda x: 100 * x / x.sum())
    source_3 = df[df[keys['drug']] == 'CL2'][[keys['options'], 'ID']].groupby(keys['options']).count().transform(
        lambda x: 100 * x / x.sum())
    source_4 = df[df[keys['drug']] == 'CL3'][[keys['options'], 'ID']].groupby(keys['options']).count().transform(
        lambda x: 100 * x / x.sum())
    print(source_4)
    source_5 = df[df[keys['drug']] == 'CL4'][[keys['options'], 'ID']].groupby(keys['options']).count().transform(
        lambda x: 100 * x / x.sum())
    source_6 = df[df[keys['drug']] == 'CL5'][[keys['options'], 'ID']].groupby(keys['options']).count().transform(
        lambda x: 100 * x / x.sum())



    data = [  # Portfolio (inner donut)
        go.Pie(values=list(source_1['ID']),
               labels=source_1.index.values.tolist(),
               domain={'x': [0.1, 0.9], 'y': [0, 1]},
               hole=0.9,
               direction='clockwise',
               sort=False,
               marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
                           line=dict(color='#000000', width=2))
               ),
        # Individual components (outer donut)
        go.Pie(values=list(source_2['ID']),
               labels=source_2.index.values.tolist(),
               domain={'x': [0.2, 0.8], 'y': [0.1, 0.9]},
               hole=0.8,
               direction='clockwise',
               sort=False,
               marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
                           line=dict(color='#000000', width=2)),
               showlegend=False),
        go.Pie(values=list(source_3['ID']),
               labels=source_3.index.values.tolist(),
               domain={'x': [0.3, 0.7], 'y': [0.2, 0.8]},
               hole=0.7,
               direction='clockwise',
               sort=False,
               marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
                           line=dict(color='#000000', width=2)),
               showlegend=False),
        go.Pie(values=list(source_4['ID']),
               labels=source_4.index.values.tolist(),
               domain={'x': [0.4, 0.6], 'y': [0.3, 0.7]},
               hole=0.6,
               direction='clockwise',
               sort=False,
               marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
                           line=dict(color='#000000', width=2)),
               showlegend=False)
        # go.Pie(values=list(source_5['ID']),
        #        labels=source_5.index.values.tolist(),
        #        domain={'x': [0.2, 0.8], 'y': [0.1, 0.9]},
        #        hole=0.8,
        #        direction='clockwise',
        #        sort=False,
        #        marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
        #                    line=dict(color='#000000', width=2)),
        #        showlegend=False),
        # go.Pie(values=list(source_6['ID']),
        #        labels=source_6.index.values.tolist(),
        #        domain={'x': [0.1, 0.9], 'y': [0, 1]},
        #        hole=0.9,
        #        direction='clockwise',
        #        sort=False,
        #        marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
        #                    line=dict(color='#000000', width=2)),
        #        showlegend=False)
    ]

    fig = go.Figure(data=data, layout={'title': 'Percentage distribution of people in a category'})

    return fig

'''


'''
st.plotly_chart(Main_chart(df, keys))

# stacked pie chart: https://stackoverflow.com/questions/33019879/hierarchic-pie-donut-chart-from-pandas-dataframe-using-bokeh-or-matplotlib/33046810
# nested pie chart : https://matplotlib.org/stable/gallery/pie_and_polar_charts/nested_pie.html#sphx-glr-gallery-pie-and-polar-charts-nested-pie-py

@st.cache(allow_output_mutation=True)
def sub_chart1(df, keys):
    
    source2 = df[df[keys['drug']] == 'CL0']

    chart = alt.Chart(source2).mark_bar().encode(
        x=alt.X('Gender', title = None, axis = alt.Axis(labels = False)),
        y=alt.Y('ID:Q', title = 'Number of people'),
        color=alt.Color('Gender', legend = alt.Legend(orient = "right")),
        column=keys['options']
        ).properties(width=20, height=150)
        
    return chart

@st.cache(allow_output_mutation=True)
def sub_chart2(df, keys):
    
    source2 = df[df[keys['drug']] == 'CL0']
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
    st.write("#### Number of people in selected category")
    st.write("Selected Category:", options)
    st.altair_chart(sub_chart1(df, keys)) 

with col2:
    st.write("#### Distribution of personal trait over selected category and drug")
    st.write("Selected category and drug: ", options, ",", drug)
    scores = st.multiselect(
     'Select the scores for personal trait:',
     ['Nscore', 'Escore', 'Oscore', 'Ascore', 'Cscore'], ['Nscore', 'Escore', 'Oscore', 'Ascore', 'Cscore'])
    
    keys['scores'] = scores
    st.altair_chart(sub_chart2(df, keys)) 
    