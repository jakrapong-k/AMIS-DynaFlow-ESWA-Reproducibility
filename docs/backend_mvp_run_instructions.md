# Backend MVP Skeleton Run Instructions (Phase 3)

เอกสารนี้อธิบายวิธีรัน backend/API skeleton ที่สร้างเพื่อการทดลองพัฒนา MVP โดย **ไม่มีการเชื่อมต่อข้อมูลจริง** และ **ไม่มีการใช้ข้อมูลโรงพยาบาลจริง**

## 1) ติดตั้ง dependencies

```bash
pip install -r requirements.txt
```

## 2) เตรียม environment variables

```bash
cp backend/.env.example .env
```

> ค่าใน `.env.example` เป็น placeholder เท่านั้น ไม่ใช่ secret สำหรับ production

## 3) รัน FastAPI server

```bash
uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8000
```

## 4) ตรวจสอบ endpoint พื้นฐาน

- Health: `GET http://localhost:8000/api/v1/health`
- OpenAPI docs: `http://localhost:8000/docs`

## 5) รันทดสอบ

```bash
PYTHONPATH=backend pytest backend/tests -q
```

## 6) ขอบเขตความสามารถของ skeleton

- มี API routes ตาม `docs/api_design.md` ในรูปแบบ mock/stub
- มี placeholder models ตาม `docs/database_schema.md`
- ยังไม่เชื่อมต่อ PostgreSQL/Redis จริง
- ยังไม่เชื่อม worker queue จริง
- ยังไม่มี credential จริง และไม่ใช้งานข้อมูลจริง
