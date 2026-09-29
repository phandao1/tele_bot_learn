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

## Docker

```bash
docker compose up --build
curl localhost:8000/health
```

## Lộ trình

- [x] Bước 1: parser, báo cáo, API tối thiểu, test
- [ ] Bước 2: GitHub Actions (lint + test + build image)
- [ ] Bước 3: PostgreSQL lưu chi tiêu
- [ ] Bước 4: Telegram bot
- [ ] Bước 5: deploy staging/production, rollback
