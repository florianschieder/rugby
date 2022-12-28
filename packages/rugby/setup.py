#!/usr/bin/python3

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

extensions = {
    "rugby_binding": {
        "sources": [
            "rugby/binding.c",
        ],
        "extra_compile_args": {
            "msvc": [
                "/WX",
            ],
            "unix": [
                "-Werror",
            ],
        },
        "extra_link_args": {
            "msvc": [
                "rugby_sum.lib",
                "rugby_greet.lib",
                "WS2_32.lib",
                "Bcrypt.lib",
                "Userenv.lib",
                "Advapi32.lib",
            ],
            "unix": [
                "librugby_sum.a",
                "librugby_greet.a",
            ],
        },
    }
}


class ExtraCompileArgsExtension(build_ext):
    def build_extension(self, ext: Extension):
        ctype = self.compiler.compiler_type
        ext.extra_compile_args = extensions[ext.name].get("extra_compile_args")[ctype]
        ext.extra_link_args = extensions[ext.name].get("extra_link_args")[ctype]
        build_ext.build_extension(self, ext)


setup(
    name="rugby",
    version="0.1.0",
    license="GNU GPLv3",

    description="Rust/Python interop illustration",
    author="Florian Schieder",
    author_email="florian.schieder@web.de",

    packages=[
        "rugby",
    ],
    ext_modules=[
        Extension(it[0], **it[1])
        for it in extensions.items()
    ],
    cmdclass={'build_ext': ExtraCompileArgsExtension},
)
