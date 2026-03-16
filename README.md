# ⚡ AI Complete Landscape 2026

ภาพรวมครบทุกหมวดของ AI ใน 5 ระดับ — กด card สีม่วงเพื่อใช้งานผ่าน Claude API ได้เลย

## 📊 สถิติ
- **5** ระดับหลัก (Tier 1–5)
- **44** หมวดย่อย
- **10** tool ใช้งานได้เลยผ่าน Claude
- **150+** เครื่องมือในตลาด

## 🏗️ โครงสร้างโปรเจกต์

```
ai_landscape/
├── app.py                    # Main Streamlit app
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml           # Dark theme config
├── data/
│   └── tools.py              # Tool registry & metadata
├── services/
│   └── claude_service.py     # Anthropic API integration
└── components/
    └── ui.py                 # Reusable UI components
```

## 🚀 Deploy บน Streamlit Cloud (Step-by-Step)

### Step 1 — Push ขึ้น GitHub

```bash
# สร้าง repo ใหม่บน GitHub ก่อน แล้วรัน:
git init
git add .
git commit -m "Initial commit: AI Landscape 2026"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-landscape.git
git push -u origin main
```

### Step 2 — Deploy บน Streamlit Cloud

1. ไปที่ [share.streamlit.io](https://share.streamlit.io)
2. กด **"New app"**
3. เลือก GitHub repo ที่ push ไว้
4. ตั้งค่า:
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. กด **"Deploy!"**

### Step 3 — ตั้งค่า (ไม่บังคับ)

API Key จะถูกใส่โดย user เองผ่าน UI — ไม่จำเป็นต้อง set Secrets

แต่ถ้าต้องการ hardcode key (สำหรับ internal use):
1. ใน Streamlit Cloud → Settings → **Secrets**
2. เพิ่ม:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

## 💻 รันในเครื่อง

```bash
# 1. ติดตั้ง dependencies
pip install -r requirements.txt

# 2. รัน app
streamlit run app.py

# เปิด browser ที่ http://localhost:8501
```

## 🔑 วิธีใช้งาน

1. ใส่ Anthropic API key ใน Sidebar (`sk-ant-...`)
2. กด **"บันทึก Key"** — ระบบจะ validate ให้อัตโนมัติ
3. กด card สีม่วงไหนก็ได้
4. พิมพ์ prompt หรือเลือก template → กด "ส่ง →"

## 🛠️ Tech Stack

- **Frontend:** Streamlit 1.35+
- **AI:** Anthropic Claude (claude-sonnet-4-5)
- **Language:** Python 3.10+
- **Deploy:** Streamlit Cloud (free tier)

---
*สร้างโดย Claude Sonnet · Anthropic · March 2026*
