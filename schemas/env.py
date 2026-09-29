from __future__ import annotations
from typing import List, Literal, Union, Annotated
from pydantic import BaseModel, Field, confloat, conint

# ---- Types ----
EvidenceSource = Union[
    Literal["poi_context", "general_knowledge", "poi_specific_knowledge"],
    str
]
NoiseLabel = Literal["very_low", "low", "medium", "high", "very_high"]
WaterUnit = Literal["liters"]
CO2Unit = Literal["kg"]

# ---- Base Structure (Streamlined) ----
class BaseCriterion(BaseModel):
    criterion_id: str
    criterion_name: str
    confidence: confloat(ge=0.0, le=1.0) # type: ignore
    evidence_sources: List[EvidenceSource] = Field(default_factory=list)
    evidence_used: List[str] = Field(default_factory=list)
    # assumptions and notes removed to match the new streamlined prompt

# ---- Helper Objects ----
class DailyWaterConsumption(BaseModel):
    value: float
    unit: WaterUnit

class DailyCO2Emissions(BaseModel):
    value: float
    unit: CO2Unit

# ---- Specific Criteria Implementations ----

class EnvWaterCriterion(BaseCriterion):
    criterion_id: Literal["ENV1"]
    value: confloat(ge=0.0, le=1.0) # type: ignore
    actual_water_consumption_daily: DailyWaterConsumption

class EnvCO2Criterion(BaseCriterion):
    criterion_id: Literal["ENV2"]
    value: confloat(ge=0.0, le=1.0) # type: ignore
    actual_co2_emissions_daily: DailyCO2Emissions

class EnvNoiseCriterion(BaseCriterion):
    criterion_id: Literal["ENV3"]
    noise_label: NoiseLabel
    noise_level_1_to_5: conint(ge=1, le=5) # type: ignore

class EnvPollutionCriterion(BaseCriterion):
    criterion_id: Literal["ENV4"]
    value: confloat(ge=0.0, le=1.0) = 0.1 # type: ignore

class EnvBiodiversityCriterion(BaseCriterion):
    criterion_id: Literal["ENV5"]
    value: confloat(ge=0.0, le=1.0) = 0.1 # type: ignore

# ---- Final Union and Assessment Model ----

EnvCriterion = Annotated[
    Union[
        EnvWaterCriterion,
        EnvCO2Criterion,
        EnvNoiseCriterion,
        EnvPollutionCriterion,
        EnvBiodiversityCriterion
    ],
    Field(discriminator="criterion_id")
]

class EnvAssessment(BaseModel):
    pillar: Literal["environmental"]
    poi_id: str
    title: str
    criteria: List[EnvCriterion]