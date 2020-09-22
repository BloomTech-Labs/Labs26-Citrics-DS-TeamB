from fastapi import APIRouter, HTTPException
import pandas as pd
import os

router = APIRouter()

rental_data = os.path.join(os.path.dirname(__file__), "..", "..", "data", "rental_data_2020.csv")

@router.get('/rental/{city_id}')
async def get_rental_data(city_id: int):
    """
    Returns 
            id,
            city,
            county_name,
            area_name,
            state, 
            city_state, 
            studio - rental rate in dollars for studio apartment,
            1br - rental rate in dollars for one bedroom apartment,
            2br - rental rate in dollars for two bedroom apartment,
            3br - rental rate in dollars for three bedroom apartment,
            4br - rental rate in dollars for four bedroom apartment,
            rental_pct_chg - rental change in percentage compared to last year
            rental_dollar_chg - rental change in dollars compared to last year
            
    of a city.
    
    ### Query Parameters: 
    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK)
    ### Response
    Dictionary object 
    """

    rt_dict = {}
    rt_data_dict = {}

    df = pd.read_csv(rental_data, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    rt_data = dataframe.to_numpy()

    rt_data_dict['id'] = rt_data[0][0]
    
    rt_data_dict['city'] = rt_data[0][1]
    rt_data_dict['county_name'] = rt_data[0][10]
    rt_data_dict['area_name'] = rt_data[0][9]
    rt_data_dict['state'] = rt_data[0][2]
    rt_data_dict['city_state'] = rt_data[0][3]
     
    rt_data_dict['studio'] = rt_data[0][4]
    rt_data_dict['1br'] = rt_data[0][5]
    rt_data_dict['2br'] = rt_data[0][6]
    rt_data_dict['3br'] = rt_data[0][7]
    rt_data_dict['4br'] = rt_data[0][8]
    
    rt_data_dict['rental_pct_chg'] = rt_data[0][11]
    rt_data_dict['rental_dollar_chg'] = rt_data[0][12]

    rt_dict['data'] = rt_data_dict
    return rt_dict