# convert the raw json from extract_functional_requirements function to a structure python object

import json
from pydantic import BaseModel, Field

class EndpointSpec(BaseModel):
    path: str = Field(..., description="API path, e.g., /users")
    method: str = Field(..., description="HTTP method, e.g., GET, POST")
    params: list = Field(..., description="List of parameters accepted by the endpoint")
    description: str = Field(..., description="Description of the endpoint")

class FunctionalRequirements(BaseModel):
    endpoints: list[EndpointSpec]
    logic: str
    db_schema: str
    auth: str

def parse_requirements(req_json:str) -> FunctionalRequirements:
    data = json.loads(req_json)
    return FunctionalRequirements(**data)