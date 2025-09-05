from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

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

#show_dir("current directory", "calculator", ".")
#show_dir("'pkg' directory", "calculator", "pkg")
#show_dir("'/bin' directory", "calculator", "/bin")
#show_dir("'../' directory", "calculator", "../")

#show_file("lorem.txt", "calculator", "lorem.txt" )
show_file("main.py", "calculator", "main.py")
show_file("calculator.py", "calculator", "pkg/calculator.py")
show_file("'/bin/cat'", "calculator", "/bin/cat")
show_file("does_not_exist.py", "calculator", "pkg/does_not_exist.py")
