from fastapi import APIRouter, HTTPException
import pandas as pd
import os

router = APIRouter()

weather_data = os.path.join(os.path.dirname(__file__), "..", "..", "data", "weather_average.csv")

@router.get('/weather/{city_id}')
async def weather(city_id: int):
    """
    Returns average humidity, maximum and minimum temperature of summer and winter season of a city.
    
    ### Query Parameters: 
    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK)
    ### Response
    Dictionary object 
    """

    rt_dict = {}
    rt_data_dict = {}

    df = pd.read_csv(weather_data, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    rt_data = dataframe.to_numpy()

    rt_data_dict['id'] = rt_data[0][0]
    rt_data_dict['city'] = rt_data[0][1]
    rt_data_dict['state'] = rt_data[0][2]
    rt_data_dict['city_state'] = rt_data[0][3]

    rt_data_dict['summer_maxtempF_mean'] = rt_data[0][4]
    rt_data_dict['winter_mintempF_mean'] = rt_data[0][8]
    rt_data_dict['summer_humidity_mean'] = rt_data[0][6]
    rt_data_dict['total_days_snowed'] = rt_data[0][10]
    rt_data_dict['total_days_rained'] = rt_data[0][11]



    rt_dict['data'] = rt_data_dict
    return rt_dict