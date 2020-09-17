from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px

router = APIRouter()


@router.get('/cities')
async def cities():
    """
    Returns list of cities and their states
    """
    
    statecodes = [
            { 'id': 1, 'name': "Albany", 'state': "NY" },
            { 'id': 2, 'name': "Allegheny", 'state': "PA" },
            { 'id': 3, 'name': "Brooklyn", 'state': "NY" },
            { 'id': 4, 'name': "Camden", 'state': "NJ" },
            { 'id': 5, 'name': "Canton", 'state': "OH" },
            { 'id': 6, 'name': "Dearborn", 'state': "MI" },
            { 'id': 7, 'name': "Duluth", 'state': "MN" },
            { 'id': 8, 'name': "Erie", 'state': "PA" },
            { 'id': 9, 'name': "Fall River", 'state': "MA" },
            { 'id': 10, 'name': "Flint", 'state': "MI" },
            { 'id': 11, 'name': "Gary", 'state': "IN" },
            { 'id': 12, 'name': "Hammond", 'state': "IN" },
            { 'id': 13, 'name': "Kenosha", 'state': "WI" },
            { 'id': 14, 'name': "Livonia", 'state': "MI" },
            { 'id': 15, 'name': "Lynn", 'state': "MA" },
            { 'id': 16, 'name': "New Bedford", 'state': "MA" },
            { 'id': 17, 'name': "Niagara Falls", 'state': "NY" },
            { 'id': 18, 'name': "Parma", 'state': "OH" },
            { 'id': 19, 'name': "Portsmouth", 'state': "VI" },
            { 'id': 20, 'name': "Reading", 'state': "PA" },
            { 'id': 21, 'name': "Roanoke", 'state': "VA" },
            { 'id': 22, 'name': "Scranton", 'state': "PA" },
            { 'id': 23, 'name': "Somerville", 'state': "MA" },
            { 'id': 24, 'name': "St. Joseph", 'state': "MO" },
            { 'id': 25, 'name': "Trenton", 'state': "NJ" },
            { 'id': 26, 'name': "Utica", 'state': "NY" },
            { 'id': 27, 'name': "Wilmington", 'state': "DW" },
            { 'id': 28, 'name': "Youngstown", 'state': "OH" },
            { 'id': 29, 'name': "Youngstown", 'state': "NY" },
            { 'id': 30, 'name': "Youngstown", 'state': "CA" }
]
    return {'cities':statecodes}
