# Парсер данных с сайта yadonor.ru

Бесплатный проект для движения донорства крови в России.

Получаем json файл с данными по каждому пункту сдачи крови в стране. 
Данные содержат названия пункта, адрес, конакты и донорский светофор
потребностей той или иной группы крови.

## Установка:

Создаем виртуальное окружение командой:
linux: ```python3 -m venv venv```
windows: ```PY -m venv venv```

## Активируем виртуальное окружение:
linux: ```source venv/bin/activate```
windows: ```cd venv/Scripts```
         ```activate```
         
## Устанавливаем зависимости:
```pip3 install -r requirements.txt```

## Запускаем скрипт:
```python3 parser.py```
