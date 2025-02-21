import requests
import re
import os
from tqdm import tqdm

def cek_status_m3u(file_path):
    """
    Mengecek status setiap URL stream dalam file M3U dan mengembalikan dictionary URL yang berfungsi beserta informasi #EXTINF.

    Args:
        file_path (str): Path ke file M3U.

    Returns:
        dict: Dictionary dengan kategori sebagai key dan list entri M3U sebagai value.
    """

    kategori = {}
    total_url = 0
    url_gagal = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("#EXTINF"):
                    total_url += 1
                    informasi_extinf = line
                    url_stream = f.readline().strip()

                    try:
                        response = requests.head(url_stream, timeout=5)
                        if response.status_code == 200:
                            # Ekstrak group-title menggunakan regex
                            match = re.search(r'group-title="([^"]+)"', informasi_extinf)
                            if match:
                                nama_kategori = match.group(1)
                            else:
                                nama_kategori = "Undefined"  # Kategori default jika tidak ada group-title

                            # Tambahkan entri ke kategori yang sesuai
                            if nama_kategori not in kategori:
                                kategori[nama_kategori] = []
                            kategori[nama_kategori].append(f"#EXTINF{informasi_extinf[8:]}{url_stream}\n")
                        else:
                            url_gagal[url_stream] = f"Gagal, Status Code: {response.status_code}"
                    except requests.exceptions.RequestException as e:
                        url_gagal[url_stream] = f"Error: {e}"
    except FileNotFoundError:
        print(f"Error: File '{file_path}' tidak ditemukan.")
        return None, None, None

    return kategori, total_url, url_gagal

def tulis_m3u_terkategori(kategori, output_file_path):
    """
    Menulis entri M3U yang sudah dikategorikan ke file baru.

    Args:
        kategori (dict): Dictionary kategori dari fungsi cek_status_m3u.
        output_file_path (str): Path untuk file M3U yang baru.
    """

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for nama_kategori, entri in kategori.items():
                f.write(f"\n# {nama_kategori}\n")
                for item in entri:
                    f.write(item)
                f.write("\n")
    except Exception as e:
        print(f"Error saat menulis file: {e}")

def main():
    """
    Fungsi utama program.
    """

    print("Program Pembersih dan Pengelompok M3U")
    file_m3u_input = input("Masukkan path file M3U: ")

    if not os.path.exists(file_m3u_input):
        print(f"Error: File '{file_m3u_input}' tidak ditemukan.")
        return

    kategori, total_url, url_gagal = cek_status_m3u(file_m3u_input)

    if kategori is None:
        return

    file_m3u_output = input("Masukkan nama file M3U output: ")
    tulis_m3u_terkategori(kategori, file_m3u_output)

    print("\nProses selesai.")
    print(f"Total URL: {total_url}")

    if url_gagal:
        print("\nURL yang dihapus:")
        for url, pesan in url_gagal.items():
            print(f"- {url}: {pesan}")

if __name__ == "__main__":
    main()