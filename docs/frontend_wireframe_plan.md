# Frontend Wireframe Plan for MVP App (Phase 2)

## 1) Goal

กำหนด wireframe และ user flow สำหรับหน้าเว็บ MVP ที่รองรับการทดลองใช้งานจริงของทีมปฏิบัติการ โดยเน้นงานหลัก: login, สร้าง run, ติดตามสถานะ, และดูผลลัพธ์

---

## 2) Primary Personas

1. **Operator**: ส่งงานและติดตามผล
2. **Viewer**: ดูผลลัพธ์และ dashboard
3. **Admin**: ดูแลสิทธิ์และตรวจ audit (MVP อาจยังไม่มี admin UI ครบ)

---

## 3) Navigation Structure

เมนูหลัก:

- Dashboard
- New Run
- Run History
- Run Detail (dynamic route)
- Login / Logout

Layout มาตรฐาน:
- Top bar: app name + user menu
- Left navigation (desktop) / drawer (mobile)
- Main content area

---

## 4) Wireframe Screens

## A) Login Page

องค์ประกอบ:
- Email input
- Password input
- Login button
- Error message area

Acceptance:
- Login สำเร็จ redirect ไป Dashboard
- Login ล้มเหลวแสดงข้อความชัดเจน

## B) Dashboard Page

องค์ประกอบ:
- KPI cards: total runs, success rate, avg runtime, active runs
- Recent runs table (run_id, status, created_at, owner)
- Mini trend chart (runs/day)

Acceptance:
- รองรับ loading/empty/error state
- กด row เพื่อไปหน้า Run Detail

## C) New Run Page

องค์ประกอบ:
- Run type selector (`forecast_only`, `optimize_only`, `full_pipeline`)
- Input reference/file upload field
- Config section (seed, profile, optional overrides)
- Submit button

UX states:
- Form validation inline
- Submit success modal (show run_id)
- Submit error banner

Acceptance:
- Submit แล้วไปหน้า Run Detail ของ run ที่สร้าง

## D) Run History Page

องค์ประกอบ:
- Filter bar (status/date/user)
- Run table พร้อม pagination
- Quick action: open detail

Acceptance:
- filter และ pagination ทำงานถูกต้อง

## E) Run Detail Page

องค์ประกอบ:
- Header: run_id + status badge
- Timeline: created/start/finish
- Config summary + input hash
- Metrics table / chart
- Artifact list + download links
- Error panel (แสดงเมื่อ failed)

Acceptance:
- auto refresh สถานะขณะ queued/running
- สถานะ succeeded/failed แสดงครบพร้อมเหตุผล

---

## 5) Component Plan (MVP)

Reusable components:
- `StatusBadge`
- `KpiCard`
- `RunTable`
- `MetricsTable`
- `ArtifactList`
- `PageState` (loading/empty/error)

---

## 6) API Binding Plan

- Login page → `POST /api/v1/auth/login`
- New Run page → `POST /api/v1/runs`
- Run History page → `GET /api/v1/runs`
- Run Detail page → `GET /api/v1/runs/{id}`, `/metrics`, `/artifacts`
- Dashboard page → `GET /api/v1/dashboard/summary`, `/trends`

---

## 7) Non-functional UX Requirements

- Time-to-interactive หน้า dashboard < 3 วินาทีใน dev dataset
- Error message ต้อง actionable (เช่น token หมดอายุ, validation fail)
- Mobile responsive ขั้นพื้นฐาน (tablet-first)
- ใช้ design token เดียวกันเพื่อขยายผลหลัง MVP

---

## 8) Frontend Delivery Sequence

1. Auth guard + routing skeleton
2. Dashboard + Run History read-only
3. New Run form + submit flow
4. Run Detail + polling status
5. UI polish + empty/error states + accessibility pass
