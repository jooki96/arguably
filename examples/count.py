from arguably import command, arg, run, main

@command("count")
@main
@arg("file", short="f")
def count(file):
    with open(file, "r", encoding="utf-8") as f:
        print(sum(1 for _ in f))

if __name__ == "__main__":
    run() 

# usage:
#   python count.py --file myfile.txt  
#       → 44
    
#   python count.py count --file myfile.txt
#       → 44