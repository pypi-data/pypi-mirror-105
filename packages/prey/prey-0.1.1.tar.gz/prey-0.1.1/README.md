# prey
```py
#!/usr/bin/env prey

async def main():
    await _("cat pyproject.toml | grep name")

    branch = await _("git branch --show-current")
    await _(f"dep deploy --branch={branch}")

    await _(
        [
            "sleep 1; echo 1",
            "sleep 2; echo 2",
            "sleep 3; echo 3",
        ]
    )

    name = "foo bar"
    await _(f"mkdir /tmp/${name}")
```

A tool for writing shell scripts in Python. Inspired by [google/zx](https://github.com/google/zx). This package provides a wrapper around `asyncio.subprocess` and escapes arguments.


## Install
```bash
pip install prey
```

## Documentation
Wrap your scripts in an async function called **`main`**:
```py
async def main():
    # script...
```
It must be called `main` as the executable looks for a function calls main and calls it. This is used so commands can be asynchronous.

You can add the shebang at the top of your script:
```py
#!/usr/bin/env prey
```
and run it like so:
```bash
chmod +x ./script.py
./script.py
```

Or via the `prey` executable:
```bash
prey ./script.py
```
When using `prey` via the executable or a shebang, all of the functions (`_`, `colorama`, `request`, etc) are available wihtout any imports.

### `await _("command")`
Asychronously executes a given string using the `create_subprocess_shell` function from the `asyncio.subprocess` module and returns the output.
```py
count = int(await _("ls -1 | wc -l"))
print(f"Files count: {count}")
```

### `cd("filepath")`
Changes the current working directory.
```py
cd("/tmp")
await _('pwd') # outputs /tmp
```

### colorama package
The [colorama]() package is available without importing inside scripts.
```py
print(f"{colorama.Fore.BLUE}Hello World!")
```

### request package
A wrapper around aiohttp, [aiohttp-requests](https://pypi.org/project/aiohttp-requests/)`.requests.session.request`, is available without importing inside scripts.
```py
response = await request("get", "http://python.org")
html = await response.text()
```

### Importing from other scripts
It is possible to make use of `_` and other functions via explicit imports:
```py
#!/usr/bin/env prey
from prey import _
await _('date')
```

### Passing env variables
```py
os.environ["FOO"] = "bar"
await _('echo $FOO')
```