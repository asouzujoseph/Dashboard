# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 15:08:30 2020

@author: Nnamdi
"""

import pandas as pd
from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

#### load the raw data and prepare the dataset
url = "https://raw.githubusercontent.com/asouzujoseph/Dashboard/master/dataset.csv"
df = pd.read_csv(url, header=[0,1])
dataFrames = {} # create a dictionary of dataframes
keys = ['CLIMATE', 'FEED_INTAKE', 'WATER_INTAKE']
for key in keys:
    value = df[key]
    value['Datetime'] = pd.to_datetime(value['Datetime'])
    value = value.set_index('Datetime', inplace=False).sort_index()
    value = value.drop(['Day'], axis=1)
    dataFrames[key] = value

#### design the dashboard
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
colors = {
    'background': 'white',
    'text': 'blue'
}

#### write the instructions to appear in the web page
markdown_text = '''Select a dataset'''
markdown2 = ''' Select a variable'''
markdown3 = ''' Select a date range '''


#### design the layout of the web page
app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(children='Smart Farm Analytics',
            style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
      html.Div([   
          html.Div([  
          dcc.Markdown(children=markdown_text),  # radio button for the first instruction
          dcc.RadioItems(id='Dataset-radio',      # radio button for the datasets
          options=[{'label': k, 'value': k} for k in dataFrames.keys()],   # loop through name of datasets and use as radio buttons
          value='WATER_INTAKE')]),      # select "water_intake as the default dataset" 
           
          
           html.Br(),
          html.Div([       
          dcc.Markdown(children=markdown2),   # radio button for the first instruction
          dcc.RadioItems(id='Variable-radio')]), # use the variables in each dataset as radio buttons
           html.Br(),
         
          html.Div([
          dcc.Markdown(children=markdown3),
          dcc.DatePickerRange(id="date_picker_range",
                              start_date_placeholder_text="StartPeriod",
                              end_date_placeholder_text="EndPeriod",
                              calendar_orientation='horizontal',
                              start_date = dt(2020,5,22).date())])
      
     ],style={'columnCount': 3}),
          
      html.Br(),
      dcc.Graph(id='indicator-graphic')  # layout for the plots
     

     
])
      
                             
      
      # html.h3("Time series analysis", style ={'textAlign':'center'})
     
    
#### Interactivity between the components
@app.callback(
    Output('Variable-radio', 'options'),  #link output to the variables
    [Input('Dataset-radio', 'value')])		# use the datasets as input
def set_variable_options(selected_data):  # selects a dataset and the list of variables are the outputs
    " this function will select a dataframe in the dictionary of dataframes"
    return [{'label': i, 'value': i} for i in dataFrames[selected_data]]
     

@app.callback(
    Output('Variable-radio', 'value'),  # output is the variable (the second variable in each dataset is the default)
    [Input('Variable-radio', 'options')]) 
def set_variable_value(available_options):
    " this function will use the first variable in the selected dataframe as default variable"
    return available_options[1]['value']  # set default variable to the second variable



@app.callback(
    Output('indicator-graphic', 'figure'),  # output is a graph
    [Input('Dataset-radio', 'value'),  # first input is the dataset
    Input('Variable-radio', 'value'), # second input is the variable
    Input('date_picker_range','start_date'), # third input is the start date
    Input('date_picker_range','end_date')])  # fourth input is the end date
def update_graph(dataset, variable,start_date,end_date):  # use the inputs as parameters in the function
    df = dataFrames[dataset]  # select the  from the dictionary
    dff = df.loc[start_date:end_date] # fikter out data using the dates
    fig = px.line(dff,y=dff[variable], title = 'Plot of ' + str(variable)) # make a line plot
    fig = fig.update_layout(showlegend=False,  plot_bgcolor="pink", paper_bgcolor=colors['background'],font_color=colors['text']) # modify aesthetics of the plot
    return fig 


if __name__ == '__main__':
    app.run_server(debug=True)




















