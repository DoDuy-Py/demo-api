import schedule
import time
import requests

import random

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import models
from core.settings import SessionLocal, engine, get_db


from constants.global_constants import BASE_API

session = Session(engine)

def add_water_quality(data):
    try:
        print(f'do function name {add_water_quality.__name__}')
        url = f"{BASE_API}/api/v1/create-water/"
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print("Create water successful!")
            print("Response data:", response.json())
        else:
            print(f"Failed to create water. Status code: {response.status_code}")
            print("Response data:", response.json())
    except Exception as e:
        print(e)

def update_water_quality(pk):
    try:
        print(f'do function name {update_water_quality.__name__}')
        instance = session.execute(select(models.WaterQuality).filter_by(id=pk)).scalar_one()

        instance.turbidity += 1

        session.commit()
        session.close()
    except Exception as e:
        print(e)

# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)
# schedule.every().minute.at(":17").do(job)

def job():
    locations = ["aaaa", "bbbbb", "cccccc", "dddddd"]
    data = {
        'location': locations[random.randint(0, 3)],
        'ph_level': random.randint(0, 14),  # Phân bố ngẫu nhiên giá trị pH
        'temperature': random.randint(0, 100),  # Nhiệt độ ngẫu nhiên
        'turbidity': random.randint(0, 100)  # Độ đục ngẫu nhiên
    }
    # add_water_quality(data)
    update_water_quality(1)

def init_schedule():
    return
    schedule.every(1).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)