from dataiku.customwebapp import *

# Access the parameters that end-users filled in using webapp config
# For example, for a parameter called "input_dataset"
# input_dataset = get_webapp_config()["input_dataset"]

import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

app.config.external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

client = dataiku.api_client()
project = client.get_default_project()
v = project.get_variables()

app.layout = html.Div(children=[
    html.H2(children='Update Project Variables'),
    
    html.H3(children='Global Project Variables'),
    html.Plaintext(json.dumps(v["standard"], sort_keys=True, indent=4), id="std-txt"),
    html.Div(children=[
        dcc.Dropdown(list(v["standard"].keys()),
                     id='std-dropdown'),
        dcc.Input(
            id="std-input-text",
            type="text",
            placeholder="input type {}".format("text"),
        ),
        html.Button('Update', id='std-update-button', n_clicks=0),
        html.Div(id='std-update-conf'),
        
    ],className='rows'),
    
    
    html.H3(children='Local Project Variables'),
    html.Plaintext(json.dumps(v["local"], sort_keys=True, indent=4), id="local-txt"),
    html.Div(children=[
        dcc.Dropdown(list(v["local"].keys()),
                     id='local-dropdown'),
        dcc.Input(
            id="local-input-text",
            type="text",
            placeholder="input type {}".format("text"),
        ),
        html.Button('Update', id='local-update-button', n_clicks=0),
        html.Div(id='local-update-conf'),
        
    ],className='rows'),
])

@app.callback(
    Output('std-update-conf', 'children'),
    Output('std-txt', 'children'),
    Input('std-update-button', 'n_clicks'),
    State('std-dropdown', 'value'),
    State('std-input-text', 'value')
)
def std_update(btn, variable, value_update):
    global v
    v = project.get_variables()
    original_val = v['standard'][variable]
    v['standard'][variable] = value_update
    project.set_variables(v)
    
    update_info = 'Global project variable {} updated from {} to {}'.format(
        variable,
        original_val,
        value_update
    )
    new_std = json.dumps(v["standard"], sort_keys=True, indent=4)
    
    return update_info , new_std  


@app.callback(
    Output('local-update-conf', 'children'),
    Output('local-txt', 'children'),
    Input('local-update-button', 'n_clicks'),
    State('local-dropdown', 'value'),
    State('local-input-text', 'value')
)
def local_update(btn, variable, value_update):
    print ("in update_info")
    global v
    v = project.get_variables()
    original_val = v['local'][variable]
    v['local'][variable] = value_update
    project.set_variables(v)
    
    update_info = 'Local project variable {} updated from {} to {}'.format(
        variable,
        original_val,
        value_update
    )
    new_local = json.dumps(v["local"], sort_keys=True, indent=4)
    print (update_info)
    return update_info , new_local
