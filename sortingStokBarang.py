import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(2000)

data_barang = []
hasil_eksekusi = {"Iteratif": {}, "Rekursif": {}}

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

def tambah_data():
    try:
        nama = entry_nama.get()
        stok = int(entry_stok.get())
        if not nama: raise ValueError
        
        data_barang.append((nama, stok))
        tabel.insert("", "end", values=(nama, stok))
        entry_nama.delete(0, tk.END)
        entry_stok.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Isi Nama dan Stok (Angka) dengan benar!")

def update_tabel(data):
    for i in tabel.get_children():
        tabel.delete(i)
    for item in data:
        tabel.insert("", "end", values=item)

def sort_iteratif():
    if not data_barang: return
    data = list(data_barang)
    n = len(data)
    
    start = time.perf_counter_ns()
    bubble_sort_iteratif(data)
    end = time.perf_counter_ns()
    
    waktu = end - start
    update_tabel(data)
    hasil_eksekusi["Iteratif"][n] = waktu
    print(f"Iteratif: {n} data | {waktu} ns")

def sort_rekursif():
    if not data_barang: return
    data = list(data_barang)
    n = len(data)
    
    try:
        start = time.perf_counter_ns()
        bubble_sort_rekursif(data, n)
        end = time.perf_counter_ns()
        
        waktu = end - start
        update_tabel(data)
        hasil_eksekusi["Rekursif"][n] = waktu
        print(f"Rekursif: {n} data | {waktu} ns")
    except RecursionError:
        messagebox.showerror("Limit Rekursi", "Data terlalu banyak untuk metode Rekursif!")

def tampilkan_grafik():
    plt.figure(figsize=(10, 5))
    
    for label, points in hasil_eksekusi.items():
        if points:
            sorted_n = sorted(points.keys())
            sorted_waktu = [points[n] for n in sorted_n]
            plt.plot(sorted_n, sorted_waktu, label=label, marker='o')

    plt.xlabel("Ukuran Input (n)")
    plt.ylabel("Waktu Eksekusi (ns)")
    plt.title("Perbandingan Bubble Sort: Iteratif vs Rekursif")
    plt.legend()
    plt.grid(True)
    plt.show()

root = tk.Tk()
root.title("Manajemen Stok Barang")

frame_input = tk.LabelFrame(root, text=" Input Data ", padx=10, pady=10)
frame_input.pack(padx=10, pady=5, fill="x")

tk.Label(frame_input, text="Nama Barang:").grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(frame_input)
entry_nama.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_input, text="Stok:").grid(row=1, column=0, sticky="w")
entry_stok = tk.Entry(frame_input)
entry_stok.grid(row=1, column=1, padx=5, pady=2)

btn_tambah = tk.Button(frame_input, text="Tambah ke Tabel", command=tambah_data, bg="#e1e1e1")
btn_tambah.grid(row=2, columnspan=2, pady=10, sticky="ew")

frame_tabel = tk.Frame(root)
frame_tabel.pack(padx=10, pady=5)

tabel = ttk.Treeview(frame_tabel, columns=("Nama", "Stok"), show="headings", height=8)
tabel.heading("Nama", text="Nama Barang")
tabel.heading("Stok", text="Stok")
tabel.column("Nama", width=150)
tabel.column("Stok", width=100)
tabel.pack(side="left")

scrollbar = ttk.Scrollbar(frame_tabel, orient="vertical", command=tabel.yview)
tabel.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

frame_aksi = tk.Frame(root)
frame_aksi.pack(pady=10)

tk.Button(frame_aksi, text="Sort Iteratif", command=sort_iteratif, width=15).grid(row=0, column=0, padx=5)
tk.Button(frame_aksi, text="Sort Rekursif", command=sort_rekursif, width=15).grid(row=0, column=1, padx=5)
tk.Button(root, text="Tampilkan Grafik Perbandingan", command=tampilkan_grafik, bg="#add8e6").pack(pady=5, fill="x", padx=10)

root.mainloop()