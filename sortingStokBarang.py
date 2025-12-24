import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt
import sys
import random

#config
sys.setrecursionlimit(2000)

data_barang = []
hasil_eksekusi = {"Iteratif": {}, "Rekursif": {}}

#algo bubble sort
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

#utility
def numeric(P):
    return P.isdigit() or P == ""

def update_tabel(data):
    tabel.delete(*tabel.get_children())
    for item in data:
        tabel.insert("", "end", values=item)

#action
def tambah_data():
    try:
        nama = entry_nama.get()
        stok = int(entry_stok.get())
        if not nama:
            raise ValueError

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

#sorting
def sort_iteratif():
    if not data_barang:
        return
    data = list(data_barang)
    start = time.perf_counter_ns()
    bubble_sort_iteratif(data)
    waktu = time.perf_counter_ns() - start

    update_tabel(data)
    hasil_eksekusi["Iteratif"][len(data)] = waktu

def sort_rekursif():
    if not data_barang:
        return
    data = list(data_barang)
    try:
        start = time.perf_counter_ns()
        bubble_sort_rekursif(data, len(data))
        waktu = time.perf_counter_ns() - start

        update_tabel(data)
        hasil_eksekusi["Rekursif"][len(data)] = waktu
    except RecursionError:
        messagebox.showerror("Error", "Limit rekursi terlampaui!")

#graph
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

#reset button
def reset_data():
    if not messagebox.askyesno("Konfirmasi", "Reset semua data?"):
        return
    data_barang.clear()
    hasil_eksekusi["Iteratif"].clear()
    hasil_eksekusi["Rekursif"].clear()
    tabel.delete(*tabel.get_children())

#window config/setup
root = tk.Tk()
root.title("Manajemen Stok Barang")

LEBAR, TINGGI = 600, 520
x = (root.winfo_screenwidth() - LEBAR) // 2
y = (root.winfo_screenheight() - TINGGI) // 2 - 40
root.geometry(f"{LEBAR}x{TINGGI}+{x}+{y}")

#inputan
frame_input = tk.LabelFrame(root, text=" Input Data ", padx=10, pady=10)
frame_input.pack(fill="x", padx=10, pady=5)

frame_center = tk.Frame(frame_input)
frame_center.pack(anchor="center")

vcmd = (root.register(numeric), "%P")

tk.Label(frame_center, text="Nama Barang").grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(frame_center, width=25)
entry_nama.grid(row=0, column=1, padx=5)

tk.Label(frame_center, text="Stok").grid(row=1, column=0, sticky="w")
entry_stok = tk.Entry(frame_center, width=25, validate="key", validatecommand=vcmd)
entry_stok.grid(row=1, column=1, padx=5)

tk.Button(frame_center, text="Tambah ke Tabel", width=30, command=tambah_data)\
    .grid(row=2, columnspan=2, pady=8)

tk.Button(frame_center, text="Tambah Data Random", width=30, command=barang_random)\
    .grid(row=3, columnspan=2)

#tabel setup/config
frame_tabel = tk.Frame(root)
frame_tabel.pack(pady=5)

tabel = ttk.Treeview(frame_tabel, columns=("Nama", "Stok"), show="headings", height=8)
tabel.heading("Nama", text="Nama Barang")
tabel.heading("Stok", text="Stok")
tabel.column("Nama", width=250)
tabel.column("Stok", width=120)
tabel.pack(side="left")

ttk.Scrollbar(frame_tabel, orient="vertical", command=tabel.yview)\
    .pack(side="right", fill="y")
tabel.configure(yscrollcommand=lambda *args: None)

#tombol sorting, tampilkan grafik, reset
frame_aksi = tk.Frame(root)
frame_aksi.pack(pady=10)

tk.Button(frame_aksi, text="Sort Iteratif", width=15, command=sort_iteratif)\
    .grid(row=0, column=0, padx=5)
tk.Button(frame_aksi, text="Sort Rekursif", width=15, command=sort_rekursif)\
    .grid(row=0, column=1, padx=5)

frame_bawah = tk.Frame(root)
frame_bawah.pack(pady=10)

tk.Button(frame_bawah, text="Tampilkan Grafik Perbandingan", width=35,
          bg="#add8e6", command=tampilkan_grafik).pack(pady=4)

tk.Button(frame_bawah, text="Reset Data", width=35,
          bg="#f08080", command=reset_data).pack()

root.mainloop()
