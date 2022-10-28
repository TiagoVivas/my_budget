from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
from dash.dash_table.Format import Group
import dash_bootstrap_components as dbc

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd

from app import app
from globals import *

# ============ Layout ============ #
layout = dbc.Col([
    html.H1("MyBudget", className='text-primary'), # Título
    html.P("By ASIMOV", className='text-info'), # Parágrafo
    html.Hr(), # Quebra de linha

# Seção PERFIL ----------------------
    dbc.Button(id='botao_avatar',
               children=[html.Img(src='/assets/img_hom.png', 
                                  id='avatar_change', 
                                  alt='Avatar', 
                                  className='perfil_avatar')],
                style={'background-color': 'transparent', 'border-color': 'transparent'}),

# Seção ADICIONAR RECEITA/DESPESA----
    dbc.Row([
        dbc.Col([
            dbc.Button(id='open-novo-receita',
                       children=['+ Receita'],
                       color='success')
        ], width=6), 
        dbc.Col([
            dbc.Button(id='open-novo-despesa',
                       children=['- Despesa'],
                       color='danger')
        ], width=6)
    ]),

    # Modal para adição de receitas
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar receita')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Descrição: "),
                    dbc.Input(id='txt-receita', 
                              placeholder="Ex.: dividendos da bolsa, herança...")
                ], width=6), 
                dbc.Col([
                    dbc.Label("Valor: "),
                    dbc.Input(id='valor-receita', 
                              placeholder="R$ 100,00",
                              value="")
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Data: "),
                    dcc.DatePickerSingle(id='date-receitas',
                                         min_date_allowed=date(2020, 1, 1),
                                         max_date_allowed=date(2030, 12, 31),
                                         date=datetime.today(),
                                         style={'width': '100%'})
                ], width=4), 
                dbc.Col([
                    dbc.Label("Extras: "),
                    dbc.Checklist(id='switches-input-receita',
                                  options=[{'label': "Foi recebida", 'value': 1},
                                           {'label': "Receita recorrente", 'value': 2}],
                                  value=[1],
                                  switch=True)
                ], width=4),
                dbc.Col([
                    html.Label("Categoria da receita"),
                    dbc.Select(id='select_receita',
                               options=[{'label': i, 'value': i} for i in cat_receita],
                               value=[cat_receita[0]])
                ], width=4)
            ], style={'margin-top': '25px'}),
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Adicionar categoria",
                                            style={'color': 'green'}),
                                dbc.Input(id='input-add-receita', 
                                          type='text',
                                          placeholder="Nova categoria...",
                                          value=""),
                                html.Br(),
                                dbc.Button("Adicionar", 
                                           id='add-category-receita', 
                                           className='btn btn-success',
                                           style={'margin-top': '20px'}),
                                html.Br(),
                                html.Div(id='category-div-add-receita', 
                                         style={})
                            ], width=6),
                            dbc.Col([
                                html.Legend("Excluir categoria",
                                            style={'color': 'red'}),
                                dbc.Checklist(id='checklist-selected-style-receita',
                                              options=[{'label': i, 'value': i} for i in cat_receita],
                                              value=[],
                                              label_checked_style={'color': 'red'},
                                              input_checked_style={'backgroundColor': 'blue', 
                                                                   'borderColor': 'orange'}),
                                dbc.Button("Remover", 
                                           id='remove-category-receita', 
                                           color='warning', 
                                           style={'margin-top': '20px'})
                                
                            ],width=6)
                        ])
                    ], title="Adicionar/Remover categorias")
                ], flush=True, start_collapsed=True, id='accordion-receita'),

                html.Div(id='id_teste_receita', style={'padding-top': '20px'}),
                dbc.ModalFooter([
                    dbc.Button("Adicionar receita",
                               id='salvar_receita',
                               color='success'),
                    dbc.Popover(dbc.PopoverBody("Receita salva"), 
                                target='salvar_receita',
                                placement='left',
                                trigger='click')
                ])
            ], style={'margin-top': '25px'})
        ])
    ], id='modal-novo-receita', 
       style={'background-color': 'rgba(17, 140, 79, 0.05)'},
       size='lg',
       is_open=False,
       centered=True,
       backdrop=True),

    # Modal para adição de despesas
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar despesa')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Descrição: "),
                    dbc.Input(id='txt-despesa', 
                              placeholder="Ex.: Aluguel, conta de energia...")
                ], width=6), 
                dbc.Col([
                    dbc.Label("Valor: "),
                    dbc.Input(id='valor-despesa', 
                              placeholder="R$ 100,00",
                              value="")
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Data: "),
                    dcc.DatePickerSingle(id='date-despesa',
                                         min_date_allowed=date(2020, 1, 1),
                                         max_date_allowed=date(2030, 12, 31),
                                         date=datetime.today(),
                                         style={'width': '100%'})
                ], width=4), 
                dbc.Col([
                    dbc.Label("Extras: "),
                    dbc.Checklist(id='switches-input-despesa',
                                  options=[{'label': "Foi recebida", 'value': 1},
                                           {'label': "Receita recorrente", 'value': 2}],
                                  value=[1],
                                  switch=True)
                ], width=4),
                dbc.Col([
                    html.Label("Categoria da despesa"),
                    dbc.Select(id='select_despesa',
                               options=[{'label': i, 'value': i} for i in cat_despesa],
                               value=[cat_despesa[0]])
                ], width=4)
            ], style={'margin-top': '25px'}),
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Adicionar categoria",
                                            style={'color': 'green'}),
                                dbc.Input(id='input-add-despesa', 
                                          type='text',
                                          placeholder="Nova categoria...",
                                          value=""),
                                html.Br(),
                                dbc.Button("Adicionar", 
                                           id='add-category-despesa', 
                                           className='btn btn-success',
                                           style={'margin-top': '20px'}),
                                html.Br(),
                                html.Div(id='category-div-add-despesa', 
                                         style={})
                            ], width=6),
                            dbc.Col([
                                html.Legend("Excluir categoria",
                                            style={'color': 'red'}),
                                dbc.Checklist(id='checklist-selected-style-despesa',
                                              options=[{'label': i, 'value': i} for i in cat_despesa],
                                              value=[],
                                              label_checked_style={'color': 'red'},
                                              input_checked_style={'backgroundColor': 'blue', 
                                                                   'borderColor': 'orange'}),
                                dbc.Button("Remover", 
                                           id='remove-category-despesa', 
                                           color='warning', 
                                           style={'margin-top': '20px'})
                                
                            ],width=6)
                        ])
                    ], title="Adicionar/Remover categorias")
                ], flush=True, start_collapsed=True, id='accordion-despesa'),

                html.Div(id='id_teste_despesa', style={'padding-top': '20px'}),
                dbc.ModalFooter([
                    dbc.Button("Adicionar despesa",
                               id='salvar_despesa',
                               color='danger'),
                    dbc.Popover(dbc.PopoverBody("Despesa salva"), 
                                target='salvar_despesa',
                                placement='left',
                                trigger='click')
                ])
            ], style={'margin-top': '25px'})
        ])
    ], id='modal-novo-despesa', 
       style={'background-color': 'rgba(17, 140, 79, 0.05)'},
       size='lg',
       is_open=False,
       centered=True,
       backdrop=True),

