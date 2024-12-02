import yaml
from config_language import convert_to_custom_language, process_global_constants, evaluate_expression

def run_test(test_name, actual, expected):
    """
    Запускает тест и сравнивает фактический и ожидаемый результат.
    """
    if actual.strip() == expected.strip():
        print(f"[PASS] {test_name}")
    else:
        print(f"[FAIL] {test_name}")
        print("EXPECTED:")
        print(expected)
        print("ACTUAL:")
        print(actual)

def test_flat_structure():
    yaml_data = {
        "config": {
            "param1": 10,
            "param2": 20
        }
    }
    expected = """{
        param1 : 10;
        param2 : 20;
    }"""
    result = convert_to_custom_language(yaml_data)
    run_test("Flat Structure", result, expected)

def test_nested_structure():
    yaml_data = {
        "config": {
            "param1": 10,
            "nested": {
                "key1": "value1",
                "key2": "value2"
            }
        }
    }
    expected = """{
        param1 : 10;
        nested : {
            key1 : "value1";
            key2 : "value2";
        }
    }"""
    result = convert_to_custom_language(yaml_data)
    run_test("Nested Structure", result, expected)

def test_constants():
    yaml_data = {
        "global x": 10,
        "global y": 5,
        "config": {
            "result": "@[+ x y]"
        }
    }
    expected = """{
        result : 15;
    }"""
    result = convert_to_custom_language(yaml_data)
    run_test("Constants and Expressions", result, expected)

def test_expression_abs():
    yaml_data = {
        "global z": -50,
        "config": {
            "absolute": "@[abs z]"
        }
    }
    expected = """{
        absolute : 50;
    }"""
    result = convert_to_custom_language(yaml_data)
    run_test("Absolute Value Expression", result, expected)

def test_invalid_expression():
    yaml_data = {
        "config": {
            "invalid": "@[unknown_operator 10]"
        }
    }
    try:
        convert_to_custom_language(yaml_data)
        print("[FAIL] Invalid Expression")
    except ValueError:
        print("[PASS] Invalid Expression")

if __name__ == "__main__":
    print("Running Tests...")
    test_flat_structure()
    test_nested_structure()
    test_constants()
    test_expression_abs()
    test_invalid_expression()
