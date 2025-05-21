import pandas as pd
import requests
import os
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"
response_times = []

def ask_ollama_for_title(text):
    prompt = "Read text with math problems and return a title of 5 words or less"
    full_prompt = f"{prompt}\n\n{text[:300]}"

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False
    })

    if response.status_code == 200:
        return response.json().get("response", "").strip()
    else:
        print(f"Ошибка запроса: {response.status_code}")
        return ""

def process_csv(csv_path):
    start_time = time.time()
    df = pd.read_csv(csv_path)

    for index, row in df.iterrows():
        txt_path = 'downloads/txt/' + row['TXT Filename']
        if not os.path.isfile(txt_path):
            print(f"Файл не найден: {txt_path}")
            continue

        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()

        print(f"Обработка файла: {txt_path}")
        title = ask_ollama_for_title(text)
        if len(title) > 50:
            title = ask_ollama_for_title('This text is too long, try again' + text)
        print(f"Предложенный заголовок: {title}")

        duration = time.time() - start_time
        response_times.append((txt_path, duration))

        df.at[index, 'Page Title'] = title
        time.sleep(1)  # Не нагружаем Ollama

    df.to_csv("updated_" + os.path.basename(csv_path), index=False)
    print("Обновлённый CSV сохранён.")


process_csv("mosolymp_titles.csv")
print(response_times)
#response_times.to_txt('ollama_time_test.txt')