
import uuid
from fastapi import Depends, Request
from task_manager.common_api.Api import CommonApi, db
from functools import wraps
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_restful import Resource, set_responses
from fastapi.exceptions import RequestValidationError, RequestErrorModel
from fastapi_jwt_auth.exceptions import AuthJWTException
from .dataclases import (
    RequestRegisterUser, AuthUser, AuthJWT, 
    StatusResponse, RefreshTokenResponse, ErrorResponse,
    AuthResponse, Credentionals, UserResponse, NewPasswordRequest, UpdateUserRequest
)
from .routines import get_error_response, JSONErrorResponse
from task_manager.models import User
from .crud import save_to_db, add_token_to_blacklist, is_jti_blacklisted, update_password, update_user_data


@CommonApi.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONErrorResponse(
        status_code=exc.status_code,
        text= exc.message
    )


@CommonApi.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    msg = exc.errors()[0]['msg']
    if msg == 'field required':
        msg = f"field {exc.errors()[0]['loc'][1]} required"
    return JSONErrorResponse(status_code=400, text=msg)

@CommonApi.exception_handler(500)
def bad_request_exception_handler(request: Request, exc: RequestErrorModel):
    return JSONErrorResponse(status_code=500, text="Something went wrong")


class UserRegistration(Resource):
    @set_responses(
        StatusResponse,
        200,
        {
            500: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            },
            409: {
                "model": ErrorResponse
            },
            400: {
                "model": ErrorResponse
            }
        }
    )
    def post(self, user: RequestRegisterUser, authorize: AuthJWT = Depends()):
        new_user = User(name=user.name, passwordHash=User.generate_hash(user.passwordHash), email=user.email)
        if save_to_db(new_user):
            return JSONResponse(status_code=200, content=StatusResponse(status=0).dict())
        else:
            return JSONErrorResponse(status_code=409, text=f"User with email {user.email} already exist")

            

class UserAuth(Resource):
    @set_responses(
        AuthResponse,
        200,
        {
            500: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            },
            401: {
                "model": ErrorResponse
            },
            404: {
                "model": ErrorResponse
            }
        }
    )
    def post(self, user: AuthUser, authorize: AuthJWT = Depends()):
        current_user = db.session.query(User).filter_by(email=user.email).first()
        if current_user is not None:
            if User.verify_hash(user.passwordHash, current_user.passwordHash):
                access_token = authorize.create_access_token(subject=user.email)
                refresh_token = authorize.create_refresh_token(subject=user.email)
                credentionals = Credentionals(accessToken=access_token, refreshToken=refresh_token)
                return JSONResponse(status_code=200, content=AuthResponse(credentionals=credentionals, user=UserResponse.from_orm(current_user)).to_json())
            else:
                return JSONErrorResponse(status_code=401, text="Invalid password")
        else:
            return JSONErrorResponse(status_code=404, text="User not found")





class UserLogout(Resource):
    @set_responses(
        StatusResponse,
        200,
        {
            500: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            }
        }
    )
    def post(self, authorize: AuthJWT = Depends()):
        authorize.jwt_required()
        jti = authorize.get_raw_jwt()['jti']
        add_token_to_blacklist(jti)
        return JSONResponse(status_code=200, content=StatusResponse(status=0).dict())


class RefreshAccessToken(Resource):
    @set_responses(
        RefreshTokenResponse,
        200,
        {
            401: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            }
        }
    )
    def post(self, authorize: AuthJWT = Depends()):
        authorize.jwt_refresh_token_required()
        jti = authorize.get_raw_jwt()['jti']

        if is_jti_blacklisted(jti):
            return JSONErrorResponse(status_code=401, text='Token revoked')

        current_user = authorize.get_jwt_subject()
        access_token = authorize.create_access_token(subject=current_user)
        return JSONResponse(status_code=200, content=RefreshTokenResponse(access_token=access_token).dict())


class CheckToken(Resource):
    @set_responses(
        StatusResponse,
        200,
        {
            401: {
                "model": ErrorResponse
            },
             500: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            }
        }
    )
    def get(self, authorize: AuthJWT = Depends()):
        authorize.jwt_required()
        jti = authorize.get_raw_jwt()['jti']
        if is_jti_blacklisted(jti):
            return JSONErrorResponse(status_code=401, text='Token revoked')
        return JSONResponse(status_code=200, content=StatusResponse(status=0).dict())


def jwt_required(func):
    @wraps(func)
    def wrapper(authorize: AuthJWT = Depends(), *args, **kw):
        authorize.jwt_required()
        jti = authorize.get_raw_jwt()['jti']

        if is_jti_blacklisted(jti):
            return JSONErrorResponse(status_code=401, text='Token revoked')

        return func(*args, **kw, authorize = authorize)
    return wrapper


class UserInfo(Resource):
    @set_responses(
        UserResponse,
        200,
        {
            404: {
                "model": ErrorResponse
            },
            500: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            }
        }
    )
    @jwt_required
    def get(self, id: str, authorize: AuthJWT = Depends()):
        try:
            uuId = uuid.UUID(f'{id}')
        except ValueError as e:
            return JSONErrorResponse(status_code=400, text=str(e))
        current_user = db.session.query(User).filter_by(id=uuId).first()
        if current_user is None:
            return JSONErrorResponse(status_code=404, text="User not found")
        return JSONResponse(status_code=200, content=UserResponse.from_orm(current_user).to_json())


class ChangePassword(Resource):
    @set_responses(
        StatusResponse,
        200,
        {
            404: {
                "model": ErrorResponse
            },
            403: {
                "model": ErrorResponse
            },
            500: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            }
        }
    )
    @jwt_required
    def put(self, passwords: NewPasswordRequest, authorize: AuthJWT = Depends()):
        email = authorize.get_jwt_subject()
        return update_password(passwords, email)


class UpdateUser(Resource):
    @set_responses(
        Credentionals,
        200,
        {
            404: {
                "model": ErrorResponse
            },
            403: {
                "model": ErrorResponse
            },
            500: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            }
        }
    )
    @jwt_required
    def put(self, user_data: UpdateUserRequest, authorize: AuthJWT = Depends()):
        return update_user_data(user_data, authorize)