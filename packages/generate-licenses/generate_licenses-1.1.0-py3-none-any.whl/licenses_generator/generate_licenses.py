"""
(C) Prisma 2021

Generate a file containing all (locally found) licenses from your project

CLI: generate_licenses.py -h

Recomanded:
    from generate_licenses import Generator, Template <- Or you can use
DefaultTemplate

    template = Template(
        wrapper_template='<div>\n$ctnt\n</div>',
        title_template='<h1>$ctnt</h1>\n',
        license_template='<pre>\n<code>\n$ctnt\n</code>\n</pre>'
    )

    generator = Generator(template, <initial_dir>, <out_file>, <out_separator>)
    generator.write_licenses()


Authors:
    David Pescariu <prisma.ro.official@gmail.com>

License:
    Copyright 2021 Prisma

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

__version__ = 1.0
__author__ = "David Pescariu @ Prisma"

import os
import sys
import time
import getopt
from typing import List

# Defaults:
INITIAL_DIR = 'node_modules'
OUT_FILE = 'LICENSES.txt'
OUT_SEPARATOR = '\n----------\n'

HELP_MSG = """
(C) Prisma 2021

Generate a file containing all (locally found) licenses from your project

Usage:
    -i <folder> --input <folder> : Initial directory to walk from
    -o <file>   --outfile <file> : File to write licenses to
    -d          --default : Run with default options
    -h          --help : Show this message

Note:
    When the CLI is used, the template will always be DefaultTemplate and the
    separator will be \\n----------\\n
"""


class License:
    def __init__(self, path: str, package_name: str) -> None:
        """
        Wrapper for a license file, holds the package_name (folder name)

        Args:
            path (str): License (relative) path
            package_name (str): node_modules/package_name <--
        """
        self.path = path
        self.package_name = package_name


class Template:
    def __init__(self, wrapper_template: str,
                 title_template: str, license_template: str
                 ) -> None:
        """
        Template for a written file. Each template must contain a $ctnt which
        is going to be replaced with the actual content.

        Args:
            license (License): License object
            wrapper_template (str, optional): Wraps the entire license.
            Defaults to None.
            title_template (str): Wraps the title
            license_template (str): Wraps the license

        Example:
```py
wrapper_template = '<div>\\n$ctnt\\n</div>'
title_template = '<h1>$ctnt</h1>\\n'
license_template = '<pre>\\n<code>\\n$ctnt\\n</code>\\n</pre>'
```
        Will generate the following:
```html
<div>
<h1>PACKAGE_NAME</h1>
<pre>
<code>
LICENSE
</code>
</pre>
</div>
```
        """
        self.license = None
        self.wrapper_template = wrapper_template
        self.title_template = title_template
        self.license_template = license_template

    def bind_license(self, license: License) -> None:
        """
        Bind a license to this instance

        Args:
            license (License): License to bind
        """
        self.license = license

    def get_wrapper_parts(self) -> List[str]:
        """
        Separate the wrapper from the $ctnt

        Returns:
            List[str]: [0] - Before $ctnt | [1] - After $ctnt
        """
        return self.wrapper_template.split('$ctnt')

    def get_title(self) -> str:
        """
        Get the package name

        Raises:
            Exception: If a license isn't bound to self.template

        Returns:
            str: Reprezentation
        """
        if self.license is None:
            raise Exception("License not binded to Template!")
        return self.title_template.replace('$ctnt', self.license.package_name)

    def get_license_parts(self) -> List[str]:
        """
        Separate the license "wrapper" from the $ctnt

        Returns:
            List[str]: [0] - Before $ctnt | [1] - After $ctnt
        """
        return self.license_template.split('$ctnt')


class DefaultTemplate(Template):
    def __init__(self) -> None:
        """
        Default template (the one in the example) for writing to the file.
        """
        super().__init__(
            wrapper_template='<div>\n$ctnt\n</div>',
            title_template='<h1>$ctnt</h1>\n',
            license_template='<pre>\n<code>\n$ctnt\n</code>\n</pre>'
        )


class Generator:
    def __init__(self, template: Template, initial_dir: str, out_file: str,
                 out_separator: str = ""
                 ) -> None:
        """
        Generate Licenses - Search for all LICENSE files in a given directory,
        and write them to a file.

        Args:
            template (Template): Template to follow
            initial_dir (str): Directory to walk from
            out_file (str): File to write licenses into
            out_separator (str, optional): Written in between licenses.
            Defaults to "".
        """
        print(
            f"Looking for licenses in {initial_dir} and writing to {out_file}")
        self.template = template
        self.initial_dir = initial_dir
        self.out_file = out_file
        self.out_separator = out_separator
        self.licenses: List[License] = Generator.find_licenses(
            self.initial_dir
        )

    def write_licenses(self) -> None:
        """
        Write licenses to the file using the given template
        """
        if len(self.licenses) == 0:
            print("Oops, no licenses found! Nothing to write...")
            return
        with open(self.out_file, 'w', encoding="utf8") as out_file:
            for license in self.licenses:
                self.template.bind_license(license)
                _wrapper = self.template.get_wrapper_parts()
                _title = self.template.get_title()
                _license = self.template.get_license_parts()

                with open(license.path, 'r', encoding="utf8") as in_file:
                    out_file.write(f"{_wrapper[0]}{_title}{_license[0]}")
                    for line in in_file:
                        out_file.write(line)
                    out_file.write(f"{_license[1]}{_wrapper[1]}")
                    out_file.write(f"\n{self.out_separator}\n")

    @staticmethod
    def is_license(file_name: str) -> bool:
        """
        Check (by name) if a given file is a license

        Args:
            file_name (str): File name

        Returns:
            bool: True if it matches to a license file, False otherwise
        """
        _name = file_name.lower()
        return _name.find("license") != -1

    @staticmethod
    def find_licenses(dir: str) -> List[License]:
        """
        Interate trough subfolders to find all license files

        Credits: https://stackoverflow.com/questions/19932130/iterate-through-folders-then-subfolders-and-print-filenames-with-path-to-text-f  # noqa: E501

        Args:
            dir (str): directory to search in

        Returns:
            List[License]: List with License objects
        """
        _licenses: List[License] = []
        for root, _, files in os.walk(dir):
            for name in files:
                if Generator.is_license(name):
                    package = root.replace('node_modules\\', '')
                    _licenses.append(
                        License(os.path.join(root, name), package))
        return _licenses


def run(initial_dir, out_file) -> None:
    start = time.perf_counter()
    print("(C) Prisma 2021 - License File Generator")

    generator = Generator(DefaultTemplate(), initial_dir,
                          out_file, OUT_SEPARATOR)
    generator.write_licenses()

    end = time.perf_counter()
    print(f"Done in {round((end - start), 3)} ms")


def main(argv):
    try:
        opts, args = getopt.getopt(
            argv, "hdi:o:", ["input=", "outfile=", "default", "help"])
    except getopt.GetoptError:
        print(HELP_MSG)
        sys.exit(1)

    initial_dir = INITIAL_DIR
    out_file = OUT_FILE

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(HELP_MSG)
            sys.exit(0)
        if opt in ('-d', "--default"):
            run(INITIAL_DIR, OUT_FILE)
            sys.exit(0)
        if opt in ('-i', "--input"):
            initial_dir = arg
        if opt in ('-o', "--outfile"):
            out_file = arg

    run(initial_dir, out_file)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
