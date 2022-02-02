import json
import requests
from bs4 import BeautifulSoup

URL_ADDRESS = 'https://www.securitylab.ru/news'


def get_links(): 
    """ список новостей """
    req_get = requests.get(URL_ADDRESS)
    soup = BeautifulSoup(req_get.content, 'html.parser')
    url_news = soup.findAll('a', class_="article-card inline-card")
    # находим все ссылки на новости 1 страницы
    news_one = [] # создаем пустой список, в который будем добалять ссылки на новости
    for item in url_news: # получаем отдельно каждую новость и добавляем в список
        news_one.append('https://www.securitylab.ru' + item.get('href'))
    return news_one #возвращаем список новостей


def get_page_content(link): 
    """список данных для новости"""
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    title_one = soup.find('h1', class_="page-title pt-3 px-3") # первый заголовок новости
    title_two = soup.find('p') # второй заголовок новости
    title_end = title_one.text.rstrip() + '. ' + title_two.text # общий заголовок новости

    img_one = soup.find('img', alt="article-title") # внутренняя ссылка на изображение
    item_img = 'https://www.securitylab.ru' + img_one.get('src') # глобальная ссылка на изображение

    body_one = soup.find('div', itemprop="description") 
    # так как текст новости разбит на несколько абзацев, сначала находим их все
    body_group = [] # создаем пустой список для добавления всех абзацев
    for item_body in body_one:
        body_group.append(item_body.text.strip()) 
    # добавляем абзацы в список, при этом обрезая знаки переносов и пробелов
    body_end = ''.join(body_group) # создаем строчный файл без абзацев

    author_one = soup.find('div', itemprop="author") # имя автора новости

    date_time = soup.find('time') 
    # так как дата и время в новости идут в одной строке, 
    # то при добавлении в словарь, разбиваем их отдельно через индекс строки
    page_info = {
    'url': link, 
    'title': title_end, 
    'img': item_img, 
    'body': body_end, 
    'author': author_one.text, 
    'date': date_time.text[8:], 
    'time': date_time.text[0:5]
    } 

    return page_info # возвращаем словарь с данными о новости


def main(): 
    """ компиляция ссылки на новость и данных, и создание json файла """
    links = get_links() # ссылки на новости
    top_news = [] # пустой список для ссылок на новости и их данных

    for link in links: # добавляем к каждой новости данные по ней
        print(f"Обрабатывается {link}")
        info = get_page_content(link)
        print(info) 
        # можно убрать знак хеша(#) и будет печататься get_page_content
        top_news.append(info)

    with open("www-securitylab-ru.json", 'wt', encoding='cp1251') as file: # создание json файла
        json.dump(top_news, file)
    print("Работа завершена")

# Главная функция
if __name__ == "__main__":
    main()
