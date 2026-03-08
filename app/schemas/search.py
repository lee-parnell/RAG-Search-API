from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query:str = Field(... , description="The search query to be processed by the AI Smart Search Engine")
    limit: int =Field(gt=2 , le=10 , description="The maximum number of search results to return (between 3 and 15)")





class Source(BaseModel):
    title: str
    url: str
        