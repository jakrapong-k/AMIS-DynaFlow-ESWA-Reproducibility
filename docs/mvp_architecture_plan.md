# MVP Architecture Plan (Phase 2)

## 1) Objective

เอกสารนี้กำหนดสถาปัตยกรรมเป้าหมายสำหรับ Phase 2 เพื่อเปลี่ยน repository จาก reproducibility workflow ไปสู่ **MVP App ทดลองใช้งานจริง** โดยเน้นการใช้งานภายในทีมแบบปลอดภัย ติดตามงานได้ และรัน pipeline ได้ end-to-end

---

## 2) Scope ของ MVP

MVP จะครอบคลุมความสามารถต่อไปนี้:

1. ผู้ใช้ล็อกอินเข้าใช้งานระบบได้
2. ผู้ใช้ส่งงานรัน (forecast/optimize/adapt schedule) ผ่าน UI ได้
3. ระบบรันงานแบบ asynchronous และติดตามสถานะได้
4. ผู้ใช้ดูผลลัพธ์ KPI และดาวน์โหลด artifacts ได้
5. ระบบมีบันทึก trace ขั้นต่ำของ run metadata และ audit

> นอก scope ของ MVP: multi-tenant เต็มรูปแบบ, autoscaling ขั้นสูง, model registry เต็มระบบ, drift monitoring ขั้น production

---

## 3) Target Architecture (MVP)

```text
[Frontend: Next.js/React]
        |
        v
[Backend API: FastAPI]
   |        |          \
   |        |           \-- [Redis: Queue/Cache]
   |        \-- [Worker: Celery/RQ]
   |
   \-- [PostgreSQL: users/runs/metrics/artifacts]
   
Artifacts -> local filesystem (MVP) / object storage (future)
```

### Components

- **Frontend**
  - หน้าจอ Login, New Run, Run List, Run Detail, Dashboard
- **Backend API**
  - REST API สำหรับ auth, run orchestration, metrics และ artifacts
- **Worker**
  - ทำงานหนัก (optimization/adaptation) แบบ async
- **PostgreSQL**
  - เก็บ metadata, status transition, metrics index
- **Redis**
  - broker สำหรับ queue และ caching สั้น
- **Artifact storage**
  - เริ่มด้วย local path มาตรฐานใน `results/` และรองรับการย้ายไป object storage ภายหลัง

---

## 4) Data & Execution Flow

1. ผู้ใช้ล็อกอิน → ได้ access token
2. ผู้ใช้สร้าง run จากหน้า New Run (พร้อม config/input)
3. API ตรวจ validation แล้วสร้าง `run_id` + บันทึกสถานะ `queued`
4. Worker ดึงงานไปประมวลผล → อัปเดตสถานะ `running`
5. เมื่อเสร็จงาน บันทึก metrics/artifacts + สถานะ `succeeded` หรือ `failed`
6. Frontend polling ข้อมูล run detail/dashboard เพื่อแสดงผลล่าสุด

---

## 5) Non-functional Requirements (MVP baseline)

- **Traceability**: ทุก run ต้องผูกกับ user, seed, config hash, timestamps
- **Reliability**: มี retry policy ขั้นต่ำของ queue job
- **Security**: protected endpoints ทั้งหมด ยกเว้น auth health
- **Observability**: structured logs พร้อม run_id
- **Portability**: รันผ่าน docker-compose ได้ทั้งเครื่อง dev และ staging

---

## 6) Risks & Mitigations

1. **Pipeline เดิมเป็น file-based สูง**
   - Mitigation: เพิ่ม orchestration service layer ใน API แทนเรียก scripts แบบไร้โครง
2. **งาน optimization ใช้เวลานาน**
   - Mitigation: บังคับ async + timeout + cancellation state
3. **test coverage ต่ำ**
   - Mitigation: เพิ่ม integration/e2e smoke ก่อนเปิดทดลองจริง

---

## 7) Phase 2 Delivery Milestones

### Milestone A: Foundation
- API scaffold + DB migrations + queue + auth baseline

### Milestone B: Usable MVP
- Frontend flow ครบ login → submit run → track status → ดู metrics

### Milestone C: Stabilization
- docker-compose deploy flow + regression tests + release checklist

---

## 8) Definition of Done (Phase 2)

ถือว่า MVP พร้อมทดลองใช้งานจริงเมื่อ:

1. ผู้ใช้ภายในล็อกอินและสั่ง run ใหม่ได้เองผ่าน UI
2. ระบบแสดง run lifecycle: queued/running/succeeded/failed ได้ถูกต้อง
3. metrics และ artifacts เข้าถึงได้จากหน้า run detail
4. มี log/audit ขั้นต่ำสำหรับการตรวจย้อนหลัง
5. deploy staging ได้ด้วยเอกสารและคำสั่งที่ทำซ้ำได้
