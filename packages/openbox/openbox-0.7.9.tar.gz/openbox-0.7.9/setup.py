#!/usr/bin/env python
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import importlib.util
from pathlib import Path
from distutils.core import setup
from setuptools import find_packages


requirements = dict()
for extra in ["dev", "main"]:
    # Skip `package @ git+[repo_url]` because not supported by pypi
    requirements[extra] = [r
                           for r in Path("requirements/%s.txt" % extra).read_text().splitlines()
                           if '@' not in r
                           ]


# Find version number
spec = importlib.util.spec_from_file_location("openbox.pkginfo", str(Path(__file__).parent / "openbox" / "pkginfo.py"))
pkginfo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pkginfo)
version = pkginfo.version
package_name = pkginfo.package_name


def readme() -> str:
    return open("README.md").read()


setup(
    name=package_name,
    version=version,
    description="Efficient and generalized blackbox optimization (BBO) system",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/thomas-young-2013/open-box',
    author="Thomas (Yang) Li from DIR Lab@PKU",
    packages=find_packages(),
    license="MIT",
    install_requires=requirements["main"],
    extras_require={"dev": requirements["dev"]},
    package_data={"open-box": ["py.typed"]},
    include_package_data=True,
    python_requires='>=3.5.2',
    entry_points={
        "console_scripts": [
            "openbox = openbox.__main__:main",
        ]
    }
)
