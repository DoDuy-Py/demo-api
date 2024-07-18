import jwt

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from core.settings import get_db

from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from models.models import User, UserLogin, user_roles, Role

from shared_func.views_func import format_response_data
from core.settings import settings

from sqlalchemy.orm import Session
from sqlalchemy import delete, select, insert
from shared_func.views_func import session

from .auth_token import validate_token
from .auth import hash_password

import json

class UserViewSet:
    __instance = None

    def __init__(self) -> None:
        pass

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )

    permission_classes = []
    authentication_classes = [HTTPBearer()]

    def get_profile(self, id: int, request: Request, db: Session = Depends(get_db)):
        try:
            auth = request.headers.get("Authorization")
            if not auth:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token not provided")
            
            user = validate_token(auth)
            if not user:
                return Response(content=format_response_data(400, "Faile", None), media_type="application/json", status_code=400)
            
            return Response(content=json.dumps({'code': 200, 'message': 'Success', 'data': None}), media_type="application/json", status_code=200)

        except Exception as e:
            print(e)
            return Response(content=format_response_data(400, "Faile", None), media_type="application/json", status_code=400)
    
    async def create(self, request: Request, db: Session = Depends(get_db)):
        '''
            @API create user
            @Input: No
            @Output: User
        '''
        try:
            auth = request.headers.get("Authorization")
            if not auth:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token not provided")
            
            user = validate_token(auth)
            if not user:
                return Response(content=format_response_data(400, "Faile", None), media_type="application/json", status_code=400)
            
            if 'admin' not in user.roles:
                return Response(content=format_response_data(400, "Không có quyền", None), media_type="application/json", status_code=400)
            
            ### Create
            input_data = await request.json()
            account = input_data.get('account')
            password = input_data.get('password')

            if not account or not password:
                return Response(content=format_response_data(400, "Vui lòng nhập đủ thông tin", None), media_type="application/json", status_code=400)
            
            user_instance = User()
            db.add(user_instance)
            db.commit()
            db.refresh()

            user_login = UserLogin(
                user_id = user.id,
                account = account,
                password = hash_password(password)
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
            return Response(content=format_response_data(400, "Faile", None), media_type="application/json", status_code=400)


class RoleViewSet:

    def add_role(self):
        pass

    async def update_roles_user(self, request: Request, db: Session = Depends(get_db)):
        try:
            auth = request.headers.get("Authorization")
            if not auth:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token not provided")
            
            user = validate_token(auth)
            if not user:
                return Response(content=format_response_data(400, "Faile", None), media_type="application/json", status_code=400)
            
            if 'admin' not in user.roles:
                return Response(content=format_response_data(400, "Không có quyền", None), media_type="application/json", status_code=400)
            
            data_input = await request.json()
            user_id = data_input.get('user_id')
            roles = data_input.get('roles')
            roles = set(roles.split(','))
            if not user_id:
                return Response(content=format_response_data(400, "Thiếu user_id", None), media_type="application/json", status_code=400)
            
            user_instance = db.query(User).filter(
                User.id == user_id,
                User.is_activate == True,
                User.is_deleted == False
            ).first()
            if not user_instance:
                return Response(content=format_response_data(400, "User not found", None), media_type="application/json", status_code=404)
            
            current_roles = session.execute(
                select(user_roles).where(user_roles.c.user_id == user_id)
            ).fetchall()
        
            set_current_role = {user_role.role_id for user_role in current_roles}

            role_instance = db.query(Role).all()
            role_ids = set([role.id for role in role_instance])

            roles = role_ids.intersection(roles) # Chỉ lấy những id đúng

            role_delete = set_current_role - roles
            role_add = roles - set_current_role

            # Xóa các role không còn trong danh sách mới
            if role_delete:
                delete_stmt = delete(user_roles).where(
                    user_roles.c.user_id == user_id,
                    user_roles.c.role_id.in_(role_delete)
                )
                session.execute(delete_stmt)
            
            if roles:
                for role in role_add:
                    session.execute(
                            insert(user_roles).values(user_id=user_id, role_id=role)
                        )
            session.commit()
            session.close()

            return Response(content=format_response_data(200, "Update thành công", None), media_type="application/json", status_code=200) 
        except Exception as e:
            print(e)
            return Response(content=format_response_data(400, "Có lỗi xảy ra", None), media_type="application/json", status_code=400)