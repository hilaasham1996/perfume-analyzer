# Perfume Analyzer — نسخه Render-ready

این پروژه یک وب‌اپ ساده است که:

- ادکلن‌های مورد علاقه یا نت‌ها را تحلیل می‌کند
- پروفایل رایحه و پیشنهادات ادکلن مشابه را نمایش می‌دهد
- UI پاستلی مدرن (سبک C) و RTL فارسی
- آماده دیپلوی روی Render (Static + Backend)

## 🖥️ مراحل سریع دیپلوی

### 1️⃣ نصب GitHub و Personal Access Token
1. اگر حساب GitHub نداری: https://github.com/signup
2. ایجاد یک Personal Access Token:
   - Settings → Developer settings → Personal Access Tokens → Fine-grained tokens → Generate new
   - حداقل دسترسی: repo (تمامی ریپوهای عمومی و خصوصی)
3. در سیستم:
```bash
export GITHUB_TOKEN=YOUR_TOKEN_HERE
```

### 2️⃣ اجرای deploy.sh
```bash
chmod +x deploy.sh
./deploy.sh
```
این اسکریپت:
- ریپوی `perfume-analyzer` در GitHub می‌سازد
- پروژه را push می‌کند
- آماده اتصال به Render می‌کند

### 3️⃣ دیپلوی روی Render
1. به https://render.com/dashboard/new برو
2. گزینه **Web Service** برای Backend:
   - Repository: `hilaasham1996/perfume-analyzer`
   - Branch: main
   - Dockerfile Path: backend/Dockerfile
3. گزینه **Static Site** برای Frontend:
   - Repository: همان
   - Branch: main
   - Static Publish Path: frontend
4. دکمه Deploy را بزن → سایت بالا می‌آید

### 4️⃣ تست
- Backend: `https://<your-backend>.onrender.com/api/analyze`
- Frontend: `https://<your-frontend>.onrender.com/`

### نکات
- تمام UI به زبان فارسی و RTL است
- اگر می‌خوای ادکلن جدید اضافه کنی، دیتابیس SQLite در `backend/data/perfumes.db` را ویرایش کن

---

**UI:** پاستلی مدرن، سبک C — مناسب پیج‌های اینستاگرامی
