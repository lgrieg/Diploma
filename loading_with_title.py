import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
from PyPDF2 import PdfReader
import csv
import time
import matplotlib.pyplot as plt

START_URL = "https://math.mosolymp.ru"
DOWNLOAD_DIR = "downloads"
#DOWNLOAD_DIR_TXT = "new_downloads/txt"
#DOWNLOAD_DIR_PDF = "new_downloads/pdf"
DOWNLOAD_DIR_TXT = "downloads/txt"
DOWNLOAD_DIR_PDF = "downloads/pdf"
CSV_FILE = "new_downloaded_files.csv"
visited = set()
download_times = []

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR_TXT, exist_ok=True)
os.makedirs(DOWNLOAD_DIR_PDF, exist_ok=True)

with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['PDF URL', 'PDF Filename', 'TXT Filename', 'Page Title'])

def download_pdf_and_save_text(pdf_url, page_title):
    try:
        start_time = time.time()
        response = requests.get(pdf_url)
        if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
            pdf_name = os.path.basename(urlparse(pdf_url).path)
            pdf_path = os.path.join(DOWNLOAD_DIR_PDF, pdf_name)

            with open(pdf_path, 'wb') as f:
                f.write(response.content)

            reader = PdfReader(pdf_path)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''

            txt_name = pdf_name.replace('.pdf', '.txt')
            txt_path = os.path.join(DOWNLOAD_DIR_TXT, txt_name)

            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)

            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([pdf_url, pdf_name, txt_name, page_title])
            duration = time.time() - start_time
            download_times.append((pdf_name, duration))
            print(f"✓ Saved: {pdf_name} | Title: {page_title}")

    except Exception as e:
        print(f"✗ Error downloading {pdf_url}: {e}")

def crawl(url, depth=2):
    if url in visited or depth <= 0:
        return
    visited.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_title = soup.title.string.strip() if soup.title and soup.title.string else 'No Title'

        for link_tag in soup.find_all('a', href=True):
            href = link_tag['href']
            full_url = urljoin(url, href)

            if full_url.lower().endswith('.pdf'):
                download_pdf_and_save_text(full_url, page_title)
            elif urlparse(full_url).netloc == urlparse(START_URL).netloc:
                crawl(full_url, depth=depth-1)
    except Exception as e:
        print(f"✗ Error crawling {url}: {e}")

# Запуск

crawl(START_URL)
# with open('urls.txt') as f:
#     urls = f.readlines()
#     for url in urls:
#         crawl(url)

def plot_download_times():
    if not download_times:
        print("No download data to plot.")
        return

    names = [item[0] for item in download_times]
    times = [item[1] for item in download_times]

    plt.figure(figsize=(10, 6))
    plt.barh(names,times, color='skyblue')
    plt.xlabel("Download Time (seconds)")
    plt.ylabel("PDF File")
    plt.title("PDF Download Times")
    plt.tight_layout()
    plt.savefig("download_times.png")
    plt.show()
    print("📈 Saved download time chart as download_times.png")

plot_download_times()