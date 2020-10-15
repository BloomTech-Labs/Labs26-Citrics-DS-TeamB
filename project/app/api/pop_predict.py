from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
import plotly.express as px
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import os

router = APIRouter()

DATA_FILEPATH1 = os.path.join(os.path.dirname(__file__), "..", "..","data", "historical_pop_complete.csv")

@router.post('/pop_predict')
async def pop_tse(city_id: int):
    """
    Return time series estimates for total population over the next 5 years

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK)

    ### Response
    Dictionary object 
    """
    rt_dict = {}
    df = pd.read_csv(DATA_FILEPATH1, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    dataframe = dataframe[['year', 'total_pop']]
    dataframe.columns = ['ds', 'y']
    dataframe['ds'] = pd.to_datetime(dataframe['ds'], format='%Y')

    m = Prophet()
    m.fit(dataframe)
    future = m.make_future_dataframe(periods=5, freq= 'y')
    forecast = m.predict(future)
    data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    rt_data = data.to_json(orient='records', date_format='iso')
    rt_dict["data"] = {"total_pop":rt_data,
                       "pop_density":pop_dens_tse(city_id=city_id)}
    rt_dict["viz"] = {"total_pop":tot_pop_tse_viz(city_id=city_id),
                      "pop_density":pop_dens_tse_viz(city_id=city_id)}
    return rt_dict

def pop_dens_tse(city_id: int):
    """
    Return time series estimates for population density over the next 5 years

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK)

    ### Response
    Dictionary object 
    """
    df = pd.read_csv(DATA_FILEPATH1, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    dataframe = dataframe[['year', 'pop_density']]
    dataframe.columns = ['ds', 'y']
    dataframe['ds'] = pd.to_datetime(dataframe['ds'], format='%Y')

    m = Prophet()
    m.fit(dataframe)
    future = m.make_future_dataframe(periods=5, freq= 'y')
    forecast = m.predict(future)
    data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    rt_data = data.to_json(orient='records', date_format='iso')
    return rt_data
    
def tot_pop_tse_viz(city_id: int):
    """
    Visualize future total population estimates for 2020-2024

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK) 

    ### Response
    JSON string to render with react-plotly.js
    """
    df = pd.read_csv(DATA_FILEPATH1, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    dataframe = dataframe[['year', 'total_pop']]
    dataframe.columns = ['ds', 'y']
    dataframe['ds'] = pd.to_datetime(dataframe['ds'], format='%Y')

    m = Prophet()
    m.fit(dataframe)
    future = m.make_future_dataframe(periods=5, freq= 'y')
    forecast = m.predict(future)
    fig = plot_plotly(m, forecast)
    return fig.to_json()

def pop_dens_tse_viz(city_id: int):
    """
    Visualize future population density estimates for 2020-2024

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK) 

    ### Response
    JSON string to render with react-plotly.js
    """
    df = pd.read_csv(DATA_FILEPATH1, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    dataframe = dataframe[['year', 'pop_density']]
    dataframe.columns = ['ds', 'y']
    dataframe['ds'] = pd.to_datetime(dataframe['ds'], format='%Y')

    m = Prophet()
    m.fit(dataframe)
    future = m.make_future_dataframe(periods=5, freq= 'y')
    forecast = m.predict(future)
    fig = plot_plotly(m, forecast)
    return fig.to_json()




