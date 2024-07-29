#Import Libraries
from dash import html, dcc, Input, Output, State, dash_table, Dash, ctx, callback
from dash_auth import BasicAuth
from flask import request

import dash_auth
from dash_auth import BasicAuth

import dash_bootstrap_components as dbc

import warnings
warnings.filterwarnings('ignore')

from view1 import *

from model1 import upload_files_model,parse_contents_model, createjoindata_model, generate_auto_refresh_data_descr_table_model,dropdownsData_model, dropdownsData1_model, barChart_model,pieChart_model,CorrelationMatrixChart_model


# Existing app initialization and authentication code
VALID_USERNAME_PASSWORD_PAIRS = {
    'test': 'testakis',
    'admin': 'admin',
    'nikos': 'papadakis'
}

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

#Layout code

# Dash layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(id='dummy-output', style={'display': 'none'}),
], style={'background-color':'rgb(255,255,255)'}) #background Color 


#Callbacks

# Callback to set the authenticated username in a dummy output
@app.callback(Output('dummy-output', 'children'),
              [Input('url', 'pathname')])
def set_authenticated_username(pathname):
    if auth.is_authorized():
        return request.authorization.username
    else:
        return ''

# Callback to update the page content based on user role (admin or simple user)
@app.callback(Output('page-content', 'children'),
              [Input('dummy-output', 'children')])
def display_page(username):
    if username:
        if username == 'admin':
            return admin_layout
        else:
            return user_layout
    else:
        return html.P("You are not logged in.")

#-------------------------------------------------------------------------------------

#Data Uploader & file info update paragraph
#Inputs: Uploaded data
#Outputs: Filename, Number of rows & columns
@app.callback(Output('uploadInfo', 'children'),
              [Input('datatable-upload', 'contents')],
              [State('datatable-upload', 'filename')])

def upload_files(list_of_contents, list_of_names):
    return upload_files_model(list_of_contents, list_of_names)


#Dataview table
#Inputs: uploaded data
#Output: dataviewTable
#Also joins data with same column name and creates dataframe

def parse_contents(contents, filename):
    return parse_contents_model(contents, filename)


@app.callback(Output('dataviewTable', 'data'),
              Output('dataviewTable', 'columns'),
            Input('datatable-upload', 'contents'),
            State('datatable-upload', 'filename'),
            prevent_initial_call=True)


def createjoindata(list_of_contents, list_of_names):
    return createjoindata_model(list_of_contents, list_of_names)


# This callback generates Data describe table and auto-refresh it when we filter data in datasetView Table
#Inputs: Data from dataview table
#Outputs: data descibre table
@app.callback(
    Output('descTable', "children"),
    Input('dataviewTable', 'derived_virtual_data'),
    prevent_initial_call=True
)

def generate_auto_refresh_data_descr_table(data):
    return generate_auto_refresh_data_descr_table_model(data)


#makes dropDown menus dynamic
#Inputs: DataView data
#Outputs: Dataframe columms to dropdowns options
@app.callback(
    Output('dropdown1','options'),
    Output('dropdown2','options'),
    # Output('dropdown3','options'),
    Input('dataviewTable', 'derived_virtual_data'),
    prevent_initial_call=False
)

def dropdownsData(data):
    return dropdownsData_model(data)


#makes dropDown menu 4 ONLY dynamic
#Inputs: DataView data
#Outputs: Dataframe columms to dropdowns options
@app.callback(
    Output('dropdown3', 'options'),
    Output('dropdown4','options'),
    Input('dataviewTable', 'derived_virtual_data'),
    prevent_initial_call=False
)

def dropdownsData1(data):
    return dropdownsData1_model(data)


'''graphs'''

# Creates callback Graph Counts (interactive)
#Inputs: data from dropdown menus(1,2) and dataviewTable
#Outputs: Counts Distribution Graph
@app.callback(
    Output('countsPlot', 'figure'),
    Input('dataviewTable', "derived_virtual_data"),
    Input('dataviewTable', "derived_virtual_selected_rows"),
    Input('dropdown1', 'value'),
    Input('dropdown2', 'value'),
    prevent_initial_call=True
)

def barChart(rows, derived_virtual_selected_rows, valuedp1, valuedp2):
    return barChart_model(rows, derived_virtual_selected_rows, valuedp1, valuedp2)


# Callback to update the pie chart based on dropdown selection
@app.callback(Output('pie-chart', 'figure'),
              Input('dataviewTable', "derived_virtual_data"),
              Input('dropdown3', 'value'),
              Input('dropdown4', 'value'),
              prevent_initial_call=True)


def pieChart(rows, names, values):
    return pieChart_model(rows, names, values)


#Generate  Correlation Matrix
#Inputs: DataView data
#Outputs: Correlation matrix Figure
@app.callback(
    Output('cormatrix','figure'),
    Input('dataviewTable', 'derived_virtual_data'),
    prevent_initial_call=True
)

def CorrelationMatrixChart(data):
    return CorrelationMatrixChart_model(data)


#Main-run app
if __name__ == '__main__':
    app.run(debug=False)
