from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,  # bcrypt 제한 72바이트에 맞춤
        description="비밀번호는 8자 이상 72자 이하",
    )


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
