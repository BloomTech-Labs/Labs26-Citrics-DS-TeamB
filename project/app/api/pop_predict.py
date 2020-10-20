from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

router = APIRouter()

DATA_FILEPATH1 = os.path.join(os.path.dirname(__file__), "..", "..","data", "historical_pop_complete.csv")
DATA_FILEPATH2 = os.path.join(os.path.dirname(__file__), "..", "..","data", "total_pop_predict.csv")
DATA_FILEPATH3 = os.path.join(os.path.dirname(__file__), "..", "..","data", "pop_density_predict.csv")

@router.get('/predict_pop/{city_id}')
async def pop_tse(city_id: int):
    """
    Return time series estimates for total population over the next 5 years

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK)

    ### Response
    Dictionary object 
    """
    rt_dict = {}
    rt_data_dict = {}
    
    df = pd.read_csv(DATA_FILEPATH2, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    rt_data = dataframe.to_numpy()
    rt_data_dict["city_id"] = rt_data[0][0]
    rt_data_dict["city"] = rt_data[0][1]
    rt_data_dict["state"] = rt_data[0][2]
    rt_data_dict["city_state"] = rt_data[0][3]
    
    rt_dict["data"] = rt_data_dict
    rt_dict["viz"] = {"total_pop":tot_pop_tse_viz(city_id=rt_data[0][0]),
                      "pop_density":pop_dens_tse_viz(city_id=rt_data[0][0])}
    return rt_dict

def tot_pop_tse_viz(city_id: int):
    """
    Visualize future total population estimates for 2020-2024

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK) 

    ### Response
    JSON string to render with react-plotly.js
    """
    df = pd.read_csv(DATA_FILEPATH2, encoding='utf-8')
    df2 = pd.read_csv(DATA_FILEPATH1, encoding='utf-8')
    df = df.loc[df['city_id'] == city_id]
    df2 = df2.loc[df2['city_id'] == city_id]
    x = df['year'].tolist()
    y = df2['total_pop'].tolist()
    y_hat = df['yhat'].tolist()
    y_upper = df['yhat_upper'].tolist()
    y_lower = df['yhat_lower'].tolist()

    fig = go.Figure([
        go.Scatter(
            x=x,
            y=y,
            line=dict(color='rgb(0,151,223)'),
            mode='lines',
            showlegend=False
        ),
        go.Scatter(
            x=x,
            y=y_hat,
            line=dict(color='rgb(0,151,223)'),
            mode='lines',
            showlegend=False
        ),
        go.Scatter(
            x=x+x[::-1], # x, then x reversed
            y=y_upper+y_lower[::-1], # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,151,223,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        )
    ])
    return fig.to_json()

def pop_dens_tse_viz(city_id: int):
    """
    Visualize future population density estimates for 2020-2024

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK) 

    ### Response
    JSON string to render with react-plotly.js
    """
    df = pd.read_csv(DATA_FILEPATH3, encoding='utf-8')
    df2 = pd.read_csv(DATA_FILEPATH1, encoding='utf-8')
    df = df.loc[df['city_id'] == city_id]
    df2 = df2.loc[df2['city_id'] == city_id]
    x = df['year'].tolist()
    y = df2['pop_density'].tolist()
    y_hat = df['yhat'].tolist()
    y_upper = df['yhat_upper'].tolist()
    y_lower = df['yhat_lower'].tolist()

    fig = go.Figure([
        go.Scatter(
            x=x,
            y=y,
            line=dict(color='rgb(255,8,0)'),
            mode='lines',
            showlegend=False
        ),
        go.Scatter(
            x=x,
            y=y_hat,
            line=dict(color='rgb(255,8,0)'),
            mode='lines',
            showlegend=False
        ),
        go.Scatter(
            x=x+x[::-1], # x, then x reversed
            y=y_upper+y_lower[::-1], # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(255,8,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        )
    ])
    return fig.to_json()
