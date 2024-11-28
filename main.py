import json
import sys


def parse_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def convert_to_config(data):
    result = ['@{']
    constants = {}

    def convert_item(key, value, deep=1):
        if isinstance(value, dict):
            result.append('    ' * deep + f"{key} = @{{")
            for k, v in value.items():
                convert_item(k, v, deep + 1)
            result.append('    ' * deep + f"}}")
        elif isinstance(value, str) and value.startswith('%'):
            result.append('    ' * deep + value)
        elif isinstance(value, str) and value.startswith('{#'):
            strings = value.split('\n')
            for string in strings:
                result.append('    ' * deep + string)
        elif isinstance(value, str) and '<-' in value:
            new_key, new_value = value.split('<-')[0].replace(' ', ''), value.split('<-')[1].replace(' ', '')
            constants[new_key] = new_value
            result.append('    ' * deep + value)
        elif isinstance(value, str) and value.startswith('|') and value.endswith('|'):
            search_value = value[1:-1]
            if search_value in constants:
                result.append('    ' * deep + search_value + ' = ' + constants[search_value])
            else:
                result.append('    ' * deep + 'None')
        elif isinstance(value, (int, float)):
            result.append('    ' * deep + f"{key} = {value};")
        elif isinstance(value, str):
            result.append('    ' * deep + f"{key} = {value};")
        else:
            raise ValueError(f"Неизвестный тип значения для ключа '{key}': {type(value)}")

    for key, value in data.items():
        convert_item(key, value)

    result.append('}')

    return "\n".join(result)


def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <путь_к_json_файлу>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        json_data = parse_json_file(file_path)
        config_output = convert_to_config(json_data)
        print(config_output)
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
    except ValueError as e:
        print(f"Ошибка преобразования: {e}")


if __name__ == "__main__":
    main()
