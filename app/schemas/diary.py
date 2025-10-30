from pydantic import BaseModel, Field


class DiaryCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="제목을 적어주세요 (100자 이내)",
    )
    content: str = Field(
        description="내용을 적어주세요",
    )
