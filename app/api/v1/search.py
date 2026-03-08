from fastapi import APIRouter, HTTPException, Request , Depends
from ...schemas.search import SearchRequest , Source
from ...schemas.response import SearchResponse
from fastapi.responses import StreamingResponse
from ...db.redis import get_redis_client
import redis
from typing import Annotated
from .deps import get_llm_service , get_search_service
from ...services.llm_service import LLMService 
from...services.search_service import SearchService
from ...api.v1.deps import limiter



router = APIRouter(prefix="/search", tags=["search"])


RedisClient = Annotated[redis.Redis , Depends(get_redis_client)]
@router.post("/" , summary="Search for information using the AI Smart Search Engine"  , response_model=SearchResponse)
@limiter.limit("5/minute")
async def search(request: Request,
                redis_ : RedisClient,
                search_request: SearchRequest ,
                 search_svc: SearchService = Depends(get_search_service) ,
                 llm_service: LLMService = Depends(get_llm_service) ,
                 
                 ):
    """
    Search for information using the AI Smart Search Engine.

    - **query**: The search query to be processed by the AI Smart Search Engine.

    Returns a JSON response containing the search results.
    """
    try:
        cached = await redis_.get(search_request.query)
        if cached:
            return SearchResponse(answer= cached , sources=[])
        search_results = await search_svc.search(search_request.query)
        if not search_results:
            return SearchResponse(answer="I apologize, but I couldn't find any relevant information based on your query.", sources=[])
        results_list = search_results.get("results", [])
        answer = await llm_service.generate_answer(search_request.query, results_list)
        await redis_.set(search_request.query , answer , ex= 3600)
        sources = [Source(title=r.get("title",""), url=r.get("url","")) for r in results_list]
        await redis_.lpush("search_history" , search_request.query)
        await redis_.ltrim("search_history" , 0 , 4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Search Error: {str(e)}")
    
    return SearchResponse(answer=answer, sources=sources)



@router.post("/stream")
@limiter.limit("3/minute")
async def search_stream(
    request : Request,
    redis_ : RedisClient ,
    search_request: SearchRequest,
    search_svc: SearchService = Depends(get_search_service),
    llm_svc: LLMService = Depends(get_llm_service)
):
    cached = await redis_.get(search_request.query)
    if cached:
            async def cached_generator():
                yield f"data: {cached}\n\n"
                yield "data: [DONE]\n\n"
            return StreamingResponse(cached_generator(), media_type="text/event-stream")    
    
    search_results = await search_svc.search(search_request.query)
    results_list = search_results.get("results", [])
    
    async def event_generator():
        full_answer = ""  
        async for chunk in llm_svc.generate_answer_stream(search_request.query , results_list):
            full_answer += chunk 
            yield f"data: {chunk}\n\n"
    
        await redis_.set(search_request.query, full_answer, ex=3600)
        await redis_.lpush("search_history" , search_request.query)
        await redis_.ltrim("search_history" , 0 , 4)
        yield "data: [DONE]\n\n" 
        

    return StreamingResponse(event_generator(),
                            media_type="text/event-stream" )
