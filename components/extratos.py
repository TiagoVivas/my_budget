from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
from dash.dash_table.Format import Group
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd

from app import app

# ============ Layout ============ #
layout = dbc.Col([
    dbc.Row([
        html.Legend("Tabela de despesas"),
        html.Div(id='tabela-despesas', className='dbc')
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph',
                      style={'margin-right': '20px'})
        ], width=9),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Despesas'),
                    html.Legend("R$ 4400", 
                                id='valor_despesa_card', 
                                style={'font-size': '60px'}),
                    html.H6("Total de depesas")
                ], style={'text-align': 'center', 'padding-top': '30px'})
            ])
        ], width=3)
    ])
], style={'padding': '10px'})

# ============ Callbacks ============ #
