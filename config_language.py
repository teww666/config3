import yaml
import argparse
import re

def process_global_constants(yaml_data):
    """
    Обрабатывает глобальные константы из YAML-данных.
    """
    constants = {}
    for key, value in yaml_data.items():
        if isinstance(key, str) and key.startswith("global "):
            name = key.split(" ", 1)[1]
            constants[name] = value
    return constants

def evaluate_expression(expr, constants):
    """
    Вычисляет значение константного выражения в префиксной форме.
    """
    match = re.match(r"@\[(.+)\]", expr)
    if not match:
        return expr  # Если это не выражение для вычисления
    expression = match.group(1).strip()

    tokens = expression.split()
    if len(tokens) < 2:
        raise ValueError(f"Некорректное выражение: '{expr}'")

    operator = tokens[0]
    operands = tokens[1:]

    # Поддержка базовых операций
    if operator == "+":
        if len(operands) != 2:
            raise ValueError(f"Операция '+' требует двух операндов: '{expr}'")
        infix_expr = f"{operands[0]} + {operands[1]}"
    elif operator == "abs":
        if len(operands) != 1:
            raise ValueError(f"Операция 'abs' требует одного операнда: '{expr}'")
        infix_expr = f"abs({operands[0]})"
    else:
        raise ValueError(f"Неизвестная операция: '{operator}'")

    # Подстановка значений из констант
    for const, value in constants.items():
        infix_expr = infix_expr.replace(const, str(value))

    try:
        # Вычисление результата
        result = eval(infix_expr, {"__builtins__": None}, {"abs": abs})
        return result
    except Exception as e:
        raise ValueError(f"Ошибка вычисления выражения '{expr}': {e}")

def process_value(value, constants, depth=0, is_variable=True):
    """
    Рекурсивно обрабатывает значение, преобразуя вложенные структуры и вычисляя выражения.
    """
    indent = "    " * depth  # Отступы для вложенности

    # Применяем шаблон в зависимости от типа данных
    if isinstance(value, str) and value.startswith("@["):
        return f"{evaluate_expression(value, constants)};"  # Добавляем точку с запятой для выражений
    elif isinstance(value, dict):
        # Для словаря обрабатываем ключи и значения, включая точку с запятой
        dict_lines = "\n".join(f"{indent}    {k} : {process_value(v, constants, depth + 1, is_variable=False)}" for k, v in value.items())
        return f"{{\n{dict_lines}\n{indent}}}"  # Добавляем фигурные скобки вокруг значений словаря
    elif isinstance(value, list):
        # Обрабатываем массивы
        list_lines = "\n".join(f"{indent}    {process_value(v, constants, depth + 1, is_variable=False)}" for v in value)
        return f"{{\n{list_lines}\n{indent}}}"  # Добавляем фигурные скобки вокруг массива
    elif isinstance(value, str):  # Обрабатываем строки
        return f"\"{value.strip()}\";"  # Убираем пробелы внутри строки и добавляем кавычки
    else:
        # Если это переменная, сохраняем шаблон (переменная: значение)
        if is_variable:
            return f"{value};"  # Просто значение для переменной
        else:
            return f"{value};"  # Для других случаев тоже добавляем точку с запятой

def convert_to_custom_language(yaml_data):
    """
    Преобразует YAML-данные в учебный конфигурационный язык.
    """
    constants = process_global_constants(yaml_data)
    output_lines = []

    for key, value in yaml_data.items():
        if isinstance(key, str) and key.startswith("global "):
            continue  # Пропускаем глобальные константы

        # Проверяем, если значение является словарем, то обрабатываем его иначе как переменную
        if isinstance(value, dict):
            processed_value = process_value(value, constants, depth=1, is_variable=False)  # Для словаря обрабатываем только значения
            output_lines.append(f"{processed_value}")  # Добавляем словарь без ключей
        else:
            processed_value = process_value(value, constants, depth=1)  # Для обычных переменных
            output_lines.append(f"{key} : {processed_value}")  # Переменные с двоеточием и значением

    return "\n".join(output_lines)

def main():
    parser = argparse.ArgumentParser(description="Преобразование YAML в учебный конфигурационный язык")
    parser.add_argument("-i", "--input", required=True, help="Путь к входному YAML-файлу")
    parser.add_argument("-o", "--output", required=True, help="Путь к выходному файлу")

    args = parser.parse_args()

    try:
        # Чтение YAML-файла
        with open(args.input, 'r', encoding='utf-8') as infile:
            yaml_data = yaml.safe_load(infile)

        # Преобразование
        result = convert_to_custom_language(yaml_data)

        # Запись в выходной файл
        with open(args.output, 'w', encoding='utf-8') as outfile:
            outfile.write(result)

        print(f"Преобразование успешно. Результат записан в {args.output}")

    except yaml.YAMLError as e:
        print(f"Ошибка в YAML-файле: {e}")
    except ValueError as e:
        print(f"Синтаксическая ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
