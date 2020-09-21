from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
import os

router = APIRouter()


@router.get('/cities')
async def cities():
    """
    Returns list of id, cities name , their states and city_state in one string 
    """
    
   # statecodes = [
   #        { 'id': 1, 'name': "Albany", 'state': "NY" },
   #        { 'id': 2, 'name': "Allegheny", 'state': "PA" },
   #        { 'id': 3, 'name': "Brooklyn", 'state': "NY" }
   # ]


    url =os.path.join(os.path.dirname(__file__), "..", "..", "data", "100city_state_data.csv")
    df = pd.read_csv(url)
    df_list = df.to_numpy()
    num_rows=len(df.to_numpy())
    
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
