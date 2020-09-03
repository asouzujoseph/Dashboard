# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 15:08:30 2020

@author: Nnamdi
"""

import pandas as pd
import glob
import os
from datetime import datetime
import numpy as np
import random
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
import plotly.express as px

def UTCFormat (DF):
# ''' this function will convert the date and time to pandas Datetime format'''
    if ("Time" in DF.columns):
        DF['Datetime'] = pd.to_datetime(DF['Date'] +' '+ DF['Time'],dayfirst = True)
        DF = DF.drop(['Date','Time'], axis=1)
        DF = DF.set_index('Datetime').sort_index()
        DF = DF.dropna()
    elif ('Time PC' in DF.columns):
        DF['Datetime'] = pd.to_datetime(DF['Date'] +' '+ DF['Time PC'],dayfirst = True)
        DF = DF.drop(['Date','Time PC'], axis=1)
        DF = DF.set_index('Datetime').sort_index()
        DF = DF.dropna()
    return DF

# this function will make a dataframe of each file and all DFs as a dictionary with the name of the file as key
def combineFiles (path):
# ''' this function will concatenate raw files as data frames and save as a dictionary'''  
    bag = {}    # empty dictionary for storing dataframes
    files = glob.glob(path,recursive = True) # function to read all files even in subfolders
    for file in files: 
        xls = pd.ExcelFile(file)     # read excel file as a data frame
        if ("week 1" in xls.sheet_names): # condition to ensure that the file contains useful data
            df1 = pd.read_excel(xls, 'week 1')  # read each sheet as a data frame
            df2 = pd.read_excel(xls, 'week 2')
            df3 = pd.read_excel(xls, 'week 3')
            df4 = pd.read_excel(xls, 'week 4')
            df5 = pd.read_excel(xls, 'week 5')
            df6 = pd.read_excel(xls, 'week 6')
            filename = file.split('\\') # make a filename to act as key in the dictionary
            name = filename[-1]
            name2 = name.split('.')
            nameDF = name2[0]
            DF = pd.concat([df1,df2,df3,df4,df5,df6],axis =0) # concatenate the data frames into one mega data frame
            DF2 = UTCFormat(DF) # call function to create DateTime columns
            bag[nameDF] = DF2 # add the dataframe to the dictionary
    return bag


path = r'C:/Users/Nnamdi/Desktop/dashFi/**/*.xlsx'

dataFrames = combineFiles (path)  # function to create dictionary of dataframes

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
## write the instructions to appear in the web page
markdown_text = '''Please select a dataset'''
markdown2 = ''' Please select a variable'''

# design the layout of the web page
app.layout = html.Div(
    [     
     dcc.Markdown(children=markdown_text),  # radio button for the first instruction
     dcc.RadioItems(id='Dataset-radio',      # radio button for the datasets
     options=[{'label': k, 'value': k} for k in dataFrames.keys()],   # loop through name of datasets and use as radio buttons
     value='WATER_INTAKE'), # select "water_intake as the default dataset"
     
     html.Hr(), 
     
     dcc.Markdown(children=markdown2),   # radio button for the first instruction
     
     dcc.RadioItems(id='Variable-radio'), # use the variables in each dataset as radio buttons
     
     html.Hr(),
     
     dcc.Graph(id='indicator-graphic'),  # layout for the plots
    
    ])


@app.callback(
    Output('Variable-radio', 'options'),  #link output to the variables
    [Input('Dataset-radio', 'value')])		# use the datasets as input
def set_variable_options(selected_data):  # selects a dataset and the list of variables are the outputs
    return [{'label': i, 'value': i} for i in dataFrames[selected_data]]
     

@app.callback(
    Output('Variable-radio', 'value'),  # output is the variable (the second variable in each dataset is the default)
    [Input('Variable-radio', 'options')]) 
def set_variable_value(available_options):
    return available_options[1]['value']  # set default variable to the second variable



@app.callback(
    Output('indicator-graphic', 'figure'),  # output is a graph
    [Input('Dataset-radio', 'value'),  # input is the dataset
    Input('Variable-radio', 'value')])  # second input is the variable
def update_graph(dataset, variable):  # use the inputs as parameters in the function
    df = dataFrames[dataset]  # select the dataset
    fig = px.line(df,x=df.index,y=df[variable], title = 'Graph of ' + str(variable)) # make a line plot
    return fig # the returned figure is given as the output


if __name__ == '__main__':
    app.run_server(debug=True)






















