from pydantic import BaseModel, Field

from mmisp.lib.attributes import mapper_val_safe_clsname

GetAttributeStatisticsTypesResponseAttrs = {x: Field(default=None) for x in mapper_val_safe_clsname.keys()}
GetAttributeStatisticsTypesResponseAttrs["__annotations__"] = {x: str | None for x in mapper_val_safe_clsname.keys()}
GetAttributeStatisticsTypesResponse = type(
    "GetAttributeStatisticsTypesResponse", (BaseModel,), GetAttributeStatisticsTypesResponseAttrs
)


class GetAttributeStatisticsCategoriesResponse(BaseModel):
    antivirus_detection: str = Field(alias="Antivirus detection")
    artifacts_dropped: str = Field(alias="Artifacts dropped")
    attribution: str = Field(alias="Attribution")
    external_analysis: str = Field(alias="External analysis")
    financial_fraud: str = Field(alias="Financial fraud")
    internal_reference: str = Field(alias="Internal reference")
    network_activity: str = Field(alias="Network activity")
    other: str = Field(alias="Other")
    payload_delivery: str = Field(alias="Payload delivery")
    payload_installation: str = Field(alias="Payload installation")
    payload_type: str = Field(alias="Payload type")
    persistence_mechanism: str = Field(alias="Persistence mechanism")
    person: str = Field(alias="Person")
    social_network: str = Field(alias="Social network")
    support__tool: str = Field(alias="Support Tool")
    targeting_data: str = Field(alias="Targeting data")

    class Config:
        orm_mode = True
