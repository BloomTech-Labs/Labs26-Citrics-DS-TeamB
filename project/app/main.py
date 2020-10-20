from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import  cities, jobs, current_city_metrics, predict, viz, rental_pred_viz, pop_predict

app = FastAPI(
    title='CITRICS-TEAM-B DS API',
    description='Citrics, city comparison app',
    version='0.1',
    docs_url='/',
)

app.include_router(predict.router)
# app.include_router(viz.router)
app.include_router(cities.router)
app.include_router(jobs.router)
app.include_router(current_city_metrics.router)
app.include_router(rental_pred_viz.router)
app.include_router(pop_predict.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
