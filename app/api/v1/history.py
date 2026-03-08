from fastapi import APIRouter , Depends
from ...db.redis import get_redis_client
from typing import Annotated
import redis
from...schemas.response import HistoryResponse

router = APIRouter(prefix="/history" , tags=["history"])

redis_client = Annotated[redis.Redis , Depends(get_redis_client)]

@router.get("/" , response_model=HistoryResponse)
async def search_history(redis_ : redis_client):
    searches = await redis_.lrange("search_history", 0, 9)
    return HistoryResponse(searches=searches,total= len(searches))