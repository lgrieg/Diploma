import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def download_pdf(url, folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            full_url = urljoin(url, href)
            pdf_links.append(full_url)

    if not os.path.exists(folder):
        os.makedirs(folder)

    for pdf_link in pdf_links:
        try:
            print(f'Скачивание: {pdf_link}')
            pdf_response = requests.get(pdf_link)
            pdf_name = os.path.join(folder, pdf_link.split('/')[-1])
            with open(pdf_name, 'wb') as f:
                f.write(pdf_response.content)
            print(f'Сохранен: {pdf_name}')
        except Exception as e:
            print(f'Ошибка при скачивании {pdf_link}: {e}')


website_url = 'https://math.mosolymp.ru/2025_khamovniki_11'
download_folder = 'downloaded_pdfs'

download_pdf(website_url, download_folder)