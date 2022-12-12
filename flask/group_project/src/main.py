import sys
from menu import menu_loop
from parse import load_html

def main(argv): 
    load_html(argv)
    menu_loop()
    return 0

if __name__ == '__main__':
    main(sys.argv)
