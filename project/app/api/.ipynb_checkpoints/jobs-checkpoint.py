from fastapi import APIRouter, HTTPException
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

router = APIRouter()

DATA_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "..","data", "job_industry_data.csv")

@router.get('/jobs/{city_id}')
async def pop_to_dict(city_id: int):
    """
    Job Industry insights 
    """
    rt_dict = {}
    rt_data_dict = {}
    
    df = pd.read_csv(DATA_FILEPATH, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    rt_data = dataframe.to_numpy()
    
    rt_data_dict['id'] = rt_data[0][1]
    rt_data_dict['city'] = rt_data[0][2]
    rt_data_dict['state'] = rt_data[0][3]
    rt_data_dict['city_state'] = rt_data[0][4]


    rt_data_dict["job_ranked_1"] = top_jobs(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[0]
    rt_data_dict["job_ranked_1_%"] = percentage(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[0]

    rt_data_dict["job_ranked_2"] = top_jobs(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[1]
    rt_data_dict["job_ranked_2_%"] = percentage(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[1]

    rt_data_dict["job_ranked_3"] = top_jobs(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[2]
    rt_data_dict["job_ranked_3_%"] = percentage(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[2]

    rt_data_dict["job_ranked_4"] = top_jobs(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[3]
    rt_data_dict["job_ranked_4_%"] = percentage(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[3]

    rt_data_dict["job_ranked_5"] = top_jobs(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[4]
    rt_data_dict["job_ranked_5_%"] = percentage(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[4]

    rt_data_dict["job_ranked_6"] = top_jobs(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[5]
    rt_data_dict["job_ranked_6_%"] = percentage(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[5]

    rt_data_dict["job_ranked_7"] = top_jobs(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[6]
    rt_data_dict["job_ranked_7_%"] = percentage(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[6]

    rt_data_dict["job_ranked_8"] = top_jobs(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[7]
    rt_data_dict["job_ranked_8_%"] = percentage(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[7]

    rt_data_dict["job_ranked_9"] = top_jobs(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[8]
    rt_data_dict["job_ranked_9_%"] = percentage(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[8]

    rt_data_dict["job_ranked_10"] = top_jobs(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[9]
    rt_data_dict["job_ranked_10_%"] = percentage(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10).iloc[9]

    rt_dict["data"] = rt_data_dict 
     
    rt_dict["viz"] = cityjobsviz(df = pd.read_csv(DATA_FILEPATH, encoding='utf-8'), city_id=rt_data[0][1], n_industries=10)
    
    return rt_dict

def cityjobsviz(df, city_id , n_industries = 10):

  df = pd.read_csv(DATA_FILEPATH, encoding='utf-8')
  df_city_top10 = df[ df["city_id"] == city_id].sort_values(by="Job Sector Percentage", ascending=False)[1:n_industries + 1]
  df_city_other = df[ df["city_id"] == city_id].sort_values(by="Job Sector Percentage", ascending=False)[n_industries + 1:]


  top_10_labels = df_city_top10["Job Sector"]
  top_10_values = df_city_top10["Job Sector Percentage"]

  df_top10_aggregate = pd.DataFrame({"Job Sector": top_10_labels,
                                     "Job Sector Percentage": top_10_values})
  
  df_city_other = pd.DataFrame({"Job Sector": ["Other"],
                                "Job Sector Percentage": [100 - sum(top_10_values)]})

  df_combined = pd.concat([df_top10_aggregate, df_city_other])

  fig = go.Figure(data=[go.Pie(labels=df_combined["Job Sector"], values=df_combined["Job Sector Percentage"], textinfo="label+percent", hole=.3)])
  fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

  return fig.to_json()

def top_jobs(df, city_id, n_industries = 10):

  df = df
  df_city_top10 = df[ df["city_id"] == city_id].sort_values(by="Job Sector Percentage", ascending=False)[1:n_industries + 1]
  df_city_other = df[ df["city_id"] == city_id].sort_values(by="Job Sector Percentage", ascending=False)[n_industries + 1:]


  top_10_labels = df_city_top10["Job Sector"]
  top_10_values = df_city_top10["Job Sector Percentage"]

  df_top10_aggregate = pd.DataFrame({"Job Sector": top_10_labels,
                                     "Job Sector Percentage": top_10_values})
  
  df_city_other = pd.DataFrame({"Job Sector": ["Other"],
                                "Job Sector Percentage": [100 - sum(top_10_values)]})

  df_combined = pd.concat([df_top10_aggregate, df_city_other])

  t = df_combined["all"] = df_combined["Job Sector"].astype(str)

  return t

def percentage(df, city_id, n_industries):

  df = df
  df_city_top10 = df[ df["city_id"] == city_id].sort_values(by="Job Sector Percentage", ascending=False)[1:n_industries + 1]
  df_city_other = df[ df["city_id"] == city_id].sort_values(by="Job Sector Percentage", ascending=False)[n_industries + 1:]


  top_10_labels = df_city_top10["Job Sector"]
  top_10_values = df_city_top10["Job Sector Percentage"]

  df_top10_aggregate = pd.DataFrame({"Job Sector": top_10_labels,
                                     "Job Sector Percentage": top_10_values})
  
  df_city_other = pd.DataFrame({"Job Sector": ["Other"],
                                "Job Sector Percentage": [100 - sum(top_10_values)]})

  df_combined = pd.concat([df_top10_aggregate, df_city_other])
  p = df_combined["all"] = (df_combined["Job Sector Percentage"].round(2)).astype(str) + "%"

  return p