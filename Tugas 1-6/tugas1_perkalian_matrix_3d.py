import argparse
import random


# ---------------------------------------------------------------
# 1. FUNGSI INTI: perkalian matrix 3 dimensi (tanpa library)
# ---------------------------------------------------------------
def kali_matrix_3d(A, B, tampilkan_langkah=False):
    """Mengalikan dua array 3D (list bersarang) per lapisan."""
    batch, m, n = len(A), len(A[0]), len(A[0][0])
    n_b, p = len(B[0]), len(B[0][0])

    # Validasi ukuran
    if len(B) != batch:
        raise ValueError(f"Jumlah batch beda: A={batch}, B={len(B)}")
    if n != n_b:
        raise ValueError(f"Kolom A ({n}) harus sama dengan baris B ({n_b})")

    # Siapkan hasil C berisi nol, ukuran (batch, m, p)
    C = [[[0 for _ in range(p)] for _ in range(m)] for _ in range(batch)]

    for k in range(batch):              # lapisan ke-k
        for i in range(m):              # baris A
            for j in range(p):          # kolom B
                total = 0
                suku = []
                for x in range(n):      # jumlahkan hasil kali
                    total += A[k][i][x] * B[k][x][j]
                    suku.append(f"{A[k][i][x]}*{B[k][x][j]}")
                C[k][i][j] = total
                if tampilkan_langkah:
                    print(f"  C[{k}][{i}][{j}] = " + " + ".join(suku) + f" = {total}")
    return C


# ---------------------------------------------------------------
# 2. FUNGSI PEMBANTU: membuat, membaca, dan mencetak array
# ---------------------------------------------------------------
def buat_acak(batch, baris, kolom):
    """Membuat array 3D berisi bilangan bulat acak 0-9."""
    return [[[random.randint(0, 9) for _ in range(kolom)]
             for _ in range(baris)] for _ in range(batch)]


def baca_manual(nama, batch, baris, kolom):
    """Meminta pengguna mengetik isi array 3D, satu baris per input."""
    print(f"\nMasukkan isi {nama} ({batch} x {baris} x {kolom}).")
    print(f"Ketik {kolom} angka dipisah spasi untuk setiap baris.")
    array = []
    for k in range(batch):
        lapisan = []
        for i in range(baris):
            while True:
                try:
                    teks = input(f"  {nama}[{k}] baris {i}: ")
                    angka = [float(x) if "." in x else int(x) for x in teks.split()]
                    if len(angka) != kolom:
                        raise ValueError
                    lapisan.append(angka)
                    break
                except ValueError:
                    print(f"  Input salah. Harus tepat {kolom} angka.")
        array.append(lapisan)
    return array


def cetak(nama, array):
    """Mencetak array 3D per lapisan agar mudah dibaca."""
    print(f"\n{nama}  (ukuran {len(array)} x {len(array[0])} x {len(array[0][0])})")
    for k, lapisan in enumerate(array):
        print(f"  Lapisan {k}:")
        for baris in lapisan:
            print("    " + "  ".join(f"{v:>5}" for v in baris))


# ---------------------------------------------------------------
# 3. PROGRAM UTAMA (CLI)
# ---------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Perkalian matrix untuk array 3 dimensi")
    parser.add_argument("-b", "--batch", type=int, default=2, help="jumlah lapisan (default 2)")
    parser.add_argument("-m", type=int, default=2, help="baris A (default 2)")
    parser.add_argument("-n", type=int, default=3, help="kolom A = baris B (default 3)")
    parser.add_argument("-p", type=int, default=2, help="kolom B (default 2)")
    parser.add_argument("--manual", action="store_true", help="ketik isi matrix sendiri")
    parser.add_argument("--langkah", action="store_true", help="tampilkan langkah perhitungan")
    parser.add_argument("--seed", type=int, default=None, help="seed angka acak")
    args = parser.parse_args()

    if min(args.batch, args.m, args.n, args.p) < 1:
        parser.error("Semua ukuran harus >= 1")

    if args.seed is not None:
        random.seed(args.seed)

    # Siapkan A dan B
    if args.manual:
        A = baca_manual("A", args.batch, args.m, args.n)
        B = baca_manual("B", args.batch, args.n, args.p)
    else:
        A = buat_acak(args.batch, args.m, args.n)
        B = buat_acak(args.batch, args.n, args.p)

    cetak("Array A", A)
    cetak("Array B", B)

    # Hitung
    if args.langkah:
        print("\nLangkah perhitungan:")
    C = kali_matrix_3d(A, B, tampilkan_langkah=args.langkah)
    cetak("Hasil C = A x B", C)

    # Verifikasi dengan NumPy (jika terpasang)
    try:
        import numpy as np
        benar = np.array_equal(np.matmul(np.array(A), np.array(B)), np.array(C))
        print("\nVerifikasi dengan numpy.matmul:", "COCOK" if benar else "TIDAK COCOK")
    except ImportError:
        print("\n(NumPy tidak terpasang, verifikasi dilewati)")


if __name__ == "__main__":
    main()
