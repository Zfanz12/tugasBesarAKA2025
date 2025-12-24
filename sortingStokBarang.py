import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt
import sys
import random

# config
sys.setrecursionlimit(2000)

data_barang = []
hasil_eksekusi = {"Iteratif": {}, "Rekursif": {}}

# --- ALGORITMA BUBBLE SORT ---
def bubble_sort_iteratif(data):
    n = len(data)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if data[j][1] > data[j + 1][1]:
                data[j], data[j + 1] = data[j + 1], data[j]

def bubble_sort_rekursif(data, n):
    if n <= 1:
        return
    for i in range(n - 1):
        if data[i][1] > data[i + 1][1]:
            data[i], data[i + 1] = data[i + 1], data[i]
    bubble_sort_rekursif(data, n - 1)

# --- UTILITY ---
def numeric(P):
    return P.isdigit() or P == ""

def update_tabel(data):
    tabel.delete(*tabel.get_children())
    for item in data:
        tabel.insert("", "end", values=item)

# --- ACTION ---
def tambah_data():
    try:
        nama = entry_nama.get()
        stok_str = entry_stok.get()
        if not nama or not stok_str:
            raise ValueError
        
        stok = int(stok_str)
        data_barang.append((nama, stok))
        tabel.insert("", "end", values=(nama, stok))
        entry_nama.delete(0, tk.END)
        entry_stok.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Isi Nama dan Stok (angka) dengan benar!")

def barang_random(jumlah=10):
    for _ in range(jumlah):
        nama = f"Barang-{len(data_barang) + 1}"
        stok = random.randint(1, 100)
        data_barang.append((nama, stok))
        tabel.insert("", "end", values=(nama, stok))

def sort_iteratif():
    if not data_barang: return
    data = list(data_barang)
    start = time.perf_counter_ns()
    bubble_sort_iteratif(data)
    waktu = time.perf_counter_ns() - start
    update_tabel(data)
    hasil_eksekusi["Iteratif"][len(data)] = waktu

def sort_rekursif():
    if not data_barang: return
    data = list(data_barang)
    try:
        start = time.perf_counter_ns()
        bubble_sort_rekursif(data, len(data))
        waktu = time.perf_counter_ns() - start
        update_tabel(data)
        hasil_eksekusi["Rekursif"][len(data)] = waktu
    except RecursionError:
        messagebox.showerror("Error", "Limit rekursi terlampaui!")

def tampilkan_grafik():
    plt.figure(figsize=(10, 5))
    for label, points in hasil_eksekusi.items():
        if points:
            n = sorted(points.keys())
            waktu = [points[i] for i in n]
            plt.plot(n, waktu, marker='o', label=label)
    plt.xlabel("Ukuran Input (n)")
    plt.ylabel("Waktu Eksekusi (ns)")
    plt.title("Perbandingan Bubble Sort")
    plt.legend()
    plt.grid(True)
    plt.show()

def reset_data():
    if not messagebox.askyesno("Konfirmasi", "Reset semua data?"):
        return
    data_barang.clear()
    hasil_eksekusi["Iteratif"].clear()
    hasil_eksekusi["Rekursif"].clear()
    tabel.delete(*tabel.get_children())

# --- WINDOW SETUP ---
root = tk.Tk()
root.title("Manajemen Stok Barang - Analisis Algoritma")

# Ukuran window lebih lebar untuk mengakomodasi tabel di kanan
LEBAR, TINGGI = 900, 500 
x = (root.winfo_screenwidth() - LEBAR) // 2
y = (root.winfo_screenheight() - TINGGI) // 2
root.geometry(f"{LEBAR}x{TINGGI}+{x}+{y}")

# --- CONTAINER UTAMA (SPLIT KIRI & KANAN) ---
frame_kiri = tk.Frame(root, width=350, padx=10, pady=10)
frame_kiri.pack(side="left", fill="y")

frame_kanan = tk.Frame(root, padx=10, pady=10)
frame_kanan.pack(side="right", fill="both", expand=True)

# --- ISI FRAME KIRI (KONTROL) ---
# Bagian Input
frame_input = tk.LabelFrame(frame_kiri, text=" Input Data ", padx=10, pady=10)
frame_input.pack(fill="x", pady=5)

vcmd = (root.register(numeric), "%P")

tk.Label(frame_input, text="Nama Barang").grid(row=0, column=0, sticky="w", pady=2)
entry_nama = tk.Entry(frame_input, width=25)
entry_nama.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_input, text="Stok").grid(row=1, column=0, sticky="w", pady=2)
entry_stok = tk.Entry(frame_input, width=25, validate="key", validatecommand=vcmd)
entry_stok.grid(row=1, column=1, padx=5, pady=2)

tk.Button(frame_input, text="Tambah ke Tabel", width=25, command=tambah_data, bg="#e1e1e1")\
    .grid(row=2, columnspan=2, pady=10)
tk.Button(frame_input, text="Tambah 10 Data Random", width=25, command=barang_random)\
    .grid(row=3, columnspan=2)

# Bagian Tombol Sorting
frame_aksi = tk.LabelFrame(frame_kiri, text=" Eksekusi Algoritma ", padx=10, pady=10)
frame_aksi.pack(fill="x", pady=10)

tk.Button(frame_aksi, text="Sort Iteratif", width=11, command=sort_iteratif, bg="#d4edda")\
    .grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_aksi, text="Sort Rekursif", width=11, command=sort_rekursif, bg="#d1ecf1")\
    .grid(row=0, column=1, padx=5, pady=5)

# Bagian Tombol Bawah
tk.Button(frame_kiri, text="Tampilkan Grafik Perbandingan", width=30, height=2,
          bg="#add8e6", command=tampilkan_grafik).pack(pady=5)
tk.Button(frame_kiri, text="Reset Semua Data", width=30,
          bg="#f08080", command=reset_data).pack(pady=5)

# --- ISI FRAME KANAN (TABEL BESAR) ---
tk.Label(frame_kanan, text="Daftar Stok Barang", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)

tabel_container = tk.Frame(frame_kanan)
tabel_container.pack(fill="both", expand=True)

tabel = ttk.Treeview(tabel_container, columns=("Nama", "Stok"), show="headings")
tabel.heading("Nama", text="Nama Barang")
tabel.heading("Stok", text="Jumlah Stok")
tabel.column("Nama", anchor="center")
tabel.column("Stok", anchor="center", width=100)

scrollbar = ttk.Scrollbar(tabel_container, orient="vertical", command=tabel.yview)
tabel.configure(yscrollcommand=scrollbar.set)

tabel.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()