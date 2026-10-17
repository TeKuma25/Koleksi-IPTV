"""
M3U Scraper & Stream Updater
Menjalankan:
1. Pengecekan status stream lokal (id.m3u).
2. Scraping stream terupdate dari upstream.
3. Menggabungkan channel aktif tanpa duplikat URL.
4. Menyimpan hasil terstruktur dengan tag group-title yang rapi.
"""

import re
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

def parse_m3u(file_path: str) -> List[Dict[str, str]]:
    """Parse file M3U ke dalam list dictionary channel."""
    channels = []
    if not os.path.exists(file_path):
        return channels

    current_meta = None
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#EXTINF"):
                current_meta = line
            elif line.startswith("#"):
                continue
            elif current_meta:
                channels.append({
                    "meta": current_meta,
                    "url": line
                })
                current_meta = None
    return channels

def extract_channel_info(meta_line: str) -> Tuple[str, str, str, str]:
    """Ekstrak tvg-id, tvg-logo, group-title, dan nama channel dari baris EXTINF."""
    tvg_id = ""
    tvg_logo = ""
    group = "General"
    title = ""

    id_match = re.search(r'tvg-id="([^"]*)"', meta_line)
    if id_match:
        tvg_id = id_match.group(1)

    logo_match = re.search(r'tvg-logo="([^"]*)"', meta_line)
    if logo_match:
        tvg_logo = logo_match.group(1)

    group_match = re.search(r'group-title="([^"]*)"', meta_line)
    if group_match:
        group = group_match.group(1)

    if "," in meta_line:
        title = meta_line.split(",")[-1].strip()
    else:
        title = tvg_id or "Unknown Channel"

    return tvg_id, tvg_logo, group, title

def check_stream_active(channel: Dict[str, str], timeout: int = 4) -> Tuple[Dict[str, str], bool]:
    """Cek apakah stream aktif."""
    url = channel["url"]
    try:
        resp = requests.head(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code in [200, 301, 302]:
            return channel, True
        if resp.status_code in [403, 405, 400]:
            with requests.get(url, headers=HEADERS, timeout=timeout, stream=True) as stream_resp:
                if stream_resp.status_code == 200:
                    return channel, True
    except Exception:
        pass
    return channel, False

def fetch_upstream_channels(country_code: str = "id") -> List[Dict[str, str]]:
    """Mengambil playlist terupdate dari upstream open-source IPTV."""
    upstream_url = f"https://iptv-org.github.io/iptv/countries/{country_code}.m3u"
    print(f"[*] Mengambil stream terupdate untuk '{country_code}' dari upstream {upstream_url}...")
    try:
        resp = requests.get(upstream_url, headers=HEADERS, timeout=12)
        if resp.status_code == 200:
            lines = resp.text.splitlines()
            upstream_channels = []
            curr_meta = None
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    curr_meta = line
                elif curr_meta and not line.startswith("#") and line:
                    upstream_channels.append({
                        "meta": curr_meta,
                        "url": line
                    })
                    curr_meta = None
            print(f"[+] Ditemukan {len(upstream_channels)} channel dari upstream.")
            return upstream_channels
    except Exception as e:
        print(f"[-] Gagal mengambil upstream: {e}")
    return []

def save_m3u(file_path: str, channels: List[Dict[str, str]]):
    """Menyimpan list channel ke file M3U secara rapi dan terkelompok."""
    groups: Dict[str, List[Dict[str, str]]] = {}
    for ch in channels:
        _, _, group, _ = extract_channel_info(ch["meta"])
        if not group or group == "Undefined":
            group = "General"
        if group not in groups:
            groups[group] = []
        groups[group].append(ch)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for grp_name, ch_list in sorted(groups.items()):
            f.write(f"\n# {grp_name}\n")
            for ch in ch_list:
                f.write(f"{ch['meta']}\n{ch['url']}\n")
    print(f"\n[+] Berhasil disimpan ke {file_path} (Total: {len(channels)} channel aktif)")

def update_playlist(input_m3u: str, country_code: str = "id", max_workers: int = 15):
    print("=== M3U STREAM AUTO-UPDATER & SCRAPER ===")
    
    # 1. Baca lokal
    local_channels = parse_m3u(input_m3u)
    print(f"[*] Channel lokal ditemukan: {len(local_channels)}")

    # 2. Ambil upstream
    upstream_channels = fetch_upstream_channels(country_code)

    # 3. Gabungkan kandidat (deduplikasi berdasarkan URL)
    candidates = []
    seen_urls = set()

    for ch in local_channels:
        url = ch["url"].strip()
        if url not in seen_urls:
            seen_urls.add(url)
            candidates.append(ch)

    for ch in upstream_channels:
        url = ch["url"].strip()
        if url not in seen_urls:
            seen_urls.add(url)
            candidates.append(ch)

    print(f"[*] Total channel unik yang akan divalidasi: {len(candidates)}")
    print(f"[*] Menjalankan validasi aktif/tidaknya stream (multi-threading: {max_workers})...")

    active_channels = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_stream_active, ch) for ch in candidates]
        done_count = 0
        for future in as_completed(futures):
            ch, is_active = future.result()
            done_count += 1
            if is_active:
                active_channels.append(ch)
            if done_count % 15 == 0 or done_count == len(candidates):
                print(f"    Progress: {done_count}/{len(candidates)} dicek, aktif saat ini: {len(active_channels)}")

    # 4. Tulis hasil
    save_m3u(input_m3u, active_channels)

if __name__ == "__main__":
    import sys
    targets = [("id.m3u", "id"), ("uk.m3u", "uk")]
    if len(sys.argv) > 2:
        targets = [(sys.argv[1], sys.argv[2])]
    elif len(sys.argv) == 2:
        targets = [(sys.argv[1], "id")]

    for m3u_file, c_code in targets:
        if os.path.exists(m3u_file):
            update_playlist(m3u_file, c_code)
