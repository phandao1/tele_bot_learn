from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app import db
from app.parser import ParsedExpense, ParseError, parse_expense
from app.report import format_summary, summarize


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()  # tạo bảng nếu chưa có
    yield


app = FastAPI(title="Expense Bot", lifespan=lifespan)


class TextRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/parse")
def parse(req: TextRequest):
    """Chỉ phân tích câu nhắn, không lưu."""
    try:
        e = parse_expense(req.text)
    except ParseError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"amount": e.amount, "note": e.note, "category": e.category}


@app.post("/expenses", status_code=201)
def create_expense(req: TextRequest):
    try:
        parsed = parse_expense(req.text)
    except ParseError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return db.add_expense(parsed)


@app.get("/expenses")
def get_expenses(days: int = Query(7, ge=1, le=3650)):
    return db.list_expenses(days)


@app.get("/summary")
def get_summary(days: int = Query(7, ge=1, le=3650)):
    rows = db.list_expenses(days)
    summary = summarize(
        ParsedExpense(amount=r["amount"], note=r["note"], category=r["category"]) for r in rows
    )
    return {**summary, "text": format_summary(summary)}
