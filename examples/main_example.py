

from arguably import main, command, run

@main
def default():
    print("This is the default command")

@command("verbose")
def verbose():
    print("This is the verbose command")

if __name__ == "__main__":
    run() 


''' if you run it without giving any arguments it will call the function
    with the main decorator. in this case default() '''

# usage:
#   python main_example.py
#       → This is a default command 
# python main_example.py --verbose
#       → This is a verbose command