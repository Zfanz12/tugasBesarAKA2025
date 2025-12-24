import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt
import sys
import random

# --- CONFIG ---
# Meningkatkan limit rekursi untuk testing Bubble Sort Rekursif
sys.setrecursionlimit(5000)

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

def barang_random():
    try:
        n_input = entry_n_random.get()
        if not n_input:
            raise ValueError
            
        jumlah = int(n_input)
        for _ in range(jumlah):
            nama = f"Barang-{len(data_barang) + 1}"
            stok = random.randint(1, 500)
            data_barang.append((nama, stok))
            tabel.insert("", "end", values=(nama, stok))
            
        entry_n_random.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Masukkan jumlah data (n) yang valid!")

def sort_iteratif():
    if not data_barang: return
    data = list(data_barang)
    start = time.perf_counter_ns()
    bubble_sort_iteratif(data)
    waktu = time.perf_counter_ns() - start
    update_tabel(data)
    hasil_eksekusi["Iteratif"][len(data)] = waktu
    messagebox.showinfo("Sukses", f"Sorting Iteratif Selesai!\nWaktu: {waktu} ns")

def sort_rekursif():
    if not data_barang: return
    data = list(data_barang)
    try:
        start = time.perf_counter_ns()
        bubble_sort_rekursif(data, len(data))
        waktu = time.perf_counter_ns() - start
        update_tabel(data)
        hasil_eksekusi["Rekursif"][len(data)] = waktu
        messagebox.showinfo("Sukses", f"Sorting Rekursif Selesai!\nWaktu: {waktu} ns")
    except RecursionError:
        messagebox.showerror("Error", "Limit rekursi terlampaui! Kurangi jumlah data.")

def tampilkan_grafik():
    if not hasil_eksekusi["Iteratif"] and not hasil_eksekusi["Rekursif"]:
        messagebox.showwarning("Peringatan", "Lakukan sorting terlebih dahulu untuk melihat data!")
        return
        
    plt.figure(figsize=(10, 6))
    for label, points in hasil_eksekusi.items():
        if points:
            n_vals = sorted(points.keys())
            waktu_vals = [points[i] for i in n_vals]
            plt.plot(n_vals, waktu_vals, marker='o', label=f"Bubble Sort {label}")

    plt.xlabel("Ukuran Input (n)")
    plt.ylabel("Waktu Eksekusi (nanoseconds)")
    plt.title("Analisis Kompleksitas Bubble Sort")
    plt.legend()
    plt.grid(True)
    plt.show()

def reset_data():
    if not messagebox.askyesno("Konfirmasi", "Reset semua data dan riwayat analisis?"):
        return
    data_barang.clear()
    hasil_eksekusi["Iteratif"].clear()
    hasil_eksekusi["Rekursif"].clear()
    tabel.delete(*tabel.get_children())

# --- WINDOW SETUP ---
root = tk.Tk()
root.title("Tubes AKA 2025 - Analisis Kompleksitas Algoritma")

LEBAR, TINGGI = 1000, 550 
x = (root.winfo_screenwidth() - LEBAR) // 2
y = (root.winfo_screenheight() - TINGGI) // 2
root.geometry(f"{LEBAR}x{TINGGI}+{x}+{y}")

vcmd = (root.register(numeric), "%P")

# --- LAYOUTING ---
# Frame Kiri untuk Kontrol
frame_kiri = tk.Frame(root, width=380, padx=15, pady=10)
frame_kiri.pack(side="left", fill="y")

# Frame Kanan untuk Tabel
frame_kanan = tk.Frame(root, padx=15, pady=10)
frame_kanan.pack(side="right", fill="both", expand=True)

# --- ISI FRAME KIRI ---
# 1. Section Input Manual
group_manual = tk.LabelFrame(frame_kiri, text=" Input Manual ", padx=10, pady=10)
group_manual.pack(fill="x", pady=5)

tk.Label(group_manual, text="Nama Barang:").grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(group_manual, width=25)
entry_nama.grid(row=0, column=1, pady=5, padx=5)

tk.Label(group_manual, text="Stok:").grid(row=1, column=0, sticky="w")
entry_stok = tk.Entry(group_manual, width=25, validate="key", validatecommand=vcmd)
entry_stok.grid(row=1, column=1, pady=5, padx=5)

tk.Button(group_manual, text="Tambah Barang", width=25, command=tambah_data, bg="#f0f0f0").grid(row=2, columnspan=2, pady=10)

# 2. Section Generate Data (N)
group_auto = tk.LabelFrame(frame_kiri, text=" Generate Data Otomatis (Testing) ", padx=10, pady=10)
group_auto.pack(fill="x", pady=10)

tk.Label(group_auto, text="Masukkan n:").grid(row=0, column=0, sticky="w")
entry_n_random = tk.Entry(group_auto, width=25, validate="key", validatecommand=vcmd)
entry_n_random.grid(row=0, column=1, pady=5, padx=5)

tk.Button(group_auto, text="Generate n Data Random", width=25, command=barang_random, bg="#fff9c4").grid(row=1, columnspan=2, pady=10)

# 3. Section Tombol Aksi
frame_btn_sort = tk.LabelFrame(frame_kiri, text=" Eksekusi Sorting ", padx=10, pady=10)
frame_btn_sort.pack(fill="x", pady=5)

tk.Button(frame_btn_sort, text="Sort Iteratif", width=12, bg="#d4edda", command=sort_iteratif).grid(row=0, column=0, padx=5)
tk.Button(frame_btn_sort, text="Sort Rekursif", width=12, bg="#d1ecf1", command=sort_rekursif).grid(row=0, column=1, padx=5)

tk.Button(frame_kiri, text="LIHAT GRAFIK PERBANDINGAN", height=2, bg="#add8e6", font=("Arial", 9, "bold"), command=tampilkan_grafik).pack(fill="x", pady=15)
tk.Button(frame_kiri, text="RESET DATA", bg="#f08080", command=reset_data).pack(fill="x")

# --- ISI FRAME KANAN ---
tk.Label(frame_kanan, text="TABEL STOK BARANG", font=("Arial", 11, "bold")).pack(pady=5)

tabel_frame = tk.Frame(frame_kanan)
tabel_frame.pack(fill="both", expand=True)

tabel = ttk.Treeview(tabel_frame, columns=("Nama", "Stok"), show="headings")
tabel.heading("Nama", text="Nama Barang")
tabel.heading("Stok", text="Jumlah Stok")
tabel.column("Nama", anchor="center")
tabel.column("Stok", anchor="center", width=100)

scrolly = ttk.Scrollbar(tabel_frame, orient="vertical", command=tabel.yview)
tabel.configure(yscrollcommand=scrolly.set)

tabel.pack(side="left", fill="both", expand=True)
scrolly.pack(side="right", fill="y")

root.mainloop()