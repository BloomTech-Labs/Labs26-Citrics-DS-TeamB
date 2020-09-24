from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
import os

router = APIRouter()

DATA_FILEPATH1 = os.path.join(os.path.dirname(__file__), "..", "..","data", "2018_city_unemployment.csv")
DATA_FILEPATH2 = os.path.join(os.path.dirname(__file__), "..", "..","data", "6yr_city_unemployment_data.csv")

@router.get('/unemployment/{city_id}')
async def unemployment_to_dict(city_id: int):
    """
    Pull unemployment data for specific city_id 

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK)

    ### Response
    Dictionary object 
    """
    rt_dict = {}
    rt_data_dict = {}
    
    df = pd.read_csv(DATA_FILEPATH1, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    rt_data = dataframe.to_numpy()
    
    rt_data_dict["unemployment_rate"] = rt_data[0][4]
    rt_data_dict["rank"] = rt_data[0][5]
    rt_data_dict["city_state"] = rt_data[0][6]

    
    rt_dict["data"] = rt_data_dict 
    rt_dict["viz"] = unemploymentviz(city=rt_data[0][1], state=rt_data[0][2])
    return rt_dict

def unemploymentviz(city, state, metric = 'unemployment_rate'):
    """
    Visualize historical population metrics from 2010 to 2018 for one city 

    ### Query Parameters:

    - `metric`: 'unemployment_rank', 'rank'; default='unemployment_rate',case sensitive, 
    unemployment_rate in percentage (ex: Spokane - 5.5% of city population unemployed), 
    rank in how the city compares to other metropolitan areas (ex: lower the better, higher means
    more unemployment)

    - `city`: [city name], case sensitive(ex: Birmingham)

    - `state `: [state abbreviation], 2-letters; case sensitive (ex: AL) 

    ### Response
    JSON string to render with react-plotly.js
    """
    df = pd.read_csv(DATA_FILEPATH2, encoding='utf-8')
    subset = df[(df.city == city) & (df.state == state)]
    fig = px.area(subset, x='year', y=metric, title=f'{metric} in {city},{state}')
    return fig.to_json()