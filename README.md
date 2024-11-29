<div align="center">
  <img src="https://github.com/user-attachments/assets/c3a01c19-e57e-48eb-8c20-19d0f94804eb" alt="Desain tanpa judul" width="300">
</div>


---

## 🌟 **Pendahuluan**

Selamat datang di repositori **MindSphere**!  
MindSphere adalah sebuah platform untuk mempermudah proses pembookingan jadwal tes psikologi, serta memberikan akses kepada pengguna untuk melihat hasil tes yang telah dilakukan secara offline. Website ini dirancang untuk meningkatkan efisiensi layanan psikologi dengan tampilan responsive yang mudah digunakan dan fitur-fitur fungsional.

---

## ✨ **Fitur Utama**

### **Untuk Pengguna**  
- **Pendaftaran Akun**: Pengguna dapat membuat akun untuk mengakses layanan platform.
- **Pendaftaran Tes Psikologi**: Daftar untuk mengikuti tes psikologi secara online.  
- **Melihat Hasil Tes**: Akses hasil tes secara langsung di dashboard.  
- **Download Sertifikat**: Unduh sertifikat hasil tes dalam format PDF.  

### **Untuk Staf Psikolog**  
- **Penilaian Tes Peserta**: Memberikan hasil penilaian terhadap tes peserta.  

### **Untuk Admin**  
- **Manajemen Jadwal Tes**: Membuat dan mengelola jadwal tes psikologi.  
- **Pembuatan Akun Psikolog**: Menambahkan akun staf psikolog untuk memberikan penilaian.  

---

## 🛠 **Teknologi yang Digunakan**

- **Frontend:** CSS, JavaScript, Bootstrap, jQuery, AG Grid, SweetAlert2
- **Backend:** Django
- **Database:** MariaDB
- **Cloud:** 

---
 
## 🚀 **Cara Menjalankan Project**
*follow the command below with your terminal/cmd/git bash*

- Clone project

```bash
git clone https://github.com/Anhar12/MindSphere.git
```
- Change Directory to MindSphere

```bash
cd MindSphere
```
- Install pipenv (if not installed)

```bash
pip install pipenv
```
- Install all dependencies & enter pipenv virtual environment

```bash
pipenv shell
pipenv install
```
- Migration

```bash
py manage.py makemigrations
py manage.py migrate
```

- Run this project

```bash
cd MindSphere
py manage.py runserver
```
