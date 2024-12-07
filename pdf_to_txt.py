import os
import pytesseract
import pdf2image
from pdf2image import convert_from_path

#~/lada_venv/bin/python3 /Users/lgrieg/Documents/Diploma/pdf_to_txt.py

def ocr_pdf_to_text(pdf_folder, text_folder):
    if not os.path.exists(text_folder):
        os.makedirs(text_folder)

    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f'Обработка файла: {pdf_path}')

            images = convert_from_path(pdf_path)

            text_content = ""
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image, lang='rus')
                text_content += f"--- Страница {i + 1} ---n{text}n"

            # Сохраняем извлеченный текст в файл
            text_filename = os.path.splitext(filename)[0] + 'rus' + '.txt'
            text_path = os.path.join(text_folder, text_filename)
            with open(text_path, 'w', encoding='utf-16') as text_file:
                text_file.write(text_content)
            print(f'Сохранен текстовый файл: {text_path}')


pdf_folder = 'downloaded_pdfs'
text_folder = 'txt_files'
ocr_pdf_to_text(pdf_folder, text_folder)