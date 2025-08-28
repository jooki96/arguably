"""
arguably — tiny decorator-based CLI for Python
(Refactor: readable, lightweight, decorator-first)

API:
@command("name", help=None, description=None)
@arg(param_name, cli_name=None, *, type=str, required=True, default=None, short=None, choices=None, help=None)
@parg(param_name, *, type=str, help=None)
@flag(flag_name, *, short=None, default=False, help=None)
@main
run(argv=None, chain=False)
"""

import argparse
import shlex
import sys
from functools import wraps

__all__ = ["command", "arg", "parg", "flag", "main", "run"]

_COMMANDS = {}
_DEFAULT = None


def _ensure_meta(func):
    if not hasattr(func, "_arguably_args"):
        func._arguably_args = []   # list of dicts for options
    if not hasattr(func, "_arguably_pargs"):
        func._arguably_pargs = []  # list of dicts for positionals
    if not hasattr(func, "_arguably_flags"):
        func._arguably_flags = []  # list of dicts for flags
    return func


def command(name, help=None, description=None):
    """Register a subcommand."""
    def deco(func):
        _ensure_meta(func)
        func._arguably_command = name
        _COMMANDS[name] = {
            "func": func,
            "args": func._arguably_args,
            "pargs": func._arguably_pargs,
            "flags": func._arguably_flags,
            "help": help or f"{name} command",
            "description": description,
        }

        @wraps(func)
        def wrapper(*a, **kw):
            return func(*a, **kw)
        return wrapper
    return deco


def arg(param_name, cli_name=None, *, type=str, required=True,
        default=None, short=None, choices=None, help=None):
    """Define an optional (named) argument that becomes a kwarg."""
    def deco(func):
        _ensure_meta(func)
        func._arguably_args.append({
            "param": param_name,
            "cli": (cli_name or param_name).replace("_", "-"),
            "type": type,
            "required": required if default is None else False,
            "default": default,
            "short": short,
            "choices": choices,
            "help": help,
        })
        return func
    return deco


def parg(param_name, *, type=str, help=None):
    def deco(func):
        _ensure_meta(func)
        func._arguably_pargs.insert(0, {   # we insert at the front because the decorator reads pargs bottom up
            "param": param_name,
            "type": type,
            "help": help,
        })
        return func
    return deco


def flag(flag_name, *, short=None, default=False, help=None):
    """Define a boolean flag (store_true)."""
    def deco(func):
        _ensure_meta(func)
        func._arguably_flags.append({
            "name": flag_name.replace("_", "-"),
            "short": short,
            "default": bool(default),
            "help": help,
        })
        return func
    return deco


def main(func):
    """Mark a function to run when no command is given."""
    global _DEFAULT
    _ensure_meta(func)
    _DEFAULT = {
        "func": func,
        "args": func._arguably_args,
        "pargs": func._arguably_pargs,
        "flags": func._arguably_flags,
        "help": "default command",
        "description": None,
    }
    return func


def _build_parser_for(cmd_name, meta):
    p = argparse.ArgumentParser(
        prog=cmd_name,
        description=meta.get("description") or meta.get("help") or cmd_name,
    )

    # Named options
    for a in meta["args"]:
        names = []
        if a["short"]:
            names.append(f"-{a['short']}")
        names.append(f"--{a['cli']}")
        kwargs = {
            "dest": a["param"],
            "required": a["required"],
            "type": a["type"],
            "help": a["help"],
            "default": a["default"],
        }
        if a["choices"] is not None:
            kwargs["choices"] = a["choices"]
        p.add_argument(*names, **{k: v for k, v in kwargs.items() if v is not None})

    # Positionals (do NOT pass dest; argparse derives it from the name)
    for pa in meta["pargs"]:
        p.add_argument(pa["param"], type=pa["type"], help=pa["help"])

    # Flags
    for fl in meta["flags"]:
        names = []
        if fl["short"]:
            names.append(f"-{fl['short']}")
        names.append(f"--{fl['name']}")
        p.add_argument(*names, dest=fl["name"].replace("-", "_"),
                       action="store_true", default=fl["default"], help=fl["help"])

    return p


def _print_top_help():
    print("Usage: <program> <command> [options]\n")
    if _COMMANDS:
        print("Available commands:")
        width = max(len(k) for k in _COMMANDS) if _COMMANDS else 0
        for name, meta in sorted(_COMMANDS.items()):
            summary = meta.get("help") or ""
            print(f"  {name.ljust(width)}  {summary}")
    if _DEFAULT:
        print("\nA default command is defined; running with no command will execute it.")


def _dispatch(argv):
    """Parse argv for a single command and execute it."""
    if not argv:
        if _DEFAULT:
            meta = _DEFAULT
            parser = _build_parser_for("<default>", meta)
            ns = parser.parse_args([])
            return meta["func"](**vars(ns))
        else:
            _print_top_help()
            return

    cmd = argv[0]
    if cmd not in _COMMANDS:
        if _DEFAULT is None:
            print(f"Unknown command: {cmd!r}\n")
            _print_top_help()
            return
        # Treat whole argv as default's args
        meta = _DEFAULT
        parser = _build_parser_for("<default>", meta)
        ns = parser.parse_args(argv)
        return meta["func"](**vars(ns))

    meta = _COMMANDS[cmd]
    parser = _build_parser_for(cmd, meta)
    ns = parser.parse_args(argv[1:])
    return meta["func"](**vars(ns))


def run(argv=None, chain=False):
    """
    Execute CLI.
    - argv: pass a custom list for testing; defaults to sys.argv[1:]
    - chain: when True, split tokens by scanning for known command names.
      NOTE: a value equal to a command name will start a new block.
    """
    if argv is None:
        argv = sys.argv[1:]

    if not chain:
        return _dispatch(argv)

    tokens = shlex.split(" ".join(argv))
    blocks, current = [], []
    for t in tokens:
        if t in _COMMANDS:
            if current:
                blocks.append(current)
            current = [t]
        else:
            current.append(t)
    if current:
        blocks.append(current)

    result = None
    for b in blocks:
        result = _dispatch(b)
    return result
