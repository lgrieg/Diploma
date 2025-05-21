import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
from PyPDF2 import PdfReader

import csv


START_URL = "https://math.mosolymp.ru"
DOWNLOAD_DIR = "pdf_miner_downloads"
CSV_FILE = "downloaded_files.csv"
visited = set()

with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['PDF URL', 'PDF Filename', 'TXT Filename'])

def download_pdf_and_save_text(pdf_url):
    try:
        response = requests.get(pdf_url)
        if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
            pdf_name = os.path.basename(urlparse(pdf_url).path)
            pdf_path = os.path.join(DOWNLOAD_DIR, pdf_name)

            with open(pdf_path, 'wb') as f:
                f.write(response.content)

            reader = PdfReader(pdf_path)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''

            txt_name = pdf_name.replace('.pdf', '.txt')
            txt_path = os.path.join(DOWNLOAD_DIR, txt_name)

            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)

            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([pdf_url, pdf_name, txt_name])
            print(f"✓ Saved: {pdf_name}")

    except Exception as e:
        print(f"✗ Error downloading {pdf_url}: {e}")

def crawl(url, depth=2):
    if url in visited or depth <= 0:
        return
    visited.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link_tag in soup.find_all('a', href=True):
            href = link_tag['href']
            full_url = urljoin(url, href)

            if full_url.lower().endswith('.pdf'):
                download_pdf_and_save_text(full_url)
            elif urlparse(full_url).netloc == urlparse(START_URL).netloc:
                crawl(full_url, depth=depth-1)
    except Exception as e:
        print(f"✗ Error crawling {url}: {e}")

crawl(START_URL)
