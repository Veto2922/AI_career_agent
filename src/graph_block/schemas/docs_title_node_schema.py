from pydantic import BaseModel, Field
from typing import List

class DocsTitleNodeSchema(BaseModel):
    selected_indexes: List[int] = Field(
        default_factory=list,
        description="The docs indexes related to the user query."
    )
