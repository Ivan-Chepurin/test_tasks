#  pip install beautifulsoup4 requests lxml

"""
Task 2:
В нашей школе мы не можем разглашать персональные данные пользователей, но чтобы преподаватель и ученик смогли объяснить нашей поддержке, кого они имеют в виду (у преподавателей, например, часто учится несколько Саш), мы генерируем пользователям уникальные и легко произносимые имена. Имя у нас состоит из прилагательного, имени животного и двузначной цифры. В итоге получается, например, "Перламутровый лосось 77". Для генерации таких имен мы и решали следующую задачу:
Получить с русской википедии список всех животных (Категория:Животные по алфавиту) и вывести количество животных на каждую букву алфавита. Результат должен получиться в следующем виде:
А: 642
Б: 412
В:....
"""
import multiprocessing

from bs4 import BeautifulSoup as bs
import requests
from threading import Thread


class CharAnimalCounter:
    base_url = 'https://ru.wikipedia.org'

    headers = None
    soup = None
    forward = True

    def __init__(self, headers, char, start_link, thread_name=None):
        self.headers = headers
        self.char = char
        self.start_link = start_link
        self.thread_name = thread_name
        self.animals = []
        self.pages_urls = []

    def draw(self):
        while self.forward:
            self.set_soup()
            self.pages_urls.append(self.get_next_page_href())
            self.filling_out_animal_dictionary()

    def set_soup(self):
        if self.pages_urls:
            self.soup = self.get_page_soup(
                self.base_url + self.pages_urls[-1]
            ).find('div', id='mw-pages')
        else:
            self.soup = self.get_page_soup(
                self.start_link
            ).find('div', id='mw-pages')

    def get_next_page_href(self):
        try:
            href = self.soup.find('a', text='Следующая страница').get('href')
        except Exception:
            href = None
        finally:
            return href

    def filling_out_animal_dictionary(self):
        blocks = self.soup.find_all('div', class_='mw-category-group')
        if blocks[-1].find('h3').text.lower() != self.char.lower():
            self.forward = False

        if blocks[0].find('h3').text.lower() == self.char.lower():
            for item in self.get_all_animals_from_page(blocks[0]):
                animal = item.text
                if animal:
                    self.animals.append(animal)

    def get_page_soup(self, page_url):
        src = requests.get(page_url, headers=self.headers).text
        return bs(src, 'lxml')

    def get_all_animals_from_page(self, div):
        return div.find_all('li')


all_animals = {}


class FastAnimalCounter(Thread):
    parser = None
    char = None

    def __init__(self, parser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = parser
        self.animals = []

    def run(self) -> None:
        self.parser.draw()
        self.animals = self.parser.animals
        self.char = self.parser.char


def get_char_links(url, headers):
    src = requests.get(url, headers=headers)
    soup = bs(src.text, 'lxml')
    letters_tags = soup.find('div', class_='toccolours plainlinks center').find('span').find_all('a')

    char_links = {}
    for i in letters_tags:
        if i.text not in ['ё', 'Ё']:
            char_links[i.text] = i.get('href')
    return char_links


if __name__ == "__main__":

    url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D1%8B%D0%B5+%D0%B3%D0%BE%D1%84%D0%B5%D1%80%D1%8B&subcatfrom=%D0%92&filefrom=%D0%92#mw-pages"
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }

    char_links = get_char_links(url, headers)

    threads = []
    for key, value in char_links.items():
        thread_name = 'Thread {}'.format(key)
        parser = CharAnimalCounter(
            headers,
            key,
            value,
            thread_name=thread_name
        )

        t = FastAnimalCounter(parser=parser,
                              name=thread_name)
        t.start()
        threads.append(t)

    for i in threads:
        i.join()
        print(i, 'закончил')
        all_animals[i.char] = i.animals

    for key, value in all_animals.items():
        print(f'{key}: {len(value)}')
