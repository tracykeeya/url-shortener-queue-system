from pydantic import BaseModel

class URLCreate(BaseModel):
    original_url: str

class URLInfo(BaseModel):
    short_url: str
    original_url: str
    visit_count: int

    class Config:
        from_attributes = True


    # class Config:
    #     orm_mode = True
