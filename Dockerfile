# ใช้ Python เวอร์ชัน 3.9 แบบ slim เป็น base image
FROM python:3.9-slim

# กำหนด working directory ภายใน container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt เข้าไปใน container
COPY requirements.txt .

# ติดตั้ง library ที่ระบุใน requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์ทั้งหมดจาก current directory (ในเครื่องคุณ) ไปยัง /app (ใน container)
COPY . .

# กำหนด port ที่ app จะรัน
EXPOSE 5000

# กำหนดคำสั่งที่จะรันเมื่อ container ถูกสร้าง
CMD ["python", "app.py"]