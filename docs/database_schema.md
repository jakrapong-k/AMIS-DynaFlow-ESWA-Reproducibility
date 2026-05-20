# Database Schema Plan for MVP App (Phase 2)

## 1) Scope

เอกสารนี้ออกแบบฐานข้อมูลสำหรับ MVP app โดยเน้น metadata ของการรัน workflow, ผู้ใช้งาน, metrics และ artifact indexing เพื่อรองรับ dashboard และการ trace ย้อนหลัง

DB engine เป้าหมาย: **PostgreSQL**

---

## 2) Entity Relationship (MVP)

```text
users (1) ---- (N) runs (1) ---- (N) run_metrics
                      \
                       \---- (N) artifacts
```

---

## 3) Table Definitions

## `users`

- `id` (PK, text/uuid)
- `email` (unique, not null)
- `password_hash` (not null, ถ้าใช้ local auth)
- `role` (not null; enum: admin/operator/viewer)
- `is_active` (boolean, default true)
- `created_at` (timestamp with tz)
- `updated_at` (timestamp with tz)

Indexes:
- unique index on `email`

## `runs`

- `id` (PK, text/uuid)
- `created_by` (FK -> users.id, not null)
- `run_type` (text, not null)
- `status` (text, not null; queued/running/succeeded/failed/cancelled)
- `status_message` (text, nullable)
- `input_ref` (text, nullable)
- `input_hash` (text, nullable)
- `config_json` (jsonb, not null)
- `config_hash` (text, nullable)
- `seed` (int, nullable)
- `error_code` (text, nullable)
- `error_detail` (text, nullable)
- `created_at` (timestamp with tz)
- `started_at` (timestamp with tz, nullable)
- `finished_at` (timestamp with tz, nullable)

Indexes:
- index on `status`
- index on `created_at desc`
- index on `(created_by, created_at desc)`

## `run_metrics`

- `id` (PK, bigserial)
- `run_id` (FK -> runs.id, not null)
- `metric_name` (text, not null)
- `metric_value` (numeric, not null)
- `metric_group` (text, nullable)
- `created_at` (timestamp with tz)

Indexes:
- index on `run_id`
- index on `(metric_name, created_at desc)`

## `artifacts`

- `id` (PK, bigserial)
- `run_id` (FK -> runs.id, not null)
- `artifact_type` (text, not null)
- `path_or_uri` (text, not null)
- `checksum` (text, nullable)
- `size_bytes` (bigint, nullable)
- `created_at` (timestamp with tz)

Indexes:
- index on `run_id`
- index on `artifact_type`

## `audit_logs` (แนะนำเพิ่มใน MVP)

- `id` (PK, bigserial)
- `user_id` (FK -> users.id, nullable สำหรับ system events)
- `action` (text, not null) เช่น `create_run`, `view_run`, `download_artifact`
- `resource_type` (text, not null)
- `resource_id` (text, nullable)
- `metadata_json` (jsonb, nullable)
- `created_at` (timestamp with tz)

Indexes:
- index on `(user_id, created_at desc)`
- index on `(resource_type, resource_id)`

---

## 4) Status Transition Rules

`runs.status` transition ที่อนุญาต:

- `queued -> running`
- `running -> succeeded`
- `running -> failed`
- `queued -> cancelled`
- `running -> cancelled` (กรณีรองรับ cancel)

สถานะอื่นที่ผิดกฎต้อง reject ด้วย conflict (409)

---

## 5) Migration Strategy

1. Initial migration: สร้าง 5 ตารางหลัก + indexes
2. Seed migration: เพิ่ม admin user เริ่มต้น (เฉพาะ dev/staging)
3. Backward-compatible changes only ระหว่าง MVP (หลีกเลี่ยง breaking migration)

---

## 6) Data Retention (MVP)

- เก็บ metadata runs อย่างน้อย 90 วัน
- artifacts อาจทำ retention policy 30-90 วันตามพื้นที่
- audit_logs เก็บตามนโยบายความปลอดภัยภายในองค์กร

---

## 7) Future Extensions (Post-MVP)

- ตาราง model registry / model versions
- ตาราง dataset registry
- ตาราง experiment tags และ lineage graph
- row-level security สำหรับ multi-tenant
