from glob import glob
from os import chdir, makedirs
from os.path import basename, exists, join
from shutil import copy, copytree
from subprocess import run, PIPE
from sys import executable as python_executable, exit, platform, version_info
from typing import Callable

EXPECTED_PYTHON_VERSION = (3, 8)
DYN_EXT = {"win32": "dll", "unix": "so"}[platform]
IMP_EXT = {"win32": "lib", "unix": "a"}[platform]


def resolve_glob(expr: str):
    matches = glob(expr)
    if len(matches) != 1:
        raise RuntimeError(
            f"pattern `{expr}` caught {len(matches)} results, not one"
        )
    return matches[0]

        
class Action:
    def run(self):
        raise NotImplementedError()


class ChangeDirectory(Action):
    def __init__(self, dir):
        self.set_dir(dir)

    def __str__(self):
        return f"changing to {self._dir}"
        
    def set_dir(self, dir):
        if not exists(dir):
            raise BrokenActionException(f"dir {dir} does not exist")
        self._dir = dir
        
    def run(self):
        chdir(self._dir)
        

class RunCommand(Action):
    def __init__(self, command):
        self._command = command
        
    def __str__(self):
        command_line = " ".join(self._command)
        return f"running `{command_line}`"
        
    def run(self):
        result = run(self._command, stderr=PIPE, stdout=PIPE)
        if result.returncode != 0:
            print(result.stdout.decode())
            print(result.stderr.decode())
            raise ActionFailedException()


class Copy(Action):
    def __init__(self, src, dest):
        if isinstance(src, str):
            self._get_src = lambda: src
        elif isinstance(src, Callable):
            self._get_src = src
        else:
            raise TypeError()
        self._dest = dest
        
    def __str__(self):
        return f"copying {self._get_src()} to {self._dest}"


class CopyFile(Copy):     
    def run(self):
        copy(self._get_src(), self._dest)


class CopyFiles(Copy):
    def run(self):
        for match in glob(self._get_src()):
            copy(match, join(self._dest, basename(match)))
        

class CopyDirectory(Copy):
    def run(self):
        copytree(self._get_src(), self._dest, dirs_exist_ok=True)


class MakeDirectory(Action):
    def __init__(self, path):
        self._path = path
        
    def __str__(self):
        return f"creating directory {self._path}"

    def run(self):
        makedirs(self._path, exist_ok=True)
        

class RunPython(RunCommand):
    def __init__(self, args):
        super().__init__([python_executable, *args])


class BrokenActionException(ValueError):
    pass


class ActionFailedException(RuntimeError):
    pass


steps = [
    ChangeDirectory("crates/rugby-sum/"),
    RunCommand(("cargo", "build")),
    RunCommand(("cargo", "test")),
    RunCommand(("cargo", "clippy")),
    RunCommand(("cargo", "fmt", "--check")),
    RunCommand(("cargo", "build", "--release")),
    ChangeDirectory("../../"),

    CopyFile(f"crates/rugby-sum/target/release/rugby_sum.{DYN_EXT}",
             f"intermediate/rugby_sum.{DYN_EXT}"),
    CopyFile(f"crates/rugby-sum/target/release/rugby_sum.{DYN_EXT}.{IMP_EXT}",
             f"intermediate/rugby_sum.{DYN_EXT}.{IMP_EXT}"),

    CopyDirectory("packages/rugby/", "intermediate/"),
    ChangeDirectory("intermediate/"),
    
    RunPython(("setup.py", "build")),
    RunPython(("setup.py", "test")),

    CopyFile(f"rugby_sum.{DYN_EXT}", "../release"),
    CopyFile(lambda: resolve_glob("rugby_binding.*.pyd"), "../release"),
    MakeDirectory("../release/rugby"),

    CopyFiles("rugby/*.py", "../release/rugby"),

    ChangeDirectory("../"),
]

if __name__ == "__main__":
    if (version_info.major, version_info.minor) < EXPECTED_PYTHON_VERSION:
        print(
            f"requires at least python version {EXPECTED_PYTHON_VERSION}. "
            f"got version {version_info}"
        )
        exit(1)

    for step in steps:
        print(f"- {step}")
        step.run()