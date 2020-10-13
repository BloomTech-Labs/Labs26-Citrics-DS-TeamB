from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
import os

router = APIRouter()

city_metrics_filepath = os.path.join(os.path.dirname(__file__), "..", "..","data", "current_city_metrics.csv")
historical_pop_filepath = os.path.join(os.path.dirname(__file__), "..", "..","data", "historical_pop_data_final.csv")
historical_unemp_filepath = os.path.join(os.path.dirname(__file__), "..", "..","data", "6yr_city_unemployment_data.csv")

@router.get('/city_metrics/{city_id}')
async def metrics_to_dict(city_id: int):
    """
    Pull current city metric data for specific city

    ### Query Parameters: 

    - `city_id`: [city_id], unique numeric mapping (ex: 0 returns Anchorage, AK)

    ### Response
    Dictionary object 
    """
    rt_dict = {}
    rt_data_city_dict = {}
    rt_data_pop_dict = {}
    rt_data_rental_dict = {}
    rt_data_weather_dict ={}
    rt_data_unemp_dict = {}
    
    df = pd.read_csv(city_metrics_filepath, encoding='utf-8')
    dataframe = df[df['city_id']==city_id]
    rt_data = dataframe.to_numpy()

    rt_data_city_dict["city_id"] = rt_data[0][0]
    rt_data_city_dict["city"] = rt_data[0][1]
    rt_data_city_dict["state"] = rt_data[0][2]
    rt_data_city_dict["city_state"] = rt_data[0][3]
    rt_data_city_dict["areaname"] = rt_data[0][4]
    rt_data_city_dict["countyname"] = rt_data[0][5]
    
    rt_data_pop_dict["total_pop"] = rt_data[0][6]
    rt_data_pop_dict["land_area"] = rt_data[0][7]
    rt_data_pop_dict["pop_density"] = rt_data[0][8]
    rt_data_pop_dict["male_pop"] = rt_data[0][9]
    rt_data_pop_dict["female_pop"] = rt_data[0][10]
    rt_data_pop_dict["age_under_20"] = rt_data[0][11]
    rt_data_pop_dict["age_20-29"] = rt_data[0][12]
    rt_data_pop_dict["age_30-39"] = rt_data[0][13]
    rt_data_pop_dict["age_40-49"] = rt_data[0][14]
    rt_data_pop_dict["age_50-59"] = rt_data[0][15]
    rt_data_pop_dict["age_above_60"] = rt_data[0][16]
    
    rt_data_unemp_dict["unemployment_rate"] = rt_data[0][17]
    rt_data_unemp_dict["rank"] = rt_data[0][18]
    
    rt_data_rental_dict["studio"] = rt_data[0][19]
    rt_data_rental_dict["1br"] = rt_data[0][20]
    rt_data_rental_dict["2br"] = rt_data[0][21]
    rt_data_rental_dict["3br"] = rt_data[0][22]
    rt_data_rental_dict["4br"] = rt_data[0][23]
    rt_data_rental_dict["rental_pct_chg"] = rt_data[0][24]
    rt_data_rental_dict["rental_dollar_chg"] = rt_data[0][25]
    
    rt_data_weather_dict["summer_maxtempF_mean"] = rt_data[0][26]
    rt_data_weather_dict["summer_mintempF_mean"] = rt_data[0][27]
    rt_data_weather_dict["summer_humidity_mean"] = rt_data[0][28]
    rt_data_weather_dict["winter_maxtempF_mean"] = rt_data[0][29]
    rt_data_weather_dict["winter_mintempF_mean"] = rt_data[0][30]
    rt_data_weather_dict["winter_humidity_mean"] = rt_data[0][31]
    rt_data_weather_dict["total_days_snowed"] = rt_data[0][32]
    rt_data_weather_dict["total_days_rained"] = rt_data[0][33]
    
    rt_dict["data"] = {"city":rt_data_city_dict,
                       "population":rt_data_pop_dict,
                       "unemployment":rt_data_unemp_dict,
                       "rental":rt_data_rental_dict,
                       "weather":rt_data_weather_dict}
    
    rt_dict["viz"] = {"population":citypopviz(city=rt_data[0][1], state=rt_data[0][2]),
                      "unemployment":unemploymentviz(city=rt_data[0][1], state=rt_data[0][2])}

    return rt_dict

def citypopviz(city, state,metric = 'total_pop'):
    """
    Visualize historical population metrics from 2010 to 2018 for one city 

    ### Query Parameters:

    - `metric`: 'total_pop', 'land_area', 'pop_density', 'male_pop', 'female_pop',
    'age_under_20', 'age_20-29', 'age_30-39', 'age_40-49', 'age_50-59', or 'age_above_60';
    default='total_pop',case sensitive, total/male/female pop in thousands, land area
    in sq mi, pop_density in person/sqmi, age demographics in percentages

    - `city`: [city name], case sensitive(ex: Birmingham)

    - `state `: [state abbreviation], 2-letters; case sensitive (ex: AL) 

    ### Response
    JSON string to render with react-plotly.js
    """
    df = pd.read_csv(historical_pop_filepath, encoding='utf-8')
    subset = df[(df.city == city) & (df.state == state)]
    fig = px.line(subset, x='year', y=metric, title=f'{metric} in {city},{state}')
    return fig.to_json()

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
    df = pd.read_csv(historical_unemp_filepath, encoding='utf-8')
    subset = df[(df.city == city) & (df.state == state)]
    fig = px.area(subset, x='year', y=metric, title=f'{metric} in {city},{state}')
    return fig.to_json()
