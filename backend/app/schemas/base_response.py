from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')
 
class BaseResponse(BaseModel):
    code: int = 0
    msg: str = 'success'
    data: Optional[object] = None 