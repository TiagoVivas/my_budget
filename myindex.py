import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

from app import app
from components import dashboards, sidebar, extratos
from globals import *

# ============ Layout ============ #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
# Componentes para armazenar os dados que estão sendo trabalhados na sessão atual ----- 
    dcc.Store(id='store-receitas',
              data=df_receitas.to_dict()),
    dcc.Store(id='store-despesas',
              data=df_despesas.to_dict()),
    dcc.Store(id='store-cat-receitas',
              data=df_cat_receitas.to_dict()),
    dcc.Store(id='store-cat-despesas',
              data=df_cat_despesas.to_dict()),

# Componentes de layout da página ---------------------
    dbc.Row([
        dbc.Col([
            dcc.Location(id='url'), 
            sidebar.layout
        ], md=2), # ocupa 2/12 da página
        dbc.Col([
            content
        ], md=10) # ocupa 10/12 da página
    ])

], fluid=True)

# ============ Callbacks ============ #
@app.callback(
    Output('page-content', 'children'), 
    [Input('url', 'pathname')]
)
def render_page(pathname):
    # Página principal
    if (pathname == '/') or (pathname == '/dashboards'):
        return dashboards.layout

    # Página de extratos
    if pathname == '/extratos':
        return extratos.layout


if __name__ == '__main__':
    app.run_server(port=8051, debug=True)


