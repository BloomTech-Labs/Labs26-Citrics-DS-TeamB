from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
import plotly.express as px
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import os

router = APIRouter()

DATA_FILEPATH1 = os.path.join(os.path.dirname(__file__), "..", "..","data", "historical_pop_complete.csv")

@router.post('/pop_predict/{city_id}')
async def pop_tse(city_id: int, metric: str):
    """
    Return time series estimates for total population over the next 5 years

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK)

    - `metric`: 'total_pop', 'land_area', 'pop_density', 'male_pop', 'female_pop',
    'age_under_20', 'age_20-29', 'age_30-39', 'age_40-49', 'age_50-59', or 'age_above_60';
    case sensitive, total/male/female pop in thousands, land area
    in sq mi, pop_density in person/sqmi, age demographics in percentages

    ### Response
    Dictionary object 
    """
    rt_dict = {}
    df = pd.read_csv(DATA_FILEPATH1, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    dataframe = dataframe[['year', metric]]
    dataframe.columns = ['ds', 'y']
    dataframe['ds'] = pd.to_datetime(dataframe['ds'], format='%Y')

    m = Prophet()
    m.fit(dataframe)
    future = m.make_future_dataframe(periods=5, freq= 'y')
    forecast = m.predict(future)
    data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    rt_data = data.to_json(orient='records', date_format='iso')
    rt_dict["predict_data"] = rt_data
    rt_dict["predict_viz"] = pop_tse_viz(city_id=city_id, metric=metric)
    return rt_dict
    
def pop_tse_viz(city_id: int, metric: str):
    """
    Visualize future population estimates for 2020-2024

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK) 

    ### Response
    JSON string to render with react-plotly.js
    """
    df = pd.read_csv(DATA_FILEPATH1, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    dataframe = dataframe[['year', metric]]
    dataframe.columns = ['ds', 'y']
    dataframe['ds'] = pd.to_datetime(dataframe['ds'], format='%Y')

    m = Prophet()
    m.fit(dataframe)
    future = m.make_future_dataframe(periods=5, freq= 'y')
    forecast = m.predict(future)
    fig = plot_plotly(m, forecast)
    return fig.to_json()



