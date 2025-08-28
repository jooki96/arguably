# arguably — tiny decorator-based CLI
A lightweight, readable, decorator-first library on top of 'argsparse' that helps you quickly create CLI apps by wrapping functions with decorators.


## API
- `@command(name)` — register a subcommand
- `@arg(param_name, cli_name=None, *, type=str, default=None, short=None)` — named argument
- `@parg(param_name, *, type=str)` — positional argument
- `@flag(flag_name, *, short=None, default=False)` — boolean flag
- `@main` — default command when no command is passed
- `run(argv=None, chain=False)` — execute the CLI

---

## Example Usage

### Basic Example
```python
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
```

Run it:
```bash
python app.py ping
# pong

python app.py greet --name Alice
# Hello, Alice

python app.py greet --name Alice -s
# HELLO, ALICE
```

---

### Compress Example
```python
import gzip, shutil
from arguably import command, parg, main, run

@command("compress")
@main
@parg("src")
@parg("dst")
def compress(src, dst):
    with open(src, "rb") as f_in, gzip.open(dst, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"Compressed {src} -> {dst}")

@command("decompress")
@parg("src")
@parg("dst")
def decompress(src, dst):
    with gzip.open(src, "rb") as f_in, open(dst, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"Decompressed {src} -> {dst}")

if __name__ == "__main__":
    run()
```

Run it:
```bash
python compress.py input.txt output.txt.gz
# Compressed input.txt -> output.txt.gz

python compress.py decompress output.txt.gz recovered.txt
# Decompressed output.txt.gz -> recovered.txt
```

---
