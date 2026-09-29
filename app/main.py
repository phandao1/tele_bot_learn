from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os   
from app.parser import ParseError, parse_expense

app = FastAPI(title="Expense Bot")


class ParseRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/parse")
def parse(req: ParseRequest):
    try:
        e = parse_expense(req.text)
    except ParseError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"amount": e.amount, "note": e.note, "category": e.category}
