import json
import unittest
from io import StringIO
import sys

# Импортируем функции из вашего кода
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

class TestJsonToConfig(unittest.TestCase):

    def test_simple_json(self):
        json_data = {
            "name": "example",
            "version": 1,
            "settings": {
                "enabled": True,
                "timeout": 30
            }
        }
        expected_output = "@{\n    name = example;\n    version = 1;\n    settings = @{\n        enabled = True;\n        timeout = 30;\n    }\n}"
        output = convert_to_config(json_data)
        self.assertEqual(output, expected_output)

    def test_nested_json(self):
        json_data = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {
                    "username": "admin",
                    "password": "secret"
                }
            }
        }
        expected_output = "@{\n    database = @{\n        host = localhost;\n        port = 5432;\n        credentials = @{\n            username = admin;\n            password = secret;\n        }\n    }\n}"
        output = convert_to_config(json_data)
        self.assertEqual(output, expected_output)

    def test_special_string_handling(self):
        json_data = {
            "constant": "MY_VAR <- value",
            "reference": "|MY_VAR|"
        }
        expected_output = "@{\n    MY_VAR <- value\n    MY_VAR = value\n}"
        output = convert_to_config(json_data)
        self.assertEqual(output, expected_output)

    def test_numeric_values(self):
        json_data = {
            "integer": 42,
            "float": 3.14
        }
        expected_output = "@{\n    integer = 42;\n    float = 3.14;\n}"
        output = convert_to_config(json_data)
        self.assertEqual(output, expected_output)

    def test_error_handling(self):
        json_data = {
            "invalid": object()  # Неправильный тип
        }
        with self.assertRaises(ValueError):
            convert_to_config(json_data)

if __name__ == "__main__":
    unittest.main()
