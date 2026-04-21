"""Data models for the restaurant bot."""

from pydantic import BaseModel
from typing import Optional


class RestaurantContext(BaseModel):
    customer_name: str
    phone: Optional[str] = None
    dietary_preference: Optional[str] = None


class HandoffData(BaseModel):
    to_agent_name: str
    request_type: str
    request_summary: str
    reason: str