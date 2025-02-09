from typing import Optional

from pydantic import BaseModel


class Proxy(BaseModel):
    host: str
    port: int
    user: Optional[str] = None
    password: Optional[str] = None
