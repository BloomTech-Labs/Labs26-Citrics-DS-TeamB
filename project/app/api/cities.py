import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
from pydantic import BaseModel, Field, validator
import os

router = APIRouter()
class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

   # x1: float = Field(..., example=3.14)
   # x2: int = Field(..., example=-42)
   # x3: str = Field(..., example='banjo')
        
    rooms : Optional[str] = None,
    pop_min : Optional[int] = None,
    pop_max : Optional[int] = None,
    rent_min : Optional[int] = None,
    rent_max : Optional[int] = None,
    weather_min : Optional[int] = None,
    weather_max : Optional[int] = None

@router.get('/cities')
async def cities(rooms : Optional[str] = None,
                pop_min : Optional[int] = None,
                pop_max : Optional[int] = None,
                rent_min : Optional[int] = None,
                rent_max : Optional[int] = None,
                weather_min : Optional[int] = None,
                weather_max : Optional[int] = None):
    """
    Returns list of id, cities name , their states and city_state in one string 
    """
   
    url =os.path.join(os.path.dirname(__file__), "..", "..", "data", "current_city_metrics.csv")
    df = pd.read_csv(url)
    condition=[]
    cond_str =""
    rooms_map={"studio":"fmr_0",
              "1br":"fmr_1",
              "2br":"fmr_2",
              "3br":"fmr_3",
              "4br":"fmr_4",
             }
    filter_df = df
    
    # Checking for rentals
    if(rooms):
        if(rent_min):
            cond_rent = f"({rooms_map[rooms]} >= {rent_min})"
            condition.append(cond_rent)
        if(rent_max):
            cond_rent = f"({rooms_map[rooms]} <= {rent_max})"
            condition.append(cond_rent)
   # Checking for population
    if(pop_min):
        cond_pop = f"(total_pop >= {pop_min})"
        condition.append(cond_pop)
    if(pop_max):
        cond_pop = f"(total_pop <= {pop_max})"
        condition.append(cond_pop)
    
    # Checking for Weather
    if(weather_min):
        cond_weather = f"(winter_mintempF_mean >= {weather_min})"
        condition.append(cond_weather)
    if(weather_max):
        cond_weather = f"(summer_maxtempF_mean <= {weather_max})"
        condition.append(cond_weather)
    
    #construct the condition str
    #print(len(condition))
    
    if (len(condition) > 0 ):
        for cond in condition:
            cond_str += f"{cond} & "
    #print(cond_str[:])
    #print(cond_str[:-2])
        filter_df = df[df.eval(cond_str[:-2])]
    
    
    filter_df = filter_df[['city_id','city','state','city_state']]
    #print(filter_df.shape)
    df_list = filter_df.to_numpy()
    num_rows=len(df_list)
    
    list_dict = []
    for row in range(num_rows):
        #print(row)
        dic ={}
        dic["id"] = df_list[row][0]
        dic["name"]= df_list[row][1]
        dic["state"] = df_list[row][2]
        dic["city_state"] = df_list[row][3]
        list_dict.append(dic)
        
    return {'cities':list_dict}
    
