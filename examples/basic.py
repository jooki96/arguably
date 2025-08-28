from arguably import command, arg, flag, run

@command("ping")
def ping():
    print("pong")

@command("greet")
@arg("name")
@flag("shout", short="s")
def greet(name, shout):
    msg = f"Hello, {name}"
    if shout:
        msg = msg.upper()
    print(msg)

if __name__ == "__main__":
    run()


# Usage:
#   python app.py ping
#     → pong
#
#   python app.py greet --name Alice
#     → Hello, Alice
#
#   python app.py greet --name Alice -s
#     → HELLO, ALICE