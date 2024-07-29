#Libraries
from dash import  Input, Output
from controller1 import *
from dash import html, dcc
from model1 import parse_contents_model, createjoindata_model, generate_auto_refresh_data_descr_table_model


accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.P('Select column (x-axis)', style={'margin-top': '10px'}),
                            dcc.Dropdown(
                                id='dropdown1',
                                value=''
                            ),
                        ]),

                        dbc.Col([
                            html.P('Select column to pair', style={'margin-top': '10px'}),
                            dcc.Dropdown(
                                id='dropdown2',
                                value='', style={'margin-bottom': '15px'}
                            )
                        ]),
                    ]),
                dcc.Graph(id='countsPlot', figure={}, style={'margin-bottom': '15px'}),]), title= "Bar Chart"
            ),
            dbc.AccordionItem(
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.P('Select Names', style={'margin-top': '10px'}),
                            dcc.Dropdown(
                                id='dropdown3',
                                value=''
                            ),
                        ]),

                        dbc.Col([
                            html.P('Select Values', style={'margin-top': '10px'}),
                            dcc.Dropdown(
                                id='dropdown4',
                                value='', style={'margin-bottom': '15px'}
                            )
                        ]),
                    ]),
                dcc.Graph(id='pie-chart', figure={}, style={'margin-bottom': '15px'}),]), title= "Pie Chart"
                ),
            dbc.AccordionItem(
                dcc.Graph(id='cormatrix', figure={}),title="Correlation Matrix"
            ),
        ],
        start_collapsed=True,
    ),
)


# Admin Layout
admin_layout = dbc.Container([

dbc.Row([
    html.H1("Data Visualization Application", style={'text-align': 'center'}),
    html.H2("Admin Dashboard", style={'text-align':'center'}),

        html.Table(
            # Header
            [html.Tr([html.Th("Users", style={'border': '1px solid #dddddd','text-align': 'center','padding': '8px',}),
                      html.Th("Passwords", style={'border': '1px solid #dddddd','text-align': 'center','padding': '8px',})])] +
            # Rows
            [html.Tr([html.Td(user, style={'border': '1px solid #dddddd','text-align': 'center','padding': '8px',}),
                      html.Td(password, style={'border': '1px solid #dddddd','text-align': 'center','padding': '8px',})]) for user, password in
             VALID_USERNAME_PASSWORD_PAIRS.items()]
        ),
    ])
], style={'width': '50%', 'margin': 'auto', 'border-collapse': 'collapse', 'margin-top': '20px'})

# User Layout
user_layout = dbc.Container([
    dbc.Row([
            html.Div('Data Visualization Application', className="text-primary text-center fs-3")
        ]),

        # Shows loading circle while loading data that user uploaded
        dcc.Loading(
            id="loading",
            type="circle",
            children=[
                # Shows files information (fileName,Rows, Columns)
                html.Div(id='uploadInfo', style={'font-size': '16px', 'text-align': 'center'})
            ]
        ),

        #Data Uploader Component
        html.Div(className='row', children=[
            dcc.Loading(
                dcc.Upload(
                    id='datatable-upload',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%', 'height': '60px', 'lineHeight': '60px',
                        'borderWidth': '1px', 'borderStyle': 'dashed',
                        'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                    },
                    multiple=True  # allow us to upload/select multiple files through uploader
                )
            )
        ]),


        #Diagrams Area Plan

        dbc.Row([
             dbc.Col([
                 dbc.Row([
                     accordion
                 ]),


             ], width=6),

            #Data Describe-Statistic Table
            dbc.Col([
                html.P('Data Statistic Table',
                       style={'textAlign': 'center', 'color': 'blue', 'fontSize': 15, 'margin-top': 5}),
                dcc.Loading(
                    id='loading_datadesc_table',
                    type='circle',
                    children=[
                        html.Div(id='descTable', children=[])
                    ]
                ),
            ], width=6),
        ]),


        #Data Preview Table
        dbc.Row([

            html.P('Data View Table',style={'textAlign': 'center', 'color': 'blue', 'fontSize':15, 'margin-top':35}),

            # Shows loading circle while loading data to DataView Table
            dcc.Loading(
                id='loading_dataview_table',
                type='circle',
                children=[
                    dash_table.DataTable(
                        id='dataviewTable',

                        # displays 100 rows/page and allows filtering data
                        page_size=20,
                        filter_action="native",

                        # Style table cells
                        style_table={'overflowX': 'auto'},
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
                ]
            )
        ])
], fluid=True)