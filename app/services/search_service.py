from tavily import MissingAPIKeyError, AsyncTavilyClient
from ..core.config import get_settings
from typing import Optional
import re

setting = get_settings()


class SearchService:
    def __init__(self , api_key: Optional[str] = None):
        if api_key is None:
            api_key = setting.TAVILY_API_KEY

        if not api_key:
            raise MissingAPIKeyError("TAVILY_API_KEY is required to initialize SearchService")    
        
        self.client = AsyncTavilyClient(api_key=api_key , 
                                        )

    async def search(self, query: str):
        # Clean the query by removing special characters
        pattern = r"[^a-zA-Z0-9\u0600-\u06FF\"\'\s\?؟\!\.!]"
        cleaned_query = re.sub(pattern, '', query)

        response = await self.client.search(cleaned_query, 
                                            max_results=10 ,
                                            search_depth='basic')
        return response
        
            

