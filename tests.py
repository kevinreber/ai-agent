# from functions.write_file import write_file
from functions.run_python_file import run_python_file


def test():
    print("Starting tests...")
    result = run_python_file("calculator", "main.py")
    print(result)
    result = run_python_file("calculator", "tests.py")
    print(result)
    result = run_python_file("calculator", "../main.py")
    print(result)
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print("Tests completed")

if __name__ == "__main__":
    test()
