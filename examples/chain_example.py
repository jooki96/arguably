from arguably import command, arg, run

@command("ping")
def ping():
    print("pong")

@command("echo")
@arg("text")
def echo(text):
    print(text)

if __name__ == "__main__":
    run(chain=True)
