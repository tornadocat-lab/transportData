from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import query

app = FastAPI()

# CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stations")
def get_stations():
    return query.get_stations()

@app.get("/trains")
def get_trains(
    from_station: str = Query(..., alias="from"), 
    to_station: str = Query(..., alias="to"),
    date: str = Query(...)
    ):
    return query.get_trains_between(from_station, to_station, date)