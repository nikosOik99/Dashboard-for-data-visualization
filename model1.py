#Import Libraries
import base64
import io
import pandas as pd
import functools as ft
import numpy as np
from dash import dash_table, Dash, ctx, callback
from dash import html, dcc, Input, Output, State
import plotly.figure_factory as ff
import plotly.express as px


def upload_files_model(list_of_contents, list_of_names):
    if list_of_contents is not None:
        # Read data into a Pandas DataFrame
        dataframes = []
        for content, name in zip(list_of_contents, list_of_names):
            content_type, content_string = content.split(',')
            decoded = base64.b64decode(content_string)
            try:
                if 'csv' in name:
                    # Assume that the user uploaded a CSV file
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                elif 'xls' in name:
                    # Assume that the user uploaded an Excel file
                    df = pd.read_excel(io.BytesIO(decoded))
                dataframes.append(df)
            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error processing file ',
                    html.B(name),
                    '. Please try again.'
                ])

        # Combine all dataframes into one
        df = pd.concat(dataframes, ignore_index=True)

        # Generate success message and display number of rows and columns
        message = f"Filename(s): {', '.join(list_of_names)} "
        message += f" | Number of rows: {len(df)} | Number of Columns: {len(df.columns)}"
        return html.Div(message)

    else:
        return html.Div()


def parse_contents_model(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))



def createjoindata_model(list_of_contents, list_of_names):

    if list_of_contents is not None:
        try:
            children = [
                parse_contents_model(c, n) for c, n in
                zip(list_of_contents, list_of_names)
            ]
        except UnboundLocalError:
            print("No problem-Just waiting for data")

    #Merge datasets On first common Colunm
    # extract column names into a list (cols)
    cols = []
    for df in children:
        cols.append(df.columns)

    # Find common column name to use it as key to merge datasets (dynamic)
    # on='element'

    Output = set(cols[0])
    for l in cols[1:]:
        Output &= set(l)

    Output = list(Output)
    element = Output[0]

    df_final = ft.reduce(lambda left, right: pd.merge(left, right, on=element), children)
    df_return = df_final.to_dict('records'), [{"name": i, "id": i} for i in df_final.columns]

    return df_return


def generate_auto_refresh_data_descr_table_model(data):

    empty_table = {} #in case of None Data
    if data is not None:
        try:
            df = pd.DataFrame(data)
            df_desc = df.describe().reset_index()  # Data describe dataframe

            descTable = dash_table.DataTable(
                data=df_desc.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df_desc.columns],

                #Style cells
                style_table={'overflowX': 'auto'},  # makes the table to fit in side bar
                style_cell={
                    'height': 'auto',
                    # all three widths are needed
                    'minWidth': '50px', 'width': '100px', 'maxWidth': '500px',
                    'whiteSpace': 'nowrap'
                },  # grey-white Striped Rows
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(242, 242, 242)',
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(98, 160, 240)',
                    'color': 'white'
                }
            )

            return descTable
        except Exception as e:
            #print(e)
            return empty_table


def dropdownsData_model(data):

    df = pd.DataFrame(data) #convert data to dataframe

    return df.columns,df.columns #returns only the columns


def dropdownsData1_model(data):

    df = pd.DataFrame(data) #convert data to dataframe

    # Select columns with numeric values
    numeric_columns = df.select_dtypes(include=np.number).columns
    categorical_columns = df.select_dtypes(exclude=np.number).columns


    return [{'label': col, 'value': col} for col in categorical_columns], [{'label': col, 'value': col} for col in numeric_columns]

'''
Functions for Graphs (Bar, Pie, Correlation Matrix)
'''

def barChart_model(rows, derived_virtual_selected_rows, valuedp1, valuedp2):

    empty_counts_plot={}
    if derived_virtual_selected_rows is not None:
        try:
            try:

                df = pd.DataFrame(rows) #conv to dataframe

                dff = df if rows is None else pd.DataFrame(rows)

                # fig = px.histogram(dff, x=valuedp1,
                #                    title=f"Data Distribution - Counts for {valuedp1}", color=dff[valuedp2],
                #                    height=500,
                #                    text_auto='.3s',
                #                    histfunc="count")

                fig = px.bar(dff, x=valuedp1, y=valuedp2)


                return fig

            except ValueError as v:
                # print(v)
                return empty_counts_plot
        except KeyError as k:
            #print(k)
            return empty_counts_plot


def pieChart_model(rows, names, values):
    empty_pie_plot = {}

    try:
        df = pd.DataFrame(rows)  # conv to dataframe
        dff = df if rows is None else pd.DataFrame(rows)

        fig = px.pie(dff, values=values, names=names, title="Pie Chart")
        fig.update_traces(textposition='inside', textinfo='percent+label')
    except ValueError as v:
        return empty_pie_plot

    return fig


def CorrelationMatrixChart_model(data):

    empty_matrix={}

    if data is not None:
        try:
            df = pd.DataFrame(data)
            df_corr = df.select_dtypes(include=np.number).corr()
            x = list(df_corr.columns)
            y = list(df_corr.index)
            z = df_corr.values

            fig_corr = ff.create_annotated_heatmap(
                z,
                x=x,
                y=y,
                annotation_text=np.around(z, decimals=2),
                hoverinfo='z',
                colorscale='Blues',
            )

            fig_corr.update_layout(autosize=True,
                                   margin=dict(l=40, r=20, t=20, b=20),
                                   paper_bgcolor='rgba(0,0,0,0)'
                                   )
            return fig_corr
        except IndexError as i:
            #print(i)
            return empty_matrix