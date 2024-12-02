# Учебный инструмент для работы с конфигурационным языком

Этот проект реализует инструмент командной строки для преобразования YAML-файлов в учебный конфигурационный язык с поддержкой вычисления констант, вложенных структур и проверки синтаксических ошибок.

---

## **Функциональность**

- Принимает на вход YAML-файл.
- Преобразует YAML-структуру в конфигурационный язык, поддерживающий:
  - **Глобальные константы**: `global имя = значение`.
  - **Словари**: вложенные структуры вида `{ ключ : значение; ... }`.
  - **Константные выражения** в префиксной форме, например: `@[+ x 10]` или `@[abs -5]`.
- Выводит преобразованный текст в файл с учетом всех синтаксических правил.
- Обрабатывает ошибки входного формата и выводит их в понятной форме.

---

## **Запуск**
Запуск инструмента
```bash
python config_language.py -i <input_file.yaml> -o <output_file.txt>
```
-i или --input: путь к входному YAML-файлу.
-o или --output: путь для сохранения преобразованного файла.
Пример команды
```bash
python config_language.py -i examples.yaml -o output.txt
```
### Примеры
Входной файл examples.yaml:
```yaml
global max_connections: 100
global timeout: 30
server:
  name: "ExampleServer"
  settings:
    connections: "@[+ max_connections 50]"
    timeout: "@[abs -timeout]"
    nested_config:
      cache_size: 256
      log_level: "INFO"
```
Выходной файл output.txt:
```css
server : {
name : ExampleServer;
settings : {
connections : 150;
timeout : 30;
nested_config : {
cache_size : 256;
log_level : INFO;
};
};
};
```
### Тестирование
Запуск тестов
В проекте есть тестовый файл test_config_language.py, который проверяет все ключевые возможности инструмента.
Запустите тесты командой:
```bash
python test_config_language.py
```
Результат тестирования
Тесты покрывают:
Простые и вложенные структуры.
Обработку глобальных констант.
Вычисление выражений.
Ошибочные выражения.
Пример успешного выполнения:

```scss
Running Tests...
[PASS] Flat Structure
[PASS] Nested Structure
[PASS] Constants and Expressions
[PASS] Absolute Value Expression
[PASS] Invalid Expression
```
![Скриншот результата](photo/Снимок%20экрана%202024-12-02%20224842.png)# config3
