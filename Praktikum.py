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