# Seção NAVEGAÇÃO--------------------
    html.Hr(),
    dbc.Nav([
        dbc.NavLink("Dashboard", href='/dashboards', active='exact'),
        dbc.NavLink("Extratos", href='/extratos', active='exact')
    ], id='nav_buttons', vertical=True, pills=True, style={'margin-bottom': '50px'}) 
    # pills = destaque ao redor quando clicado

], id='sidebar_completa')


# ============ Callbacks ============ #
# Pop-up receita
@app.callback(
    Output('modal-novo-receita', 'is_open'),
    Input('open-novo-receita', 'n_clicks'),
    State('modal-novo-receita', 'is_open')
)
def toggle_modal(num_clicks, is_open):
    if num_clicks:
        return not is_open

# Pop-up despesa
@app.callback(
    Output('modal-novo-despesa', 'is_open'),
    Input('open-novo-despesa', 'n_clicks'),
    State('modal-novo-despesa', 'is_open')
)
def toggle_modal(num_clicks, is_open):
    if num_clicks:
        return not is_open

# Adicionar nova receita
@app.callback(
    Output('store-receitas', 'data'),
    Input('salvar_receita', 'n_clicks'),
    [
        State('txt-receita', 'value'),
        State('valor-receita', 'value'),
        State('date-receitas', 'date'),
        State('switches-input-receita', 'value'),
        State('select_receita', 'value'),
        State('store-receitas', 'data')
    ]
)
def salve_form_receita(n, descricao, valor, date, switches, categoria, dict_receitas):
    df_receitas = pd.DataFrame(dict_receitas)
    
    if (n != None) and (valor != "") and (valor != None): # Pular primeira execução do callback quando o programa inicia
         # DEBUG
        #import pdb
        #pdb.set_trace()
        # =======

        valor = round(float(valor), 2)
        date = pd.to_datetime(date).date()
        # Duas linhas iguais para tratar casos de lista dentro da lista
        categoria = categoria[0] if type(categoria) == list else categoria
        categoria = categoria[0] if type(categoria) == list else categoria
        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        df_receitas.loc[df_receitas.shape[0]] = [valor, recebido, fixo, date, categoria, descricao]
        df_receitas.to_csv('df_receitas.csv')

    data_return = df_receitas.to_dict()
    
    return data_return

