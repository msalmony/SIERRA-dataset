from __future__ import annotations
from typing import List, Literal
from pydantic import BaseModel, Field, confloat

class TestCriterion(BaseModel):
    criterion_id: Literal["T1", "T2"]
    criterion_name: str
    value: confloat(ge=0.0, le=1.0) # type: ignore
    confidence: confloat(ge=0.0, le=1.0) # type: ignore
    notes: str

class TestAssessment(BaseModel):
    pillar: Literal["test"]
    poi_id: str
    poi_title: str
    criteria: List[TestCriterion] = Field(default_factory=list)
   
