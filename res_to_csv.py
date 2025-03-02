import csv

def convert_to_csv(input_file, output_file):
    print("started")
    with open(input_file, 'r', encoding='utf-16') as infile, open(output_file, 'w', newline='', encoding='utf-16') as outfile:
        print("opened")
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['Название файла', 'Ссылка на файл', 'Заголовок'])

        for line in infile:
            parts = line.split(': Заголовок :')
            if len(parts) == 2:
                file_name = parts[0].strip()
                title = parts[1].strip()
                pdf_name = file_name.strip()[:-7] + '.pdf'
                file_link = f"https://math.mosolymp.ru/upload/files/2025/khamovniki/11/{pdf_name}"
                csv_writer.writerow([file_name, file_link, title])


input_file_path = 'result.txt'
output_file_path = 'output.csv'

convert_to_csv(input_file_path, output_file_path)