# Adicionar nova despesa
@app.callback(
    Output('store-despesas', 'data'),
    Input('salvar_despesa', 'n_clicks'),
    [
        State('txt-despesa', 'value'),
        State('valor-despesa', 'value'),
        State('date-despesa', 'date'),
        State('switches-input-despesa', 'value'),
        State('select_despesa', 'value'),
        State('store-despesas', 'data')
    ]
)
def salve_form_despesa(n, descricao, valor, date, switches, categoria, dict_despesas):
    df_despesas = pd.DataFrame(dict_despesas)
    
    if (n != None) and (valor != "") and (valor != None): # Pular primeira execução do callback quando o programa inicia
         # DEBUG
        #import pdb
        #pdb.set_trace()
        # =======

        valor = round(float(valor), 2)
        date = pd.to_datetime(date).date()
        # Duas linhas iguais para tratar casos de lista dentro da lista
        categoria = categoria[0] if type(categoria) == list else categoria
        categoria = categoria[0] if type(categoria) == list else categoria
        pago = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        df_despesas.loc[df_despesas.shape[0]] = [valor, pago, fixo, date, categoria, descricao]
        df_despesas.to_csv('df_despesas.csv')

    data_return = df_despesas.to_dict()
    
    return data_return

# Adicionar ou remover categoria de despesa
@app.callback(
    [
        Output('select_despesa', 'options'),
        Output('checklist-selected-style-despesa', 'options'),
        Output('checklist-selected-style-despesa', 'value'),
        Output('store-cat-despesas', 'data')
    ],
    [
        Input('add-category-despesa', 'n_clicks'),
        Input('remove-category-despesa', 'n_clicks')
    ],
    [
        State('input-add-despesa', 'value'),
        State('checklist-selected-style-despesa', 'value'),
        State('store-cat-despesas', 'data')
    ]
)
def add_remove_category_despesa(n, n2, txt, check_delete, data):
    cat_despesa = list(data['Categoria'].values())

    if n and (txt != "") and (txt != None):
        cat_despesa = cat_despesa + [txt] if txt not in cat_despesa else cat_despesa

    if n2:
        if len(check_delete) > 0:
            cat_despesa = [i for i in cat_despesa if i not in check_delete]

    opt_despesa = [{'label': i, 'value': i} for i in cat_despesa]
    df_cat_despesa = pd.DataFrame(cat_despesa, columns=['Categoria'])
    df_cat_despesa.to_csv('df_cat_despesas.csv')
    data_return = df_cat_despesa.to_dict()

    return [opt_despesa, opt_despesa, [], data_return]

# Adicionar ou remover categoria de receita
@app.callback(
    [
        Output('select_receita', 'options'),
        Output('checklist-selected-style-receita', 'options'),
        Output('checklist-selected-style-receita', 'value'),
        Output('store-cat-receitas', 'data')
    ],
    [
        Input('add-category-receita', 'n_clicks'),
        Input('remove-category-receita', 'n_clicks')
    ],
    [
        State('input-add-receita', 'value'),
        State('checklist-selected-style-receita', 'value'),
        State('store-cat-receitas', 'data')
    ]
)
def add_remove_category_receita(n, n2, txt, check_delete, data):
    cat_receita = list(data['Categoria'].values())

    if n and (txt != "") and (txt != None):
        cat_receita = cat_receita + [txt] if txt not in cat_receita else cat_receita

    if n2:
        if len(check_delete) > 0:
            cat_receita = [i for i in cat_receita if i not in check_delete]

    opt_receita = [{'label': i, 'value': i} for i in cat_receita]
    df_cat_receita = pd.DataFrame(cat_receita, columns=['Categoria'])
    df_cat_receita.to_csv('df_cat_receitas.csv')
    data_return = df_cat_receita.to_dict()

    return [opt_receita, opt_receita, [], data_return]