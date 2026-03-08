from ...services.llm_service import LLMService 
from...services.search_service import SearchService
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


_search_service = SearchService()
_llm_service = LLMService()

def get_search_service():
    return _search_service

def get_llm_service():
    return _llm_service