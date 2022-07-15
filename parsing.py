import requests as requests
from bs4 import BeautifulSoup
import sys

languages = {'arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese',
             'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish', 'all'}


def welcome():
    args = sys.argv
    source_language = args[1]
    target_language = args[2]
    word = args[3]
    return [source_language, target_language, word]


def translation(source_language, target_language, word, count):
    url = f'https://context.reverso.net/translation/{source_language.lower()}-{target_language.lower()}/{word}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    if page.status_code == 404:
        print(f'Sorry, unable to find {word}')
        sys.exit()
    elif page.status_code != 200:
        print(f'Something wrong with your internet connection')
        sys.exit()
    soup = BeautifulSoup(page.content, 'html.parser')

    print(f'{target_language} Translations:')
    write_to_file(f'{target_language} Translations:', word)
    words = [word.text.strip() for word in soup.find_all('a', {'class': 'translation'})]
    for index in range(1, min(len(words), count + 1)):
        print(words[index])
        write_to_file(words[index], word)

    print(f'\n{target_language} Examples:')
    write_to_file(f'\n{target_language} Examples:', word)
    examples_from = [example.text.strip() for example in soup.find_all('div', {'class': 'src'}) if example.text.strip()]
    examples_to = [example.text.strip() for example in soup.find_all('div', {'class': 'trg'}) if example.text.strip()]
    for index in range(min(len(examples_to), count)):
        print(f'{examples_from[index]}\n{examples_to[index]}\n')
        write_to_file(f'{examples_from[index]}\n{examples_to[index]}\n', word)


def write_to_file(result, word):
    with open(f'{word}.txt', 'a', encoding='utf-8') as final_result:
        final_result.write(f'{result}\n')


def main():
    greeting = welcome()
    source_language = greeting[0]
    target_language = greeting[1]
    word = greeting[2]
    if source_language not in languages:
        print(f"Sorry, the program doesn't support {source_language}")
        sys.exit()
    if target_language not in languages:
        print(f"Sorry, the program doesn't support {target_language}")
        sys.exit()
    if target_language == 'all':
        for language in languages:
            if language != source_language:
                translation(source_language, language, word, count=1)
    else:
        translation(source_language, target_language, word, count=5)


if __name__ == "__main__":
