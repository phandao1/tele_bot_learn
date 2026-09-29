# Expense Bot

Bot ghi chi tiêu: nhắn "cafe 45k" là tự ghi. Project học CI/CD.

## Chạy trên máy

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest            # chạy test
ruff check .      # lint
uvicorn app.main:app --reload   # chạy API, mở http://localhost:8000/docs
```

## Test với PostgreSQL (integration test)

Test cần DB đọc `TEST_DATABASE_URL` (tách riêng, vì test xoá sạch bảng). Không set thì các test này tự bỏ qua.

```bash
docker compose --profile test up -d db_test
export TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5433/expense_test
pytest -v
docker compose --profile test down   # xoá DB test
```

## Docker

```bash
docker compose up --build
curl localhost:8000/health
```

## Lộ trình

- [x] Bước 1: parser, báo cáo, API tối thiểu, test
- [x] Bước 2: GitHub Actions (lint + test + build image)
- [x] Bước 3: PostgreSQL lưu chi tiêu, test với DB thật trong CI
- [ ] Bước 4: Telegram bot
- [ ] Bước 5: deploy staging/production, rollback
