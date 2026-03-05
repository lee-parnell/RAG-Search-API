from fastapi import APIRouter, HTTPException, Query , Depends
from...services.search_service import SearchService
from ...schemas.search import SearchRequest , SearchResponse , Source
from ...services.llm_service import LLMService
from app.services import search_service

from app.services import llm_service



router = APIRouter(prefix="/search", tags=["search"])

_search_service = SearchService()
_llm_service = LLMService()

def get_search_service():
    return _search_service

def get_llm_service():
    return _llm_service

@router.post("/" , summary="Search for information using the AI Smart Search Engine"  , response_model=SearchResponse)
async def search(search_request: SearchRequest ,
                 search_svc: SearchService = Depends(get_search_service) ,
                 llm_service: LLMService = Depends(get_llm_service)
                 ):
    """
    Search for information using the AI Smart Search Engine.

    - **query**: The search query to be processed by the AI Smart Search Engine.

    Returns a JSON response containing the search results.
    """
    try:
        search_results = await search_svc.search(search_request.query)
        if not search_results:
            return SearchResponse(answer="I apologize, but I couldn't find any relevant information based on your query.", sources=[])
        results_list = search_results.get("results", [])
        answer = await llm_service.generate_answer(search_request.query, results_list)
        sources = [Source(title=r.get("title",""), url=r.get("url","")) for r in results_list]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Search Error: {str(e)}")
    
    return SearchResponse(answer=answer, sources=sources)

