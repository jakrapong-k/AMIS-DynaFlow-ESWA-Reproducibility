# API Design for MVP App (Phase 2)

## 1) Principles

- REST-first และ schema-driven
- แยก synchronous requests ออกจาก asynchronous execution อย่างชัดเจน
- ทุก endpoint ที่เกี่ยวกับ run ต้อง trace ด้วย `run_id`
- response รูปแบบคงที่เพื่อลด coupling กับ frontend

---

## 2) API Versioning

Base path:

- `/api/v1`

---

## 3) Authentication Endpoints

## `POST /api/v1/auth/login`

ใช้สำหรับรับ token (MVP อาจเป็น internal auth หรือ mock identity provider)

**Request**

```json
{
  "email": "user@example.com",
  "password": "********"
}
```

**Response 200**

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "usr_123",
    "email": "user@example.com",
    "role": "operator"
  }
}
```

---

## 4) Run Management Endpoints

## `POST /api/v1/runs`

สร้างงานใหม่สำหรับ forecast/optimize/adapt

**Request**

```json
{
  "run_type": "full_pipeline",
  "input_ref": "sample_dataset_v1",
  "config": {
    "seed": 42,
    "experiment": "default"
  }
}
```

**Response 202**

```json
{
  "run_id": "run_20260520_0001",
  "status": "queued",
  "created_at": "2026-05-20T10:00:00Z"
}
```

## `GET /api/v1/runs`

ดึงรายการ runs พร้อม filter

**Query params (optional)**
- `status`: queued|running|succeeded|failed
- `limit`: default 20
- `offset`: default 0

**Response 200**

```json
{
  "items": [
    {
      "run_id": "run_20260520_0001",
      "run_type": "full_pipeline",
      "status": "running",
      "created_by": "usr_123",
      "created_at": "2026-05-20T10:00:00Z",
      "started_at": "2026-05-20T10:01:00Z",
      "finished_at": null
    }
  ],
  "total": 1
}
```

## `GET /api/v1/runs/{run_id}`

ดูสถานะรายละเอียด run

**Response 200**

```json
{
  "run_id": "run_20260520_0001",
  "status": "succeeded",
  "status_message": "completed",
  "run_type": "full_pipeline",
  "config_hash": "sha256:...",
  "input_hash": "sha256:...",
  "created_by": "usr_123",
  "created_at": "2026-05-20T10:00:00Z",
  "started_at": "2026-05-20T10:01:00Z",
  "finished_at": "2026-05-20T10:05:00Z",
  "error": null
}
```

## `GET /api/v1/runs/{run_id}/metrics`

ดึง metrics ของ run

**Response 200**

```json
{
  "run_id": "run_20260520_0001",
  "metrics": [
    {"name": "mae", "value": 2.31},
    {"name": "service_level", "value": 0.94},
    {"name": "utilization", "value": 0.88}
  ]
}
```

## `GET /api/v1/runs/{run_id}/artifacts`

แสดงรายการไฟล์ผลลัพธ์ที่ดาวน์โหลดได้

**Response 200**

```json
{
  "run_id": "run_20260520_0001",
  "artifacts": [
    {
      "type": "summary_csv",
      "path": "results/sample_outputs/reproduction_summary.csv",
      "checksum": "sha256:..."
    }
  ]
}
```

---

## 5) Dashboard Endpoints

## `GET /api/v1/dashboard/summary`

**Response 200**

```json
{
  "total_runs": 128,
  "success_rate": 0.96,
  "avg_runtime_seconds": 242,
  "active_runs": 3
}
```

## `GET /api/v1/dashboard/trends`

**Response 200**

```json
{
  "daily": [
    {"date": "2026-05-18", "runs": 21, "success_rate": 0.95},
    {"date": "2026-05-19", "runs": 18, "success_rate": 0.94}
  ]
}
```

---

## 6) Error Model

มาตรฐาน error:

```json
{
  "error": {
    "code": "RUN_NOT_FOUND",
    "message": "Run id not found",
    "details": null
  }
}
```

HTTP status mapping:
- 400: validation error
- 401: unauthorized
- 403: forbidden
- 404: not found
- 409: conflict (invalid status transition)
- 500: internal server error

---

## 7) Authorization Matrix (MVP)

- `admin`: ทุก endpoint
- `operator`: สร้าง run, ดู run/metrics/artifacts/dashboard
- `viewer`: ดู run/metrics/artifacts/dashboard, ห้ามสร้าง run

---

## 8) Test Contract Priorities

1. `POST /runs` ต้องได้ 202 และ run_id
2. `GET /runs/{id}` สะท้อน status transition ถูกต้อง
3. endpoint ต้อง reject token ไม่ถูกต้องด้วย 401
4. `viewer` เรียก `POST /runs` ต้องได้ 403
