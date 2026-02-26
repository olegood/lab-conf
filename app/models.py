"""Pydantic models for configuration service API requests and responses.

This module defines the data models used for validating and serializing
configuration data in the Flask API endpoints.
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ConfigCreateRequest(BaseModel):
    """Request a model for creating a new configuration.
    
    Attributes:
        data: Key-value configuration data to be stored.
        created_by: Username or identifier of the person creating the configuration.
    """
    data: dict[str, Any] = Field(..., description="Key-value configuration data")
    created_by: str


class ConfigResponse(BaseModel):
    """Response model representing a stored configuration.
    
    Attributes:
        service: Name of the service this configuration belongs to.
        environment: Environment name (e.g., "dev", "staging", "prod").
        version: Unique version identifier (UUID) for this configuration.
        data: The stored key-value configuration data.
        created_at: Timestamp when the configuration was created.
        created_by: Username or identifier of the person who created the configuration.
    """
    service: str
    environment: str
    version: str
    data: dict[str, Any]
    created_at: datetime
    created_by: str
