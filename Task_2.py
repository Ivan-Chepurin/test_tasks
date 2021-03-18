#  pip install beautifulsoup4 requests lxml

'''
Task 2:
В нашей школе мы не можем разглашать персональные данные пользователей, но чтобы преподаватель и ученик смогли объяснить нашей поддержке, кого они имеют в виду (у преподавателей, например, часто учится несколько Саш), мы генерируем пользователям уникальные и легко произносимые имена. Имя у нас состоит из прилагательного, имени животного и двузначной цифры. В итоге получается, например, "Перламутровый лосось 77". Для генерации таких имен мы и решали следующую задачу:
Получить с русской википедии список всех животных (Категория:Животные по алфавиту) и вывести количество животных на каждую букву алфавита. Результат должен получиться в следующем виде:
 А: 642
Б: 412
В:....
'''

from bs4 import BeautifulSoup as bs
import requests


class AnimalCounter:
    base_url = 'https://ru.wikipedia.org'
    page_urls = [
        '/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%D0%90']
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    soup = None
    animals = {}

    # def __init__(self):
    #     self.set_soup()

    def draw(self):
        counter = 0
        while self.page_urls[-1]:
            counter += 1
            print(f'Читаю страницу {counter}')
            self.set_soup()
            self.page_urls.append(self.get_next_page_href())
            self.filling_out_animal_dictionary()

        self.print_results()

    def print_results(self):
        for key, value in self.animals.items():
            print(f'{key}: {len(value)}')

    def get_page_soup(self, page_url):
        src = requests.get(self.base_url + page_url, headers=self.headers).text
        return bs(src, 'lxml')

    def set_soup(self):
        self.soup = self.get_page_soup(self.page_urls[-1]).find('div', id='mw-pages')

    def get_next_page_href(self):
        try:
            href = self.soup.find('a', text='Следующая страница').get('href')
        except Exception:
            href = None
        finally:
            return href

    def filling_out_animal_dictionary(self):
        animals = self.get_all_animals_from_page()
        for item in animals:
            animal = item.text
            if animal:
                if animal[0].lower() not in self.animals:
                    self.animals[animal[0].lower()] = [animal]
                else:
                    self.animals[animal[0].lower()].append(animal)

    def get_all_animals_from_page(self):
        return self.soup.find_all('li')


if __name__ == "__main__":
    ac = AnimalCounter()
    ac.draw()
