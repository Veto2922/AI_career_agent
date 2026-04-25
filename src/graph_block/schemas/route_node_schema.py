from pydantic import BaseModel, Field

class RouteNodeSchema(BaseModel):
    need_retrieval: bool = Field(
        ...,
        description="True if external retrieval is required, otherwise False."
    )
