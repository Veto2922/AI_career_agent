from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from langchain.messages import AnyMessage
from typing_extensions import Annotated
import operator

class GraphState(BaseModel):
    # input
    messages: Annotated[List[AnyMessage], operator.add] = Field(default_factory=list)
    user_query: str = ""

    docs_titles: List[Dict] = Field(default_factory=list)

    # router outputs
    router_outputs: Dict[str, Any] = Field(default_factory=dict)

    # title node
    selected_docs_indexes: List[int] = Field(default_factory=list)

    # context selector
    target_docs: List[Dict] = Field(default_factory=list)
