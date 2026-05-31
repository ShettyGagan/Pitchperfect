from toon import encode , decode , generate_structure, generate_structure_from_pydantic
from pydantic import BaseModel
from typing import Any


# encode decode functions

def to_toon(data:dict|list)->str:
    return encode(data)

def from_toon(toonstr:str)->dict|list:
    return decode(toonstr)


def structure_template(schema:dict|list)->str:
    return generate_structure(schema)

def structure_template_pydantic(model_class: type[BaseModel]) -> str:
    return generate_structure_from_pydantic(model_class)



# Convenience: compress an already-parsed agent result before forwarding 
def compress_agent_result(data: dict | list) -> str:
    return to_toon(data)
