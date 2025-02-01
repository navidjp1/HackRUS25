import requests
from bs4 import BeautifulSoup



def extract_text_from_url(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text()

    return text

def write_text_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

if __name__ == '__main__':
    pdf_path = 'https://www.gutenberg.org/cache/epub/25344/pg25344.txt'
    book_name = '25344'
    text = extract_text_from_url(pdf_path)
    if text:
        output_file_path = f'/Users/navidjery/Desktop/HackRUS25/backend/{book_name}.txt'
        write_text_to_file(text, output_file_path)
        print(f"Text has been written to {output_file_path}")
