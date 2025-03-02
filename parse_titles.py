import os
import subprocess

txt_files_dir = 'txt_files'
query = "Тебе дан фрагмент листочка по математике. Определи название темы листочка в одну строчку до 50 символов в формате: 'Заголовок' "
result_txt = "result.txt"
print("1")
def process_text_files():
    for filename in os.listdir(txt_files_dir):
        print("2")
        if filename.endswith('.txt'):
            file_path = os.path.join(txt_files_dir, filename)
            with open(file_path, 'r', encoding='utf-16') as file:
                print("3")
                content = file.read(300)
                print(content)
                full_query = f"{query}: {content}"
                
                result = subprocess.run(['ollama', 'run', 'llama3.2'], 
                                        input=full_query, text=True, capture_output=True)
                if (len(result.stdout.strip()) > 50):
                    print("OUTPUT IS TOO BIG RESTART")
                    result = subprocess.run(['ollama', 'run', 'llama3.2'], 
                                        input=full_query, text=True, capture_output=True)
                if result.returncode == 0:
                    print(f"Заголовок из файла '{filename}': {result.stdout.strip()}")
                    with open(result_txt, 'a', encoding='utf-16') as text_file:
                        text_file.write(f"{filename}: {result.stdout.strip()} \n")
                else:
                    print(f"Ошибка при обработке файла '{filename}': {result.stderr.strip()}")

if __name__ == "__main__":
    process_text_files()