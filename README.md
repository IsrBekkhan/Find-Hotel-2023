<h1 align="center">Find Hotel 2023</h1>
  

<p align="center">

<img alt="Static Badge" src="https://img.shields.io/badge/Python-3.10-%23EAD248?logo=python&logoColor=white&labelColor=%233776AB">

<img alt="Static Badge" src="https://img.shields.io/badge/pyTelegramBotAPI-4.8.0-white?logo=telegram&logoColor=white&labelColor=%2326A5E4">

<img alt="Static Badge" src="https://img.shields.io/badge/peewee-3.16.0-white?logoColor=white&labelColor=gray">

</p>

<p align="center">
<img src="./readme_assets/main_page.png" width="100%"></p>

## Описание телеграмм-бота

__Find Hotel 2023__ - телеграмм-бот для поиска отелей по введенному пользователем названию города, предлагающий следующие функции:
* поиск самых дешёвых отелей;
* поиск самых дорогих отелей;
* поиск самых близко расположенных к центру города отелей с вводом ценового дипазаона;
* вывод истории поиска.
    
Для поиска отелей данный бот использует АPI сайта _https://www.hotels.com_

## Используемые сторонние библиотеки

* __pyTelegramBotAPI__ - вспомогательная библиотека для взаимодействия с API телеграмма
* __python-dotenv__ - библиотека для шифрования секретных данных
* __requests__ - библиотека для API-запросов
* __python-telegram-calendar__ - библиотека для добавления календаря в диалог бота, облегчающая процесс ввода дат
* __loguru__ - используется для логгирования
* __peewee__ - используется для подключения и работы с базой данных

## Настройка бота

Для работоспособности бота необходимо в корневом каталоге репозитория создать файл '.env' , куда с помощью
текстового редактора нужно скопировать следующий текст:
* __BOT_TOKEN__ = 'Ваш токен для бота, полученный от _@BotFather_'
* __RAPID_API_KEY__ = 'Ваш ключ полученный от API по адресу _rapidapi.com/apidojo/api/hotels4/_'
* __RAPID_API_HOST__ = 'hotels4.p.rapidapi.com'
    
## Обратная связь

По всем вопросам пишите мне на почту: 
<a href="mailto:israpal@bk.ru" rel="noopener noreferrer" class="link">Бекхан Исрапилов</a>

