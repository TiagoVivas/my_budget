from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *

from app import app

card_icon = {
    'color': 'white',
    'textAlign': 'center',
    'fontSize': 30,
    'margin': 'auto'
}

graph_margin = dict(l=25, r=25, t=25, b=0)

# ============ Layout ============ #
layout = dbc.Col([
# Seção com cards de KPIs-------------
    dbc.Row([
        # Saldo total
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Saldo"),
                    html.H5("R$ 5400,00", 
                            id='p-saldo-dashboards', 
                            style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card([
                    html.Div(className='fa fa-university', style=card_icon),
                ], color='warning', style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'})
            ])
        ], width=4),

        # Receita
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Receita"),
                    html.H5("R$ 10000,00", 
                            id='p-receita-dashboards', 
                            style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card([
                    html.Div(className='fa fa-smile-o', style=card_icon),
                ], color='success', style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'})
            ])
        ], width=4),

        # Despesa
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Despesa"),
                    html.H5("R$ 4600,00", 
                            id='p-despesa-dashboards', 
                            style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card([
                    html.Div(className='fa fa-meh-o', style=card_icon),
                ], color='danger', style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'})
            ])
        ], width=4),
    ], style={'margin': '10px'}),

    dbc.Row([
        dbc.Col([
# Seção Filtro de lançamentos ------------
            dbc.Card([
                html.Legend("Filtrar lançamentos", className='card-title'),
                html.Label("Categorias das receitas"),
                html.Div(dcc.Dropdown(id='dropdown-receita',
                                      clearable=False,
                                      style={'width': '100%'},
                                      persistence=True,
                                      persistence_type='session',
                                      multi=True)),
                html.Label("Categorias das despesas"),
                html.Div(dcc.Dropdown(id='dropdown-despesa',
                                      clearable=False,
                                      style={'width': '100%'},
                                      persistence=True,
                                      persistence_type='session',
                                      multi=True)),
                html.Legend("Período de análise", style={'margin-top': '10px'}),
                dcc.DatePickerRange(id='date-picker-config',
                                    month_format='Do MMM, YY',
                                    end_date_placeholder_text='Data...',
                                    start_date=datetime(2022, 4, 1).date(),
                                    end_date=datetime.today() + timedelta(days=31),
                                    updatemode='singledate',
                                    style={'z-index': '100'})
            ], style={'height': '100%', 'padding': '20px'}),
        ], width=4),
# Seção gráfico -------------------------------
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph1')
            ], style={'height': '100%', 'padding': '10px'})
        ], width=8)
        
    ], style={'margin': '10px'}),
# Seção de gráficos inferiores-----------------
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph2')
            ], style={'padding': '10px'})
        ], width=6),

        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph3')
            ], style={'padding': '10px'})
        ], width=3),

        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph4')
            ], style={'padding': '10px'})
        ], width=3)
    ], style={'margin': '10px'})

])

# ============ Callbacks ============ #
@app.callback(
    [
        Output('dropdown-receita', 'options'),
        Output('dropdown-receita', 'value')
    ],
    Input('store-receitas', 'data'),
)
def populate_dropdownvalues_receita(data):
    df = pd.DataFrame(data)

    val = df.Categoria.unique().tolist()
    lista_opcoes = [{'label': i, 'value': i} for i in val]

    return (lista_opcoes, val)

@app.callback(
    [
        Output('dropdown-despesa', 'options'),
        Output('dropdown-despesa', 'value'),
    ],
    Input('store-despesas', 'data'),
)
def populate_dropdownvalues_despesa(data):
    df = pd.DataFrame(data)

    val = df.Categoria.unique().tolist()
    lista_opcoes = [{'label': i, 'value': i} for i in val]

    return (lista_opcoes, val)

