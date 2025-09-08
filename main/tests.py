from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def show_dir(title, wd, dir_):
    print(f"Result for {title}:")
    result = get_files_info(wd, dir_)
    if result:
        print("  " + result.replace("\n", "\n "))


def show_file(title, wd, fp):
    print(f"Result for {title}:")
    result = get_file_content(wd, fp)
    len_result = len(result)
    if result:
        print(result)

def show_write(t, wd, fp, c):
    print(f"Result for {t}: ")
    result = write_file(wd, fp, c)
    if result:
        print("  " + result.replace("\n", "\n "))

def show_run(title, wd, fp, args=[]):
    print(f"Result for {title}:")
    result = run_python_file(wd, fp, args)
    if result:
        print("  " + result.replace("\n", "\n "))


#show_dir("current directory", "calculator", ".")
#show_dir("'pkg' directory", "calculator", "pkg")
#show_dir("'/bin' directory", "calculator", "/bin")
#show_dir("'../' directory", "calculator", "../")

#show_file("lorem.txt", "calculator", "lorem.txt" )
#show_file("main.py", "calculator", "main.py")
#show_file("calculator.py", "calculator", "pkg/calculator.py")
#show_file("'/bin/cat'", "calculator", "/bin/cat")
#show_file("does_not_exist.py", "calculator", "pkg/does_not_exist.py")

#show_write("lorem.txt", "calculator", "lorem.txt", "wait, this isn't lorem ipsum")
#show_write("morelorem.txt", "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
#show_write("temp.txt", "calculator", "/tmp/temp.txt", "this should not be allowed")

show_run("main.py", "calculator", "main.py")
show_run("main.py + args","calculator", "main.py", ["3 + 5"])
show_run("test.py","calculator", "tests.py")
show_run("../main.py","calculator", "../main.py")
show_run("nonexistent.py","calculator", "nonexistent.py")
