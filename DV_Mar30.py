"""
# Tutorial: Building data apps with Streamlit
Created by Natkamon Tovanich - version 2022-03-01
"""
# from curses import use_default_colors
from pydoc import cli

import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objs as go
from streamlit_plotly_events import plotly_events

st.set_page_config(page_title="Visualization of Drug Consumption Behavior", page_icon="🧊",layout="wide")

st.title("Visualization of Drug Consumption Behavior")



st.header('Data')
'''
The data was collected by Elaine Fehrman between March 2011 and March 2012. (Fehrman et al.) While gathering data, an online survey tool was used to maximize anonymity. The database contains records of 1,885 respondents. Each participant was asked 50 questions on their personality which was normalized to Gaussian and converted to T-score. 
For each respondent, 12 attributes are included: personality measurement of impulsivity, sensation seeking, and 5 features from FFM, which comprises Neuroticism(N), Extraversion(E), Openness to Experience(O), Agreeableness(A), and Conscientiousness(C), level of education, age, gender, country of residence, and ethnicity. It includes the usage of 18 legal and illegal drugs* with categorical answers: never used the drug, used it over a decade ago, or in the last decade, year, month, week, or day.
* list of drugs alcohol, amphetamines, amyl nitrite, benzodiazepine, cannabis, chocolate, cocaine, caffeine, crack, ecstasy, heroin, ketamine, legal highs, LSD, methadone, mushrooms, nicotine
* source: https://archive.ics.uci.edu/ml/datasets/Drug+consumption+%28quantified%29#
'''


@st.cache
def loadData():
    df = pd.read_excel('Dataset 4 Drug Consumption ass2.xlsx')
    df_original = pd.read_excel('drug_consumption_original.xlsx')
    return df, df_original

df, df_original = loadData()

@st.cache
def convert_df(df):
     return df.to_csv().encode('utf-8')

csv = convert_df(df_original)
st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='dataset_drug_consumption_behavior.csv',
     mime='text/csv',
 )

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
    options = st.sidebar.radio("Choose the category to see:", ('Age', 'Education', 'Country'))
    
    
keys = dict()
keys_1 = dict()
keys['drug'] = drug
keys['options'] = options
keys_1['options'] = options

# @st.cache(allow_output_mutation=True)
# def Main_chart(df, keys):
    # selected = alt.selection_multi(encodings=['x', 'y', 'size'])
consum_dict = dict()
consum_dict = {0: "CL0", 1:"CL1", 2:"CL2", 3:"CL3", 4: "CL4", 5:'CL6'}

source_1 = df[df[keys['drug']] == 'CL0'][[keys['options'], 'ID']].groupby(keys['options']).count()
source_2 = df[df[keys['drug']] == 'CL1'][[keys['options'], 'ID']].groupby(keys['options']).count()
source_3 = df[df[keys['drug']] == 'CL2'][[keys['options'], 'ID']].groupby(keys['options']).count()\


data = [  # Portfolio (inner donut)
go.Pie(values=list(source_1['ID']),
           labels=source_1.index.values.tolist(),
           domain={'x': [0.3, 0.7], 'y': [0.2,0.8]},
           hole=0.25,
           direction='clockwise',
           sort=False,hovertext = 'Category: Never consumed',
           marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
                       line=dict(color='#000000', width=2)),
           showlegend = False
           ),
    go.Pie(values=list(source_2['ID']),
           labels=source_2.index.values.tolist(),
           domain={'x': [0.2, 0.8], 'y': [0.1, 0.9]},
           hole=0.5,
           direction='clockwise',
           sort=False,
           hovertext = 'Category: Have stopped consuming',
           marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
                       line=dict(color='#000000', width=2)),
           showlegend=False),
    go.Pie(values=list(source_3['ID']),
           labels=source_3.index.values.tolist(),
           domain={'x': [0.1, 0.9], 'y': [0, 1]},
           hole=0.75,
           direction='clockwise',
           sort=False,hovertext = 'Category: Still Consuming',
        #    hovertemplate= '<br>percentage:{values}<br>labels: {labels}',
           marker=dict(colors=['#EC7063', '#F1948A', '#2E86C1', '#5DADE2', '#85C1E9'],
                       line=dict(color='#000000', width=2)),
           showlegend=True)]

col1, col2 = st.columns(2)

with col1:

    fig = go.Figure(data=data, layout={'title': 'Percentage distribution of people in a category'})

    st.session_state['click'] = plotly_events(fig)

    try:
        st.session_state['name'] = consum_dict[st.session_state['click'][0]['curveNumber']]
    except:
        st.session_state['name'] = "CL0"
with col2:
    if options == "Education":
        st.write(pd.DataFrame({
    #'first column': [0, 1, 2, 3, 4, 5, 6, 7, 8],
                                'Education level': ['Left school before 16 years','Left school at 16 years', 'Left school at 17 year','Left school at 18 years',
                                'Some college or university, no certificate or degree','Professional certificate/ diploma', 'University degree',
                                'Masters degree', 'Doctorate degree'],
                            }))

'''


'''

def sub_chart1(df, keys):
    
    
    source2 = df[df[keys['drug']] == st.session_state['name']]

    chart = alt.Chart(source2).mark_bar().encode(  
    
        x=alt.X('Gender', title = None, axis = alt.Axis(labels = False)),
        y=alt.Y('count(ID):Q',title = 'Number of people'),

        color=alt.Color('Gender', scale=alt.Scale(
 
                range=['#e7e1ef', '#c994c7']
        )),
        column=alt.Column(keys['options']
        ),
        tooltip = [keys['options'], 'Gender', 'count(ID)']
        ).properties(height=410
        ).configure_legend(orient='bottom'
)
        
    return chart

def sub_chart2(df, keys):
    
    source2 = df[df[keys['drug']] == st.session_state['name']]
    chart = alt.Chart(source2).transform_fold(
        keys['scores'],
        as_ = ['Personal_trait', 'value']
    ).transform_density(
        density='value',
        bandwidth=1,
        groupby=['Personal_trait'],
        extent= [15, 65],
        counts = True,
        steps=500
    ).mark_area(opacity = 0.5).encode(
        x = alt.X('value:Q'),
        y = alt.Y('density:Q', stack='zero'),
        color = alt.Color('Personal_trait:N'),
        tooltip = ['density:Q', 'value:Q', 'Personal_trait:N']

        
    )
    return chart

group_dict = dict()
group_dict = {'CL0': 'Never taken before', 'CL1':'Have stopped taking since a year ago', 'CL2': 'Still taking'}
st.write('### Detailed graphs for selected Group: ')
st.write('#####', group_dict[st.session_state['name']])

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.subheader('Number of people in selected category')
        st.write("##### Selected Category:", options)
        st.altair_chart(sub_chart1(df, keys), use_container_width=False) 


with col2:
        with st.container():
            st.subheader("Distribution of personal trait over selected category and drug")
            st.write("##### Selected category and drug: ", options, ",  ", drug)
            scores = st.multiselect(
            'Select the scores for personal trait:',
            ['Nscore', 'Escore', 'Oscore', 'Ascore', 'Cscore'], ['Nscore', 'Escore', 'Oscore', 'Ascore', 'Cscore'])
            
            keys['scores'] = scores
            '''
            
            








            '''
            st.altair_chart(sub_chart2(df, keys), use_container_width=True) 
            '''
            Personal trait has been measured with Five-Factor Model.(PT et al.) \n
            N-score: Neuroticism(N)\n
            E-score: Extraversion(E)\n
            O-score: Openness to Experience(O)\n
            A-score: Agreeableness(A)\n
            C-score: Conscientiousness(C)\n
            '''
