import jwt

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.settings import SessionLocal, engine, get_db

from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from starlette import status

from models.models import User, UserLogin
from core.settings import settings
from core.security import verify_password, hash_password, create_access_token_v2
# from app.schemas.sche_token import TokenPayload

from shared_func.views_func import format_response_data

import json


class Authentication(object):
    # __instance = None

    # def __init__(self) -> None:
    #     pass

    # reusable_oauth2 = HTTPBearer(
    #     scheme_name='Authorization'
    # )

    async def login_access_token(self, request: Request, db: Session = Depends(get_db)):
        try:
            data = await request.json()

            account = data['account']
            password = data['password']
            # user = user_service.authenticate(email=form_data.username, password=form_data.password)
            instance = db.query(UserLogin).filter(
                UserLogin.account == account,
                # UserLogin.password == password,
                UserLogin.is_deleted == False
            ).first()

            if not verify_password(password, instance.password):
                raise HTTPException(status_code=400, detail='Incorrect email or password')
            if not instance:
                raise HTTPException(status_code=400, detail='Incorrect email or password')
            elif not instance.user:
                raise HTTPException(status_code=401, detail='Inactive user')
            elif not instance.user.is_activate:
                raise HTTPException(status_code=400, detail='User is Locked')
            # user.last_login = datetime.now()
            # db.session.commit()


            user_instance = {
                'id': instance.user.id,
                'roles': [role.name for role in instance.user.roles]
            }

            access_token = create_access_token_v2(user_instance)

            response_content = json.dumps({
                    'code': 200,
                    'message': 'Done',
                    'data': {
                        'access_token': access_token
                    }
            })
            
            return Response(content=response_content, media_type="application/json", status_code=200)

            # return DataResponse().success_response({
            #     'access_token': create_access_token(user_id=user.id)
            # })
        except Exception as e:
            print(e)
            return Response(content=json.dumps({'code': 400, 'message': 'Fail', 'data': None}), media_type="application/json", status_code=400)
    
    async def signup(self, request: Request, db: Session = Depends(get_db)):
        try:
            data = await request.json()

            ### Thiếu check tài khoản tồn tại 

            account = data['account']
            password = data['password']

            user = User()
            db.add(user)
            db.commit()
            db.refresh(user)

            if not user.id:
                raise HTTPException(status_code=401, detail='Inactive user')
            
            hashed_password = hash_password(password)
            
            user_login = UserLogin(
                user_id = user.id,
                account = account,
                password = hashed_password
            )
            db.add(user_login)
            db.commit()
            db.refresh(user_login)

            response_content = json.dumps({
                'code': 200,
                'message': 'Done',
                'data': None
            })
            
            return Response(content=response_content, media_type="application/json", status_code=200)
        except Exception as e:
            print(e)
            return Response(content=json.dumps({'code': 400, 'message': 'Fail', 'data': None}), media_type="application/json", status_code=400)