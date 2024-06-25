from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('/')
def read(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'token': token}
