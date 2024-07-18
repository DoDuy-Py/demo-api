from core.security import hash_password
from core.settings import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from models.models import User, Role, UserLogin, user_roles

from constants.global_constants import BASE_API
import json

session = Session(engine)

def format_response_data(status: int, message: str, data=None):
    data = {
        'code': status,
        'message': message,
        'data': data
    }
    return json.dumps(data)


def init_db():
    try:
        print(f'Run function name: {init_db.__name__}')
        user_instance = session.execute(select(User)).scalars().all()
        if not user_instance:
            user_default = User()
            session.add(user_default)
            session.commit()
            session.refresh(user_default)
            # session.close()

            user_login = UserLogin(
                user_id = user_default.id,
                account = 'admin',
                password = hash_password('123'),
            )
            session.add(user_login)
            session.commit()
            session.refresh(user_login)

        role_instance = session.execute(select(Role)).scalars().all()
        if not role_instance:
            objects = [
                Role(name="admin", description="Quản trị viên"),
                Role(name="user", description="Người dùng bình thường"),
            ]
            session.add_all(objects)
            session.commit()
            # session.bulk_save_objects(objects)
            # session.refresh(objects)
            for role in objects:
                session.refresh(role)
            role_instance = objects

        if not user_instance:
            # Thêm quyền cho user mặc định nếu chưa có
            user_roles_instance = session.execute(
                select(user_roles).where(user_roles.c.user_id == user_default.id)
            ).fetchall()
            if not user_roles_instance:
                for role in role_instance:
                    session.execute(
                        insert(user_roles).values(user_id=user_default.id, role_id=role.id)
                    )
                session.commit()

    except Exception as e:
        print(e)
    finally:
        session.close()