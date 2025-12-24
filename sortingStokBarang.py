import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt
import sys
import random

# --- CONFIG ---
sys.setrecursionlimit(20000)

data_barang = []
hasil_eksekusi = {"Iteratif": {}, "Rekursif": {}}
attempt_counter = 0  

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

def update_tabel_stok(data):
    tabel_stok.delete(*tabel_stok.get_children())
    for item in data:
        tabel_stok.insert("", "end", values=item)

# --- ACTION ---
def tambah_data():
    try:
        nama = entry_nama.get()
        stok_str = entry_stok.get()
        if not nama or not stok_str:
            raise ValueError
        
        stok = int(stok_str)
        data_barang.append((nama, stok))
        tabel_stok.insert("", "end", values=(nama, stok))
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
            stok = random.randint(1, 1000)
            data_barang.append((nama, stok))
            tabel_stok.insert("", "end", values=(nama, stok))
            
        entry_n_random.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Masukkan jumlah data (n) yang valid!")

def sort_iteratif():
    global attempt_counter
    if not data_barang: return
    
    data = list(data_barang)
    n = len(data)
    start = time.perf_counter_ns()
    bubble_sort_iteratif(data)
    waktu = time.perf_counter_ns() - start
    
    update_tabel_stok(data)
    hasil_eksekusi["Iteratif"][n] = waktu
    
    attempt_counter += 1
    tabel_history.insert("", "end", values=(attempt_counter, n, f"{waktu} ns", "-"))

def sort_rekursif():
    global attempt_counter
    if not data_barang: return
    
    data = list(data_barang)
    n = len(data)
    try:
        start = time.perf_counter_ns()
        bubble_sort_rekursif(data, n)
        waktu = time.perf_counter_ns() - start
        
        update_tabel_stok(data)
        hasil_eksekusi["Rekursif"][n] = waktu
        
        attempt_counter += 1
        tabel_history.insert("", "end", values=(attempt_counter, n, "-", f"{waktu} ns"))
    except RecursionError:
        messagebox.showerror("Error", "Limit rekursi terlampaui!")

# FUNGSI BARU: JALANKAN KEDUANYA
def run_comparison():
    global attempt_counter
    if not data_barang: 
        messagebox.showwarning("Peringatan", "Data kosong!")
        return
    
    n = len(data_barang)
    
    # 1. Jalankan Iteratif
    data_it = list(data_barang)
    start_it = time.perf_counter_ns()
    bubble_sort_iteratif(data_it)
    waktu_it = time.perf_counter_ns() - start_it
    hasil_eksekusi["Iteratif"][n] = waktu_it
    
    # 2. Jalankan Rekursif
    data_rec = list(data_barang)
    try:
        start_rec = time.perf_counter_ns()
        bubble_sort_rekursif(data_rec, n)
        waktu_rec = time.perf_counter_ns() - start_rec
        hasil_eksekusi["Rekursif"][n] = waktu_rec
        rec_display = f"{waktu_rec} ns"
    except RecursionError:
        rec_display = "Error (Limit)"
    
    # Update UI
    update_tabel_stok(data_it)
    attempt_counter += 1
    tabel_history.insert("", "end", values=(attempt_counter, n, f"{waktu_it} ns", rec_display))
    messagebox.showinfo("Selesai", f"Perbandingan selesai untuk n={n}")

def tampilkan_grafik():
    if not hasil_eksekusi["Iteratif"] and not hasil_eksekusi["Rekursif"]:
        messagebox.showwarning("Peringatan", "Belum ada data analisis!")
        return
        
    plt.figure(figsize=(10, 6))
    for label, points in hasil_eksekusi.items():
        if points:
            n_vals = sorted(points.keys())
            waktu_vals = [points[i] for i in n_vals]
            plt.plot(n_vals, waktu_vals, marker='o', label=f"Bubble Sort {label}")

    plt.xlabel("Ukuran Input (n)")
    plt.ylabel("Waktu (ns)")
    plt.title("Perbandingan Kecepatan Bubble Sort")
    plt.legend()
    plt.grid(True)
    plt.show()

def reset_data():
    global attempt_counter
    if not messagebox.askyesno("Konfirmasi", "Reset semua data?"):
        return
    data_barang.clear()
    hasil_eksekusi["Iteratif"].clear()
    hasil_eksekusi["Rekursif"].clear()
    attempt_counter = 0
    tabel_stok.delete(*tabel_stok.get_children())
    tabel_history.delete(*tabel_history.get_children())

# --- WINDOW SETUP ---
root = tk.Tk()
root.title("Tubes AKA 2025 - Analisis Kompleksitas Algoritma")

LEBAR, TINGGI = 1100, 700 
x = (root.winfo_screenwidth() - LEBAR) // 2
y = (root.winfo_screenheight() - TINGGI) // 2
root.geometry(f"{LEBAR}x{TINGGI}+{x}+{y}")

