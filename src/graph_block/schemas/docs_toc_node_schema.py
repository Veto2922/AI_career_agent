from pydantic import BaseModel, Field
from typing import List

class TargetDoc(BaseModel):
    doc_index: int = Field(
        ...,
        description="Index of the document in the docs list"
    )
    target_ids: List[str] = Field(
        ...,
        description="List of relevant chunk or section IDs داخل الدوك"
    )

class DocsTocNodeSchema(BaseModel):
    selected_docs: List[TargetDoc] = Field(
        default_factory=list,
        description="List of documents and their relevant target IDs for the query"
    )
