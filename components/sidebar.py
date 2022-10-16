from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
from dash.dash_table.Format import Group
import dash_bootstrap_components as dbc

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd

from app import app

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
                                  options=[],
                                  value=[],
                                  switch=True)
                ], width=4),
                dbc.Col([
                    html.Label("Categoria da receita"),
                    dbc.Select(id='select_receita',
                               options=[],
                               value=[])
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
                                              options=[],
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
                                  options=[],
                                  value=[],
                                  switch=True)
                ], width=4),
                dbc.Col([
                    html.Label("Categoria da despesa"),
                    dbc.Select(id='select_despesa',
                               options=[],
                               value=[])
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
                                              options=[],
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