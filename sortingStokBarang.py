import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider 
from matplotlib.widgets import Slider, RadioButtons
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
    # 1. Cek Data
    if not hasil_eksekusi["Iteratif"] and not hasil_eksekusi["Rekursif"]:
        messagebox.showwarning("Peringatan", "Belum ada data analisis!")
        return
        
    # --- SETUP LAYOUT ---
    # sharex=True: Zoom X di atas akan ngefek ke bawah juga
    fig, (ax_main, ax_diff) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[2, 1], sharex=True)
    
    # Atur margin supaya Slider & Radio Button muat
    plt.subplots_adjust(bottom=0.25, left=0.15, right=0.95, top=0.95, hspace=0.15)

    # --- AUTO MAXIMIZE WINDOW (Full Screen) ---
    manager = plt.get_current_fig_manager()
    try:
        # Perintah ini bekerja di Windows (Tkinter backend)
        manager.window.state('zoomed')
    except:
        try:
            # Fallback untuk OS lain (Linux/Mac)
            manager.full_screen_toggle()
        except:
            pass # Kalau gagal, biarkan ukuran default

    all_times = []
    all_n = []
    data_points = {"Iteratif": {}, "Rekursif": {}}

    # --- 1. PLOT GRAFIK UTAMA (ATAS) ---
    if hasil_eksekusi["Iteratif"]:
        n_vals = sorted(hasil_eksekusi["Iteratif"].keys())
        waktu_vals = [hasil_eksekusi["Iteratif"][i] for i in n_vals]
        all_times.extend(waktu_vals)
        all_n.extend(n_vals)
        for n, t in zip(n_vals, waktu_vals): data_points["Iteratif"][n] = t
        ax_main.plot(n_vals, waktu_vals, marker='o', linestyle='-', color='blue', label='Iteratif', alpha=0.8)

    if hasil_eksekusi["Rekursif"]:
        n_vals = sorted(hasil_eksekusi["Rekursif"].keys())
        waktu_vals = [hasil_eksekusi["Rekursif"][i] for i in n_vals]
        all_times.extend(waktu_vals)
        all_n.extend(n_vals)
        for n, t in zip(n_vals, waktu_vals): data_points["Rekursif"][n] = t
        ax_main.plot(n_vals, waktu_vals, marker='x', linestyle='--', color='red', label='Rekursif', alpha=0.8)

    ax_main.set_ylabel("Waktu (ns)")
    ax_main.set_title("Perbandingan Waktu Eksekusi (Atas) & Overhead Gap (Bawah)", fontweight='bold')
    ax_main.legend(loc='upper left')
    ax_main.grid(True, which="both", ls=":", alpha=0.6)

    # --- 2. PLOT SELISIH (BAWAH) ---
    common_n = sorted(list(set(data_points["Iteratif"].keys()) & set(data_points["Rekursif"].keys())))
    if common_n:
        # Hitung Gap
        gaps = [data_points["Rekursif"][n] - data_points["Iteratif"][n] for n in common_n]
        
        ax_diff.plot(common_n, gaps, color='purple', linestyle='-', marker='.', linewidth=1)
        ax_diff.fill_between(common_n, gaps, 0, color='purple', alpha=0.3)
        ax_diff.axhline(0, color='black', linewidth=1) # Garis nol
        
        # Anotasi Max Gap
        max_gap = max(gaps)
        max_n = common_n[gaps.index(max_gap)]
        ax_diff.annotate(f'Max Gap:\n{max_gap} ns', 
                         xy=(max_n, max_gap), 
                         xytext=(max_n, max_gap * 1.3),
                         arrowprops=dict(facecolor='black', arrowstyle='->'),
                         fontsize=9, color='purple', fontweight='bold')

    ax_diff.set_ylabel("Selisih (ns)")
    ax_diff.set_xlabel("Ukuran Input (n)")
    ax_diff.grid(True, alpha=0.5)

    # --- 3. SLIDER CONFIG (X & Y) ---
    if not all_times or not all_n: return

    max_n_val = max(all_n)
    max_time_val = max(all_times) * 1.1

    # Slider Y (Mengontrol Grafik Atas)
    ax_slider_y = plt.axes([0.20, 0.12, 0.60, 0.03], facecolor='lightgoldenrodyellow')
    slider_y = Slider(ax_slider_y, 'Zoom Y (Main) ', 0, max_time_val, valinit=max_time_val)

    # Slider X (Mengontrol KEDUA Grafik)
    ax_slider_x = plt.axes([0.20, 0.07, 0.60, 0.03], facecolor='lightblue')
    slider_x = Slider(ax_slider_x, 'Zoom X (n) ', min(all_n), max_n_val, valinit=max_n_val, valstep=1)

    def update_sliders(val):
        # Update Y Limit (Hanya grafik atas)
        ax_main.set_ylim(ymin=0, ymax=slider_y.val)
        
        # Update X Limit (Otomatis kedua grafik karena sharex=True)
        ax_main.set_xlim(xmin=min(all_n)*0.9, xmax=slider_x.val)
        
        # Grafik bawah (Diff) kita autoscale Y-nya biar gap selalu terlihat jelas
        ax_diff.relim()
        ax_diff.autoscale_view()
        
        fig.canvas.draw_idle()

    slider_y.on_changed(update_sliders)
    slider_x.on_changed(update_sliders)

    # --- 4. RADIO BUTTON (LINEAR/LOG) ---
    ax_radio = plt.axes([0.02, 0.4, 0.10, 0.15], facecolor='#f0f0f0')
    radio = RadioButtons(ax_radio, ('Linear', 'Logarithmic'))

    def change_scale(label):
        if label == 'Linear':
            ax_main.set_yscale('linear')
            ax_main.set_ylim(ymin=0, ymax=slider_y.val)
        else:
            ax_main.set_yscale('log')
            ax_main.autoscale(enable=True, axis='y')
            
        fig.canvas.draw_idle()

    radio.on_clicked(change_scale)

    # Simpan referensi widget
    fig.slider_y = slider_y
    fig.slider_x = slider_x
    fig.radio = radio

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

tk.Label(frame_kanan, text="HISTORY", font=("Arial", 10, "bold")).pack(anchor="w")
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