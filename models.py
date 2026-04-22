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


class InputGuardRailOutput(BaseModel):
    is_off_topic: bool
    has_inappropriate_language: bool
    reason: str


class OutputGuardRailOutput(BaseModel):
    is_inappropriate: bool
    exposes_internal_info: bool
    reason: str