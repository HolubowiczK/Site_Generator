from filescopy import copy_files
from generategape import generate_pages_recursive

def main():
    source = './static'
    destination = './public'
    copy_files(source, destination)

    generate_pages_recursive('./content/', './template.html', './public/')

if __name__ == "__main__":
    main()