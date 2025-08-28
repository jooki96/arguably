# arguably — tiny decorator-based CLI

A lightweight, readable, decorator-first wrapper around `argparse`. No magic, no dependencies.

## Install (dev)
```bash
pip install -e .
```

## API
- `@command(name, help=None, description=None)` — register a subcommand
- `@arg(param_name, cli_name=None, *, type=str, required=True, default=None, short=None, choices=None, help=None)`
- `@parg(param_name, *, type=str, help=None)` — positional argument
- `@flag(flag_name, *, short=None, default=False, help=None)` — boolean flag
- `@main` — default command when no command is passed
- `run(argv=None, chain=False)` — execute the CLI
