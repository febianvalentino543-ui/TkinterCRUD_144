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