@app.callback(
    [
        Output('p-saldo-dashboards', 'children'),
        Output('p-despesa-dashboards', 'children'),
        Output('p-receita-dashboards', 'children')
    ],
    [
        Input('store-receitas', 'data'),
        Input('store-despesas', 'data'),
        Input('dropdown-despesa', 'value'),
        Input('dropdown-receita', 'value'),
        Input('date-picker-config', 'start_date'),
        Input('date-picker-config', 'end_date')
    ]
    
)
def populate_dropdownvalues_saldo(receitas, despesas, filtro_despesas, filtro_receitas, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_receitas = pd.DataFrame(receitas)
    # Filtro de categorias
    df_receitas = df_receitas[(df_receitas['Categoria'].isin(filtro_receitas))]
    # Filtro de datas
    df_receitas['Data'] = pd.to_datetime(df_receitas['Data'])
    df_receitas = df_receitas[(df_receitas['Data'] >= start_date) & (df_receitas['Data'] <= end_date)]
    valor_receita = df_receitas['Valor'].sum()

    df_despesas = pd.DataFrame(despesas)
    # Filtro de categorias
    df_despesas = df_despesas[(df_despesas['Categoria'].isin(filtro_despesas))]
    # Filtro de datas
    df_despesas['Data'] = pd.to_datetime(df_despesas['Data'])
    df_despesas = df_despesas[(df_despesas['Data'] >= start_date) & (df_despesas['Data'] <= end_date)]
    valor_despesa = df_despesas['Valor'].sum()

    valor = valor_receita - valor_despesa

    return (f"R$ {valor}", f"R$ {valor_despesa}", f"R$ {valor_receita}")

@app.callback(
    Output('graph1', 'figure'),
    [
        Input('store-despesas', 'data'),
        Input('store-receitas', 'data'),
        Input('dropdown-despesa', 'value'),
        Input('dropdown-receita', 'value'),
        Input('date-picker-config', 'start_date'),
        Input('date-picker-config', 'end_date')
    ]
)
def update_graph1(data_despesa, data_receita, despesas, receitas, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_despesas = pd.DataFrame(data_despesa)
    df_despesas['Data'] = pd.to_datetime(df_despesas['Data'])
    # Filtro de datas
    df_despesas = df_despesas[(df_despesas['Data'] >= start_date) & (df_despesas['Data'] <= end_date)]
    # Filtro de categorias
    df_despesas = df_despesas[(df_despesas['Categoria'].isin(despesas))]
    df_despesas.set_index('Data', inplace=True)
    valores_despesas = df_despesas[['Valor']]
    valores_despesas = valores_despesas.groupby('Data').sum()
    valores_despesas.rename(columns={'Valor': 'Despesa'}, inplace=True)
    
    df_receitas = pd.DataFrame(data_receita)
    df_receitas['Data'] = pd.to_datetime(df_receitas['Data'])
    # Filtro de datas
    df_receitas = df_receitas[(df_receitas['Data'] >= start_date) & (df_receitas['Data'] <= end_date)]
    # Filtro de categorias
    df_receitas = df_receitas[(df_receitas['Categoria'].isin(receitas))]
    df_receitas.set_index('Data', inplace=True)
    valores_receitas = df_receitas[['Valor']]
    valores_receitas = valores_receitas.groupby('Data').sum()
    valores_receitas.rename(columns={'Valor': 'Receita'}, inplace=True)

    df_acum = valores_despesas.join(valores_receitas, how='outer').fillna(0)
    df_acum['Acum'] = (df_acum['Receita'] - df_acum['Despesa']).cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Fluxo de caixa', x=df_acum.index, y = df_acum['Acum'], mode='lines'))

    fig.update_layout(margin=graph_margin, height=350)
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)')

    return fig

@app.callback(
    Output('graph2', 'figure'),
    [
        Input('store-receitas', 'data'),
        Input('store-despesas', 'data'),
        Input('dropdown-receita', 'value'),
        Input('dropdown-despesa', 'value'),
        Input('date-picker-config', 'start_date'),
        Input('date-picker-config', 'end_date'),
    ]
)
def update_graph2(data_receita, data_despesa, receitas, despesas, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_despesas = pd.DataFrame(data_despesa)
    df_despesas['Output'] = "Despesas"

    df_receitas = pd.DataFrame(data_receita)
    df_receitas['Output'] = "Receitas"

    df_final = pd.concat([df_despesas, df_receitas]).reset_index(drop=True)
    df_final['Data'] = pd.to_datetime(df_final['Data'])
    # Filtro de datas
    df_final = df_final[(df_final['Data'] >= start_date) & (df_final['Data'] <= end_date)]
    # Filtro de categorias
    df_final = df_final[(df_final['Categoria'].isin(receitas)) | (df_final['Categoria'].isin(despesas))]

    fig = px.bar(df_final, x="Data", y='Valor', color='Output', barmode='group')

    fig.update_layout(margin=graph_margin, height=300)
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)')

    return fig

@app.callback(
    Output('graph3', 'figure'),
    [
        Input('store-receitas', 'data'),
        Input('dropdown-receita', 'value'),
        Input('date-picker-config', 'start_date'),
        Input('date-picker-config', 'end_date'),
    ]
)
def pie_receita(data_receita, receitas, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df = pd.DataFrame(data_receita)
    # Filtro de categorias
    df = df[df['Categoria'].isin(receitas)]
    # Filtro de datas
    df['Data'] = pd.to_datetime(df['Data'])
    df = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]

    fig = px.pie(df, values=df.Valor, names=df.Categoria, hole=.2)

    fig.update_layout(title={'text': 'Receitas'})
    fig.update_layout(margin=graph_margin, height=300)
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)')

    return fig

@app.callback(
    Output('graph4', 'figure'),
    [
        Input('store-despesas', 'data'),
        Input('dropdown-despesa', 'value'),
        Input('date-picker-config', 'start_date'),
        Input('date-picker-config', 'end_date'),
    ]
)
def pie_despesa(data_despesa, despesas, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df = pd.DataFrame(data_despesa)
    # Filtro de categorias
    df = df[df['Categoria'].isin(despesas)]
    # Filtro de datas
    df['Data'] = pd.to_datetime(df['Data'])
    df = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]

    fig = px.pie(df, values=df.Valor, names=df.Categoria, hole=.2)

    fig.update_layout(title={'text': 'Despesas'})
    fig.update_layout(margin=graph_margin, height=300)
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)')

    return fig