vcmd = (root.register(numeric), "%P")

# --- LAYOUTING ---
frame_kiri = tk.Frame(root, width=350, padx=15, pady=10)
frame_kiri.pack(side="left", fill="y")

frame_kanan = tk.Frame(root, padx=15, pady=10)
frame_kanan.pack(side="right", fill="both", expand=True)

# --- ISI FRAME KIRI ---
group_input = tk.LabelFrame(frame_kiri, text=" Pengaturan Data ", padx=10, pady=10)
group_input.pack(fill="x", pady=5)

tk.Label(group_input, text="Nama Barang:").grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(group_input, width=22)
entry_nama.grid(row=0, column=1, pady=3)

tk.Label(group_input, text="Stok:").grid(row=1, column=0, sticky="w")
entry_stok = tk.Entry(group_input, width=22, validate="key", validatecommand=vcmd)
entry_stok.grid(row=1, column=1, pady=3)

tk.Button(group_input, text="Tambah Manual", width=28, command=tambah_data).grid(row=2, columnspan=2, pady=10)

tk.Label(group_input, text="Generate (n):").grid(row=3, column=0, sticky="w")
entry_n_random = tk.Entry(group_input, width=22, validate="key", validatecommand=vcmd)
entry_n_random.grid(row=3, column=1, pady=3)

tk.Button(group_input, text="Generate Data Random", width=28, bg="#fff9c4", command=barang_random).grid(row=4, columnspan=2, pady=5)

# Group Eksekusi (DIUBAH)
group_aksi = tk.LabelFrame(frame_kiri, text=" Eksekusi ", padx=10, pady=10)
group_aksi.pack(fill="x", pady=10)

tk.Button(group_aksi, text="Sort Iteratif", width=12, bg="#d4edda", command=sort_iteratif).grid(row=0, column=0, padx=5, pady=5)
tk.Button(group_aksi, text="Sort Rekursif", width=12, bg="#d1ecf1", command=sort_rekursif).grid(row=0, column=1, padx=5, pady=5)
# Tombol Baru
tk.Button(group_aksi, text="Jalankan Keduanya (Comparison)", width=27, bg="#ffe0b2", font=("Arial", 9, "bold"), command=run_comparison).grid(row=1, columnspan=2, pady=10)

tk.Button(frame_kiri, text="TAMPILKAN GRAFIK", height=2, bg="#add8e6", font=("Arial", 10, "bold"), command=tampilkan_grafik).pack(fill="x", pady=10)
tk.Button(frame_kiri, text="RESET SEMUA", bg="#f08080", command=reset_data).pack(fill="x")

# --- ISI FRAME KANAN (DUA TABEL) ---
tk.Label(frame_kanan, text="TABEL STOK BARANG", font=("Arial", 10, "bold")).pack(anchor="w")
tabel_stok_frame = tk.Frame(frame_kanan)
tabel_stok_frame.pack(fill="both", expand=True, pady=(0, 20))

tabel_stok = ttk.Treeview(tabel_stok_frame, columns=("Nama", "Stok"), show="headings", height=10)
tabel_stok.heading("Nama", text="Nama Barang")
tabel_stok.heading("Stok", text="Jumlah Stok")
tabel_stok.column("Nama", anchor="center")
tabel_stok.column("Stok", anchor="center")

scrollbar1 = ttk.Scrollbar(tabel_stok_frame, orient="vertical", command=tabel_stok.yview)
tabel_stok.configure(yscrollcommand=scrollbar1.set)
tabel_stok.pack(side="left", fill="both", expand=True)
scrollbar1.pack(side="right", fill="y")

tk.Label(frame_kanan, text="HISTORY WAKTU EKSEKUSI (Log)", font=("Arial", 10, "bold")).pack(anchor="w")
tabel_hist_frame = tk.Frame(frame_kanan)
tabel_hist_frame.pack(fill="both", expand=True)

tabel_history = ttk.Treeview(tabel_hist_frame, columns=("Attempt", "n", "Iteratif", "Rekursif"), show="headings", height=8)
tabel_history.heading("Attempt", text="Attempt")
tabel_history.heading("n", text="n (Data)")
tabel_history.heading("Iteratif", text="Waktu Iteratif")
tabel_history.heading("Rekursif", text="Waktu Rekursif")

tabel_history.column("Attempt", width=70, anchor="center")
tabel_history.column("n", width=70, anchor="center")
tabel_history.column("Iteratif", width=150, anchor="center")
tabel_history.column("Rekursif", width=150, anchor="center")

scrollbar2 = ttk.Scrollbar(tabel_hist_frame, orient="vertical", command=tabel_history.yview)
tabel_history.configure(yscrollcommand=scrollbar2.set)
tabel_history.pack(side="left", fill="both", expand=True)
scrollbar2.pack(side="right", fill="y")

root.mainloop()