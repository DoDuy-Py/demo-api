from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import models
from core.settings import SessionLocal, engine, get_db

import json


models.Base.metadata.create_all(bind=engine)

# router = APIRouter()

class WaterQualityView:

    # @staticmethod
    # @router.post("/create-water/")
    async def create(self, request: Request, db: Session = Depends(get_db)):
        try:
            data = await request.json()
            obj = models.WaterQuality(
                location = data.get("location"),
                ph_level = data.get("ph_level"),
                temperature = data.get("temperature"),
                turbidity = data.get("turbidity")
            )
            db.add(obj)
            db.commit()
            db.refresh(obj)
            response_content = json.dumps({
                'code': 200,
                'message': 'Done',
                'data': {
                    'id': obj.id,
                    'location': obj.location,
                    'ph_level': obj.ph_level,
                    'temperature': obj.temperature,
                    'turbidity': obj.turbidity
                }
            })
            return Response(content=response_content, media_type="application/json", status_code=200)
        except Exception as e:
            print(e)
            return {
                'code': 400,
                'message': 'Fail',
                'data': None
            }

    # @router.get("/get-water/")
    def get(self, request: Request, db: Session = Depends(get_db)):
        try:
            data_res = db.query(models.WaterQuality).all()
            return {
                'code': 400,
                'message': 'Lấy thông tin thành công',
                'data': data_res
            }
        except Exception as e:
            print(e)
            return {
                'code': 400,
                'message': 'Có lỗi xảy ra',
                'data': None
            }
        
    # @router.get("/detail-water/{id}")
    def detail(self, id: int, request: Request, db: Session = Depends(get_db)):
        try:
            instance = db.query(models.WaterQuality).get(id)
            return {
                'code': 400,
                'message': 'Lấy thông tin thành công',
                'data': instance
            } 
        except Exception as e:
            print(e)
            return {
                'code': 400,
                'message': 'Có lỗi xảy ra',
                'data': None
            }
    
    # @router.put("/update-water/{id}")
    async def update(self, id: int, request: Request, db: Session = Depends(get_db)):
        try:
            instance = db.query(models.WaterQuality).filter(models.WaterQuality.id == id).first()

            if instance is None:
                raise HTTPException(status_code=404, detail="Water quality not found")

            update_data = await request.json()

            for field, value in update_data.items():
                setattr(instance, field, value)

            db.commit()
            db.refresh(instance)
            return {
                'code': 200,
                'message': 'Done',
                'data': None
            }
        except Exception as e:
            print(e)
            return {
                'code': 400,
                'message': 'Fail',
                'data': None
            }

    # @router.delete("/delete-water/{id}")
    def remove(self, id: int, request: Request, db: Session = Depends(get_db)):
        try:
            obj = db.query(models.WaterQuality).get(id)
            db.delete(obj)
            db.commit()
            return {
                'code': 200,
                'message': 'Xóa bản ghi thành công',
                'data': None
            }
        except Exception as e:
            print(e)
            return {
                'code': 400,
                'message': 'Xóa bản ghi không thành công',
                'data': None
            }