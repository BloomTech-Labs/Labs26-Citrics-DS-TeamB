from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
import os

router = APIRouter()

DATA_FILEPATH1 = os.path.join(os.path.dirname(__file__), "..", "..","data", "100city_population_data_2018.csv")
DATA_FILEPATH2 = os.path.join(os.path.dirname(__file__), "..", "..","data", "9yr_city_pop_data.csv")

@router.get('/population/{city_id}')
async def pop_to_dict(city_id: int):
    """
    Pull demographic data for specific city, state, and year 

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
    
    rt_data_dict["total_pop"] = rt_data[0][4]
    rt_data_dict["male_pop"] = rt_data[0][5]
    rt_data_dict["female_pop"] = rt_data[0][6]
    rt_data_dict["age_under_20"] = rt_data[0][7]
    rt_data_dict["age_20-29"] = rt_data[0][8]
    rt_data_dict["age_30-39"] = rt_data[0][9]
    rt_data_dict["age_40-49"] = rt_data[0][10]
    rt_data_dict["age_50-59"] = rt_data[0][11]
    rt_data_dict["age_above_60"] = rt_data[0][12]
    
    rt_dict["data"] = rt_data_dict 
    rt_dict["viz"] = citypopviz(city=rt_data[0][1], state=rt_data[0][2])
    return rt_dict

def citypopviz(city, state,metric = 'total_pop'):
    """
    Visualize historical population metrics from 2010 to 2018 for one city 

    ### Query Parameters:

    - `metric`: 'total_pop', 'male_pop', 'female_pop', 'age_under_20',
    'age_20-29', 'age_30-39', 'age_40-49', 'age_50-59', or 'age_above_60';
    default='total_pop',case sensitive, total/male/female pop in thousands,
    age demographics in percentages

    - `city`: [city name], case sensitive(ex: Birmingham)

    - `state `: [state abbreviation], 2-letters; case sensitive (ex: AL) 

    ### Response
    JSON string to render with react-plotly.js
    """
    df = pd.read_csv(DATA_FILEPATH2, encoding='utf-8')
    subset = df[(df.city == city) & (df.state == state)]
    fig = px.line(subset, x='year', y=metric, title=f'{metric} in {city},{state}')
    return fig.to_json()