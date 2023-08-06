__version__ = "0.1.1"

import asyncio
from asyncio.subprocess import PIPE
from os import chdir
import sys
from typing import Union

Command = Union[str, bytes]


async def execute_one(cmd: Command):
    print(f"$ {cmd}")
    proc = await asyncio.subprocess.create_subprocess_shell(
        cmd, stdout=PIPE, stderr=PIPE
    )

    output = (await proc.stdout.read()).decode("utf-8")
    sys.stdout.write(output)

    return output


async def execute_many(cmds: list[Command]):
    return await asyncio.gather(*[execute_one(cmd) for cmd in cmds])


async def execute(cmd: Union[Command, list[Command]]):
    if type(cmd) == list:
        return await execute_many(cmd)

    return await execute_one(cmd)


_ = execute


def cd(filepath: str):
    chdir(filepath)
