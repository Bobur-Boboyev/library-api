from typing import Annotated, Self

from pydantic import BaseModel, Field, model_validator, ConfigDict


class UserRegister(BaseModel):
    username: Annotated[str, Field(min_length=5, max_length=100)]
    password: Annotated[str, Field(min_length=8, max_length=50)]
    confirm: Annotated[str, Field(min_length=8, max_length=50)]

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm:
            raise ValueError("Passwords do not match")
        return self


class UserResponse(BaseModel):
    id: int
    username: Annotated[str, Field(min_length=5, max_length=100)]
    hash_password: Annotated[str, Field(max_length=255)]

    model_config = ConfigDict(from_attributes=True)
