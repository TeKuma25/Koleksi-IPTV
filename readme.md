# Program Pembersih dan Pengelompok M3U

Program ini adalah alat bantu untuk membersihkan dan merapikan file M3U (playlist IPTV). Program ini akan mengecek status setiap URL stream dalam file M3U, menghapus URL yang tidak berfungsi, dan mengelompokkan URL yang berfungsi berdasarkan kategori (group-title).

## Fitur

*   Mengecek status setiap URL stream dalam file M3U.
*   Menghapus URL stream yang tidak berfungsi atau mengalami error.
*   Mengelompokkan URL stream yang berfungsi berdasarkan kategori (group-title).
*   Menyimpan URL stream yang sudah dibersihkan dan dikelompokkan ke dalam file M3U baru.
*   Menampilkan progress bar saat pengecekan URL.
*   Menampilkan laporan URL yang dihapus dan penyebab errornya.
*   Input path file M3U dan nama file output dari pengguna.
*   Menampilkan nama program di awal.
*   Penanganan error untuk file yang tidak ditemukan dan error saat penulisan file.

## Cara Menggunakan

1.  Pastikan Anda sudah meng-install library `requests` dan `tqdm`:

    ```bash
    pip install requests tqdm
    ```

2.  Unduh atau clone repositori ini.

3.  Simpan kode Python di atas sebagai file, misalnya `m3u_organizer_filter.py`, di dalam direktori program ini.

4.  Jalankan program dengan perintah:

    ```bash
    python m3u_organizer_filter.py
    ```

5.  Ikuti instruksi yang ditampilkan di terminal:
    *   Masukkan path file M3U input.
    *   Masukkan nama file M3U output.

6.  File M3U baru yang sudah dibersihkan dan dikelompokkan akan dibuat di direktori yang sama dengan nama yang Anda masukkan.

## Contoh Penggunaan

Program Pembersih dan Pengelompok M3U
Masukkan path file M3U: playlist_input.m3u
Masukkan nama file M3U output: playlist_output_bersih.m3u

[========================================] 100%   0:00:10

Proses selesai.
Total URL: 150

URL yang dihapus:

http://url_rusak_1.m3u8: Gagal, Status Code: 404
http://url_error.m3u8: Error: Koneksi ditolak ...

## Keterangan

*   File M3U input adalah file M3U yang akan dibersihkan dan dirapikan.
*   File M3U output adalah file M3U baru yang berisi URL stream yang berfungsi dan sudah dikelompokkan.
*   Program akan menampilkan progress bar saat pengecekan URL.
*   Setelah selesai, program akan menampilkan laporan URL yang dihapus dan penyebab errornya.

## Kontribusi

Anda dipersilakan untuk berkontribusi pada pengembangan program ini. Silakan kirimkan *pull request* jika Anda memiliki fitur baru atau perbaikan yang ingin ditambahkan.

## Lisensi

[Tambahkan lisensi yang sesuai, misalnya MIT License]

## Informasi Tambahan

Program ini dibuat untuk memudahkan pengelolaan koleksi file M3U IPTV.  Repository ini juga berisi koleksi file M3U lainnya.  Gunakan program ini dengan bijak dan sesuai dengan hukum yang berlaku.  Kami tidak bertanggung jawab atas penyalahgunaan program ini.

## Terima Kasih

Terima kasih telah menggunakan program ini!  Jika Anda memiliki pertanyaan atau saran, silakan hubungi kami.