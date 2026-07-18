"""
Dataset models.

Defines all resources used by the Digital Twin.
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DatasetResource(BaseModel):
    """
    One Andrew Ng resource.
    """

    id: str

    title: str

    author: str = "Andrew Ng"

    source: str

    local_path: str

    resource_type: str

    category: str

    tags: List[str] = Field(default_factory=list)

    language: str = "en"

    published_year: Optional[int] = None

    description: Optional[str] = None

    metadata: Dict = Field(default_factory=dict)

    indexed: bool = False

    personality_processed: bool = False

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class DatasetRegistry(BaseModel):
    """
    Registry of all imported resources.
    """

    resources: List[DatasetResource] = Field(
        default_factory=list
    )