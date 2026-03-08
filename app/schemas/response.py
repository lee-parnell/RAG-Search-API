from pydantic import BaseModel
class SearchResponse(BaseModel):
    answer: str
    sources: list  

class HistoryResponse(BaseModel):
    searches: list[str]
    total: int