from pydantic import BaseModel, Field
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description='Natural-language search query')
    top_k: int = Field(default=5, ge=1, le=20, description='Number of top SubTopics to match')

class VideoResult(BaseModel):
    vc_id: int
    subtopic_id: int
    subtopic: str
    caption: str
    file_name: str
    thumbnail: str
    score: float

class SearchResponse(BaseModel):
    query: str
    results: List[VideoResult]
    total: int
    time_ms: float
