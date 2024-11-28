# Инструмент преобразования JSON в учебный конфигурационный язык

## Описание

Этот инструмент предназначен для преобразования данных из формата JSON в специализированный учебный конфигурационный язык. Данный инструмент позволяет загружать JSON-файлы и выводить их содержимое в другом формате, поддерживающем однострочные и многострочные комментарии, а также объявление и использование констант.

## Установка

1. Убедитесь, что у вас установлен Python версии 3.x.
2. Сохраните скрипт в файл, например, converter.py.

## Использование

1. Подготовьте JSON-файл с данными, которые вы хотите преобразовать. 
   
   Пример JSON-файла (example.json):
```
{
  "ключ1": "значение1",
  "ключ2": 42,
  "блок1": {
    "комментарий": "%Комментарий в одну строку",
    "ключ3": "значение3",
    "ключ4": 56
  },
  "константа": "число <- 100",
  "выражение": "|число|",
  "комментарий": "{#\nЭтот комментарий\nпродолжается на несколько строк\n#}",
  "словарь": {
    "вложенный_ключ": "вложенное_значение",
    "вложенный_ключ2": {
      "глубокий_ключ": 100
    }
  }
}
```

2. Запустите скрипт из командной строки, передав путь к вашему JSON-файлу:

      python converter.py example.json
   

3. Вывод преобразованного текста будет напечатан в стандартный вывод.

## Функции

- parsejsonfile(filepath)**: Читает JSON-файл и возвращает его содержимое как словарь.
- **converttoconfig(data)**: Преобразует словарь (JSON) в строчный формат учебного конфигурационного языка, добавляя поддержку комментариев и констант.

## Обработка ошибок

- Если JSON-файл имеет синтаксические ошибки, программа выведет сообщение об ошибке:
  ```
  Ошибка парсинга JSON: <описание ошибки>
  ```
- Если возникает ошибка преобразования, например, если встречается неизвестный тип значения, будет выведено следующее сообщение:
  ```
  Ошибка преобразования: <описание ошибки>
  ```

## Пример работы

Для приведенного выше JSON-файла вывод может выглядеть так:

```
@{
    ключ1 = значение1;
    ключ2 = 42;
    блок1 = @{
        %Комментарий в одну строку
        ключ3 = значение3;
        ключ4 = 56;
    }
    число <- 100
    число = 100
    {#
    Этот комментарий
    продолжается на несколько строк
    #}
    словарь = @{
        вложенный_ключ = вложенное_значение;
        вложенный_ключ2 = @{
            глубокий_ключ = 100;
        }
    }
}

```