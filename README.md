โปรเจกต์เว็บแอปพลิเคชันจัดการภาพยนตร์
โปรเจกต์นี้คือเว็บแอปพลิเคชันขนาดเล็กที่พัฒนาด้วย Flask, MongoDB และ Docker เพื่อจัดการและแสดงข้อมูลภาพยนตร์ โดยสามารถดึงข้อมูลภาพยนตร์จาก TMDb API ได้

คุณสมบัติหลัก
แสดงข้อมูลทีมงานผู้พัฒนา

สามารถเพิ่มภาพยนตร์ใหม่ลงในฐานข้อมูล MongoDB

ดึงข้อมูลภาพยนตร์ (เช่น ชื่อเรื่อง, ปีที่ฉาย, โปสเตอร์, คะแนน) จาก TMDb API โดยอัตโนมัติ

แสดงรายการภาพยนตร์ที่เพิ่มเข้ามา

เทคโนโลยีที่ใช้
Flask: Web framework สำหรับ Python

MongoDB: NoSQL database สำหรับจัดเก็บข้อมูลภาพยนตร์

Docker / Docker Compose: สำหรับการจัดสภาพแวดล้อมการพัฒนาและการรันแอปพลิเคชันและฐานข้อมูลใน Container

Python: ภาษาโปรแกรมหลัก

TMDb API: สำหรับดึงข้อมูลภาพยนตร์

การตั้งค่าและการเรียกใช้งานสำหรับนักพัฒนา
ทำตามขั้นตอนต่อไปนี้เพื่อเรียกใช้โปรเจกต์บนเครื่องของคุณ:

1. ติดตั้ง Docker และ Docker Compose
โปรเจกต์นี้ใช้ Docker และ Docker Compose เพื่อจัดการสภาพแวดล้อมและฐานข้อมูล หากคุณยังไม่ได้ติดตั้ง โปรดทำตามคำแนะนำอย่างเป็นทางการที่นี่:

ติดตั้ง Docker

ติดตั้ง Docker Compose

2. โคลน Repository
เปิด Terminal หรือ Command Prompt แล้วโคลนโปรเจกต์นี้จาก GitHub:

git clone https://github.com/babephasuk/movie.git
cd movie/CT519

หมายเหตุ: โฟลเดอร์ CT519 คือโฟลเดอร์หลักของโปรเจกต์

3. รับ API Key จาก TMDb
โปรเจกต์นี้จำเป็นต้องใช้ API Key จาก The Movie Database (TMDb) เพื่อดึงข้อมูลภาพยนตร์:

ไปที่ https://www.themoviedb.org/ และเข้าสู่ระบบ (หากยังไม่มีบัญชี โปรดลงทะเบียน)

เข้าสู่ระบบแล้วไปที่ Settings (การตั้งค่าบัญชี)

ในเมนูด้านซ้าย เลือก API

เลือก Developer แล้วอ่านข้อตกลงและกรอกข้อมูลเพื่อขอ API Key

คุณจะได้รับ API Key (v3 auth) คัดลอก Key นี้เก็บไว้

4. ตั้งค่า API Key ใน app.py
เปิดไฟล์ app.py ที่อยู่ในโฟลเดอร์ CT519 ด้วย Text Editor (เช่น nano, VS Code, Sublime Text)
ค้นหาบรรทัด TMDB_API_KEY และแทนที่ YOUR_TMDB_API_KEY ด้วย Key ที่คุณได้รับจาก TMDb:

# app.py
TMDB_API_KEY = 'YOUR_TMDB_API_KEY' # เปลี่ยน YOUR_TMDB_API_KEY เป็น Key ของคุณ

บันทึกการเปลี่ยนแปลงในไฟล์ app.py

5. เรียกใช้งานด้วย Docker Compose
ใน Terminal/Command Prompt ตรวจสอบให้แน่ใจว่าคุณอยู่ในโฟลเดอร์ CT519 (ที่ไฟล์ docker-compose.yaml และ Dockerfile อยู่) จากนั้นรันคำสั่งต่อไปนี้:

sudo docker compose up -d --build

sudo: ใช้สิทธิ์ผู้ดูแลระบบ (สำหรับ Linux/macOS)

up: สร้างและเริ่มต้นบริการทั้งหมดที่กำหนดไว้ใน docker-compose.yaml

-d: รัน Container ในโหมด "detached" (ทำงานอยู่เบื้องหลัง)

--build: บังคับให้ Docker สร้าง Docker Image ใหม่สำหรับแอปพลิเคชันของคุณ ซึ่งจำเป็นเมื่อมีการเปลี่ยนแปลงโค้ดหรือไฟล์ requirements.txt

6. เข้าถึงเว็บแอปพลิเคชัน
เมื่อ Docker Container ทั้งหมด (เว็บแอปและฐานข้อมูล MongoDB) รันขึ้นมาเรียบร้อยแล้ว คุณสามารถเปิดเว็บเบราว์เซอร์และเข้าถึงเว็บแอปพลิเคชันได้ที่:

http://localhost:5000

ตอนนี้คุณควรจะเห็นหน้าเว็บแอปพลิเคชันแสดงผลและสามารถใช้งานได้ตามปกติ

โครงสร้างโปรเจกต์
CT519/
├── app.py                      # โค้ด Flask Application หลัก
├── docker-compose.yaml         # ไฟล์กำหนด Docker services (Flask app และ MongoDB)
├── Dockerfile                  # ไฟล์สำหรับสร้าง Docker Image ของ Flask app
├── requirements.txt            # รายการไลบรารี Python ที่จำเป็น
├── static/                     # โฟลเดอร์สำหรับไฟล์ Static (CSS, JavaScript, รูปภาพ)
│   ├── profile1.jpg            # รูปภาพโปรไฟล์สมาชิก 1
│   └── profile2.jpg            # รูปภาพโปรไฟล์สมาชิก 2
└── templates/                  # โฟลเดอร์สำหรับไฟล์ HTML templates
    └── index.html              # หน้าหลักของเว็บแอปพลิเคชัน

ผู้พัฒนา
[พีระภัทร์ ผาสุข]
