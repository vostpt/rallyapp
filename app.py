# -*- coding: utf-8 -*-

# Import libraries 

import pandas as pd 
import io
import requests
import plotly.express as px 

# Import csv file from URL 

url="https://bot-api.vost.pt/rally-pt/rallyptdata.csv"
s=requests.get(url).content

# Convert csv file to two dataframes: one for the map, another for the table

df_map=pd.read_csv(io.StringIO(s.decode('utf-8')))
df=pd.read_csv(io.StringIO(s.decode('utf-8')))

# Plot mapbox map with dataframe variables

fig = px.scatter_mapbox(df_map, lat="lat", lon="lon", color="capacity", #size="capacity",
                            labels=dict(color="Lotação/Capacidad/Capacity"),
                            color_continuous_scale=["#61c462","yellow","#f89406","#ee5f5a"],
                            center=dict(lon=-7.441015, lat=40.777132),
                            zoom=7,
                            size_max=10, hover_name='label',
                            hover_data={
                                    'lat':False, 
                                 'lon':False,
                                 'capacity':False,

                                }        
                            )
fig.update_layout(
            hoverlabel=dict(
            bgcolor="#272b30",
            font_size=16,
            font_family="Open Sans")
        )

fig.update_coloraxes(cmin=0,cmax=100)
fig.update_layout(mapbox_style="carto-darkmatter")


# Table generation starts here 
# Import libraries to generate table

import dash_table

# Generate dataframe for table with only the relevant columns

df_table=df.filter(['name','stage','capacity'])

# Conditional formatting 

df_table['opstatus'] = df['capacity'].apply(lambda x:
    '🔴' if x > 89 else (
    '🟠' if x > 69 else (
    '🟡' if x > 49 else (
    '🟢' if x > 9 else ''
))))

# Create a column named "id" based on the index of the dataframe

df_table['id'] = df_table.index 

# Create Table and assign it an id for app callback 

newtable = dash_table.DataTable(
    id='table',
    data=df_table.to_dict('records'),
    columns=[
            {'name':'Zona Espectáculo', 'id':'name'},
            {'name':'Troço', 'id':'stage'},
            {'name':'Status', 'id':'opstatus'},        
    ],
    # Define table styling 
    fixed_rows={'headers': True},
    style_table={'height': 400},  

    # Condition resizing of columns 
    style_cell_conditional=[
        {'if': {'column_id': 'name'},
         'width': '10%'},
         {'if': {'column_id': 'opstatus'},
         'width': '15%'},
        {'if': {'column_id': 'stage'},
         'width': '10%'},
    ],
    # Define overall styling for the table
    style_as_list_view=True,
     style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white',
        'fontSize':16, 'font-family':'Open Sans',
    },
    )

# Card design starts here 

# Import libraries

import dash_bootstrap_components as dbc
import dash_html_components as html

card_info = [
        dbc.CardBody(
            [
                html.H4("Sobre este site", className="card-title"),
                html.P(
                    " Este site foi desenvolvido pela VOST Portugal em colaboração com o ACP. "
                    " As informações que aqui constam são disponibilizadas em tempo real em coordenação com a GNR",
                    className="card-text",
                ),
                html.P(
                    "Este sitio web fue desarrollado por VOST Portugal en colaboración con ACP. "
                    " La información aquí contenida está disponible en tiempo real en coordinación con la GNR.",
                    className="card-text",
                ),
                html.P(
                    "This website was developed by VOST Portugal in collaboration with ACP. "
                    "The information contained here is made available in real time in coordination with the GNR",
                    className="card-text",
                ),
            ]
        ),
    ]

card_legend = [
        dbc.CardBody(
            [
                html.H4("INFO", className="card-title"),
                html.P(
                    "🇵🇹 | 🔴 Lotação Esgotada | 🟠 Lotação acima dos 80% | 🟡 Lotação acima dos 50% | 🟢 Livre",
                    className="card-text",
                ),
                html.P(
                    "🇪🇸 | 🔴 Sin Capacidad | 🟠 Capacidad superior al 80% | 🟡 Capacidad Superior al 50% | 🟢 Libre",
                    
                    className="card-text",
                ),
                html.P(
                    "🇬🇧 🔴 Full Capacity | 🟠 Capaciy above  80% | 🟡 Capacity above 50% | 🟢 Free",
                    className="card-text",
                ),
            ]
        ),
    ]
    

