import tkinter as tk
from tkinter import messagebox 
import sqlite3

DB_Name = "Sekolah.db"

# ================ DATA LAYER =====================
def run_query(sql, params=()):
    conn = sqlite3.connect(DB_Name)
    try:
        with conn:
            return conn.execute(sql, params).fetchall()
    finally:
        conn.close()

def init_db():
    run_query("""CREATE TABLE IF NOT EXISTS Nilai_Siswa (
        Nama_siswa TEXT PRIMARY KEY,
        Biologi INTEGER NOT NULL,
        Fisika INTEGER NOT NULL,
        Inggris INTEGER NOT NULL,
        Prediksi_Fakultas TEXT)""")


def add_nilai(nama, biologi, fisika, inggris, prediksi):
    run_query("""INSERT INTO Nilai_Siswa
                 (Nama_siswa, Biologi, Fisika, Inggris, Prediksi_Fakultas)
                 VALUES (?, ?, ?, ?, ?)""",
              (nama, biologi, fisika, inggris, prediksi))

def get_nilai():
    return run_query("""SELECT Nama_siswa, Biologi, Fisika, Inggris, Prediksi_Fakultas
                        FROM Nilai_Siswa ORDER BY Nama_siswa""")

def tentukan_prediksi(biologi, fisika, inggris):
    if biologi >= fisika and biologi >= inggris:
        return "Kedokteran"     
    elif fisika >= inggris:
        return "Teknik"         
    else:
        return "Bahasa"         


# ============== membuat window =====================
init_db()

root = tk.Tk()
root.title("Aplikasi Nilai Siswa")
root.geometry("400x500")

# Judul aplikasi
judul = tk.Label(
    root,
    text="Aplikasi Nilai Siswa",
    font=("Times New Roman", 14)
)
judul.pack(pady=10)

# tempat masukkan nama siswa
frame_nama = tk.Frame(root)
frame_nama.pack(pady=3)

label_nama = tk.Label(frame_nama, text="Nama Siswa", width=20, anchor="w")
label_nama.pack(side="left")

entry_nama = tk.Entry(frame_nama, width=15)
entry_nama.pack(side="left")

# Daftar mata pelajaran (urutan disamakan dengan soal)
mapel = [
    "Biologi",
    "Fisika",
    "Inggris",
]

# dengan nama mapel: input_nilai["Biologi"]
input_nilai = {}

for nama in mapel:
    frame = tk.Frame(root)
    frame.pack(pady=3)

    label = tk.Label(frame, text=nama, width=20, anchor="w")
    label.pack(side="left")

    entry = tk.Entry(frame, width=15)
    entry.pack(side="left")

    input_nilai[nama] = entry

#  validasi -> prediksi -> simpan
def submit_nilai():
    nama = entry_nama.get().strip()
    biologi = input_nilai["Biologi"].get().strip()
    fisika = input_nilai["Fisika"].get().strip()
    inggris = input_nilai["Inggris"].get().strip()

    # 1. Validasi input
    if not nama or not biologi or not fisika or not inggris:
        messagebox.showwarning("Data kurang", "Semua kolom harus diisi.")
        return
    if not (biologi.isdigit() and fisika.isdigit() and inggris.isdigit()):
        messagebox.showwarning("Nilai salah", "Nilai harus berupa angka.")
        return

    biologi, fisika, inggris = int(biologi), int(fisika), int(inggris)
    if max(biologi, fisika, inggris) > 100:
        messagebox.showwarning("Nilai salah", "Nilai maksimal 100.")
        return

    # 2. Tentukan prediksi
    prediksi = tentukan_prediksi(biologi, fisika, inggris)

    # 3. Simpan ke database
    try:
        add_nilai(nama, biologi, fisika, inggris, prediksi)
    except sqlite3.IntegrityError:
        messagebox.showwarning("Nama sudah ada", "Nama siswa ini sudah tersimpan.")
        return

    # 4. Tampilkan hasil, lalu kosongkan form
    hasil.config(text=f"Hasil Prediksi: {prediksi}")
    entry_nama.delete(0, tk.END)
    for e in input_nilai.values():
        e.delete(0, tk.END)

# Tombol submit
tombol = tk.Button(
    root,
    text="Submit Nilai",
    command=submit_nilai
)
tombol.pack(pady=10)

# Menampilkan hasil
hasil = tk.Label(root, text="Hasil Prediksi: -")
hasil.pack()

# Menjalankan aplikasi
root.mainloop()