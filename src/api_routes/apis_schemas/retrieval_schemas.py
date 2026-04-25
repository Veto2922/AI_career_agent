from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DocIndicesRequest(BaseModel):
    doc_indices: List[int]

class TargetDoc(BaseModel):
    doc_index: int
    target_ids: List[str]

class RetrieveRequest(BaseModel):
    target_docs: List[TargetDoc]

class DocTitle(BaseModel):
    doc_index: int
    name: str
    description: Optional[str] = None

class TitlesResponse(BaseModel):
    titles: List[DocTitle]

class TOCResponse(BaseModel):
    toc: List[Any]

class RetrievalContentResponse(BaseModel):
    content: List[Any]