# App starts here 

# Import Libraries

import dash
import dash_core_components as dcc


from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template


# Get template for layout. This saves time. 

load_figure_template("slate")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE],title='Rally de Portugal Vodafone 2021',update_title=None,
                meta_tags=[{'name': 'viewport',
                           'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
        )

server = app.server

# Google Analytics 

app.index_string = """<!DOCTYPE html>
<html>
    <head>

        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-E2EZVCEJDS"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-E2EZVCEJDS');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

# Design top Navbar 

VOSTPT_LOGO =  "https://dash.vost.pt/wp-content/uploads/2020/11/cropped-VOSTPT_LOGO_PNG_TRANSP.png"

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=VOSTPT_LOGO, height="15px")),
                    dbc.Col(dbc.NavbarBrand("RALLY DE PORTUGAL VODAFONE 2021", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://vost.pt",
        ),
    ],
    color="dark",
    dark=True,
)

# Design layout 

app.layout = dbc.Container(
    [
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        ),
    navbar,
    html.Hr(),
    dbc.Row(
        [
        dbc.Col(dcc.Graph(id='graph',figure=fig,animate=True, className="h-100"),lg=6),
        dbc.Col(id='table',lg=6),
        ], 
    ),
    dbc.Row(
        [
        dbc.Col(html.Div(dbc.Card(card_legend, color="primary", inverse=True)),width=12),
        dbc.Col(html.Div(dbc.Card(card_info, color="primary", inverse=True)),width=12),
               
        ],
    ),


    ],

    fluid=True,
)



@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', "n_intervals")]
)

def streamFig(value):
    
    global df
    # Import csv file from URL 

    url="https://bot-api.vost.pt/rally-pt/rallyptdata.csv"
    s=requests.get(url).content
    df1 = pd.read_csv(io.StringIO(s.decode('utf-8')))
    fig = px.scatter_mapbox(df1, lat="lat", lon="lon", color="capacity", #size="capacity",
                            labels=dict(color="Lotação/Capacidad/Capacity"),
                            color_continuous_scale=["#61c462","yellow","#f89406","#ee5f5a"],
                            center=dict(lon=-7.441015, lat=40.777132),
                            zoom=7,
                            size_max=10, hover_name='label',
                            hover_data={
                                    'lat':False, 
                                 'lon':False,
                                 'capacity':False,

                                }        
                            )
    fig.update_layout(
            hoverlabel=dict(
            bgcolor="#272b30",
            font_size=16,
            font_family="Open Sans")
        )

    fig.update_coloraxes(cmin=0,cmax=100)
    fig.update_layout(mapbox_style="carto-darkmatter")

    return(fig)

@app.callback(
    Output('table', 'children'),
    [Input('interval-component', "n_intervals")]
)

def streamTable(value):
    
    global table
    # Assing CSV to dataframe df 
    url="https://bot-api.vost.pt/rally-pt/rallyptdata.csv"
    s=requests.get(url).content

    df_up=pd.read_csv(io.StringIO(s.decode('utf-8')))

    # Generate dataframe for table 

    df_table_up=df_up.filter(['name','stage','capacity'])

    df_table_up['opstatus'] = df_up['capacity'].apply(lambda x:
    '🔴' if x > 90 else (
    '🟠' if x > 70 else (
    '🟡' if x > 50 else (
    '🟢' if x > 9 else ''
    ))))

    df_table_up['id'] = df_table_up.index 


    newtable_up = dash_table.DataTable(
        
        data=df_table_up.to_dict('records'),
        columns=[
                {'name':'Zona Espectáculo', 'id':'name'},
                {'name':'Troço', 'id':'stage'},
                #{'name':'Lotação', 'id':'capacity','type':'numeric'},
                {'name':'Status', 'id':'opstatus'},

        ],
        fixed_rows={'headers': True},
        style_table={'height': 500},  

        style_cell_conditional=[
            {'if': {'column_id': 'name'},
             'width': '10%'},
             {'if': {'column_id': 'opstatus'},
             'width': '15%'},
            {'if': {'column_id': 'stage'},
             'width': '10%'},
        ],

        style_as_list_view=True,
         style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white',
            'fontSize':16, 'font-family':'Open Sans',
        },
        )

    return newtable_up

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=False)

