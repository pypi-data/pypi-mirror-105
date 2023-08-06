# pydoni-cli
pydoni-cli is a Python library that serves as a command-line interface to custom-built tools developed by Andoni Sooklaris.

## Installation [WIP]

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pydoni-cli.

```bash
pip install pydoni-cli
```

## Usage

When pydoni-cli is installed, an executable `doni` is implicitly installed as well. This is the primary entry point to activating the custom-built tools included in each release of pydoni-cli.

`doni` is an executable built on top of `click` architecture, which supports multiple layers of command-line arguments. In the context of this module, these are referred to as *major* and *minor* command names.

As an example, should the user wish to run the script `doni imessage workflow-elt`, the command is broken into components as follows:

- `doni`: main executable entry point
- `imessage`: click command group for tools that deal with iMessage data, referred to as the *major* command name
- `workflow-elt`: specific click command to execute, referred to as the *minor* command name

Executing simpily `doni` will list all available major commands, and executing `doni {major}` will list all minor commands associated with the named major click command group. The flag `-h` or `--help` is available for all commands and will list the expectations for the chosen command's parameters, if there are any.

## The App

The `doni` executable includes command-line callable syntax for each specific minor command, but it also includes an interactive command-line app built with click and PyInquirer. This app allows the user to interactively select which tool they would like to use, modify parameters for that tool, and execute it.

As a result, each tool may be called either directly:

```bash
$ doni imessage workflow-elt
```

Or via the app interface:

```bash
$ doni
imessage  # User select via arrow keys
workflow-elt  # User select via arrow keys
# Modify parameters if desired, hit 'enter' to proceed
# Once 'enter' has been pressed, the `doni imessage workflow-elt {modified parameters if any}` command will be run
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

<div style="display: flex; justify-content: center;">
  <img src="graphics/logo.png" style="width: 300px; height: 300px;" />
</div>
