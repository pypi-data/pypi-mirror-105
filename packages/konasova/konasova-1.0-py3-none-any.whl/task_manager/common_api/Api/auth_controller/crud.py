from task_manager.models import User, RevokedTokenModel
from task_manager.common_api.Api import db
from .dataclases import NewPasswordRequest, UpdateUserRequest, Credentionals, StatusResponse
from fastapi.responses import JSONResponse    
from fastapi_jwt_auth import AuthJWT
from .routines import JSONErrorResponse

def save_to_db(new_user: User):
    """ сохраняем пользователя в базу если его еще там нет """
    if db.session.query(User).filter(User.email==new_user.email).first() is not None:
        return None
    else:
        db.session.add(new_user)
        db.session.commit()
        return 'ok'


def update_password(passwords: NewPasswordRequest, email: str):
    """ обновляем пароль пользователя """
    user = db.session.query(User).filter(User.email==email).first()
    if user is None:
        return JSONErrorResponse(status_code=404,text='User not found')

    if User.verify_hash(passwords.passwordHashOld, user.passwordHash):        
        user.passwordHash = User.generate_hash(passwords.passwordHashNew)
        db.session.merge(user)
        db.session.commit()
        return JSONResponse(status_code=200, content=StatusResponse(status=0).dict())
    else:
        return JSONErrorResponse(status_code=403, text='Old Password is not correct')


def update_user_data(user_data: UpdateUserRequest, authorize: AuthJWT):
    """ обновляем данные о пользователе """
    email = authorize.get_jwt_subject()
    user = db.session.query(User).filter(User.email==email).first()
    if user is None:
        return JSONErrorResponse(status_code=404,text='User not found')

    user.name = user_data.name
    user.surname = user_data.surname
    if len(db.session.query(User).filter(User.email==user_data.email).all()) <= 1:
        user.email = user_data.email
    else:
        return JSONErrorResponse(status_code=403,text='Another email exist')
    user.about = user_data.about
    user.telegram = user_data.telegram
    user.phone = user_data.phone
    user.skype = user_data.skype
    user.slack = user_data.slack

    db.session.merge(user)
    db.session.commit()
    
    access_token = authorize.create_access_token(subject=user.email)
    refresh_token = authorize.create_refresh_token(subject=user.email)
    credentionals = Credentionals(accessToken=access_token, refreshToken=refresh_token)
    return JSONResponse(status_code=200, content=credentionals.dict())


def add_token_to_blacklist(jti: str):
    """ добавляем токен в блэклист """
    revoked_token = RevokedTokenModel(jti = jti)
    db.session.add(revoked_token)
    db.session.commit()


def is_jti_blacklisted(jti):
    """ проверяем есть ли токен в блэклист """
    query = db.session.query(RevokedTokenModel).filter_by(jti = jti).first()
    return bool(query)

