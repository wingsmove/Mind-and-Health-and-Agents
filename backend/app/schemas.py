from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    message: str


class AnalyzeResponse(BaseModel):
    content: str
    report: str
