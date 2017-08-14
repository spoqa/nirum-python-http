import ast
import os
import re
import sys

from setuptools import find_packages
from setuptools import setup, __version__ as setuptools_version


def readme(name='README.rst'):
    try:
        with open(name) as f:
            rst = f.read()
        return re.sub(
            r'(^|\n).. include::\s*([^\n]+)($|\n)',
            lambda m: m.group(1) + (readme(m.group(2)) or '') + m.group(3),
            rst
        )
    except (IOError, OSError):
        return


def get_version():
    module_path = os.path.join(os.path.dirname(__file__),
                               'nirum_http', '__init__.py')
    module_file = open(module_path)
    try:
        module_code = module_file.read()
    finally:
        module_file.close()
    tree = ast.parse(module_code, module_path)
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target, = node.targets
        if isinstance(target, ast.Name) and target.id == '__version__':
            value = node.value
            if isinstance(value, ast.Str):
                return value.s
            raise ValueError('__version__ is not defined as a string literal')
    raise ValueError('could not find __version__')


setup_requires = []
install_requires = [
    'nirum >= 0.6.0',
    'requests >= 2.11.1',
    'six',
]
tests_require = [
    'flake8-import-order >= 0.12, < 1.0',
    'flake8-import-order-spoqa >= 1.0.1, < 2.0.0',
    'pytest >= 3.1.2, < 4.0.0',
    'pytest-flake8 >= 0.8.1, < 1.0.0',
    'requests-mock >= 1.3.0, < 1.4.0',
]
extras_require = {
    'tests': tests_require,
}
below35_requires = [
    'typing',
]
async_require = [
    'aiohttp',
]
async_test_require = [
    'pytest-aiohttp >= 0.1.3, < 1.2.0',
    'aiotools >= 0.4.3, < 0.5.0',
]

if 'bdist_wheel' not in sys.argv and sys.version_info < (3, 5):
    install_requires.extend(below35_requires)

if sys.version_info >= (3, 5):
    tests_require.extend(async_test_require)


if tuple(map(int, setuptools_version.split('.'))) < (17, 1):
    setup_requires = ['setuptools >= 17.1']
    extras_require.update({":python_version=='3.4'": below35_requires})
    extras_require.update({":python_version=='2.7'": below35_requires})
else:
    extras_require.update({":python_version<'3.5'": below35_requires})
    extras_require.update({":python_version>='3.5'": async_require})


setup(
    name='nirum-http',
    version=get_version(),
    description='Nirum HTTP transport for Python',
    long_description=readme(),
    url='https://github.com/spoqa/nirum-python-http',
    author='Kang Hyojun',
    author_email='iam.kanghyojun' '@' 'gmail.com',
    license='MIT license',
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    extras_require=extras_require
)
