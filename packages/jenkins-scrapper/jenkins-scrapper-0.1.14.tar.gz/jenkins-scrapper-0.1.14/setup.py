#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'jenkins-scrapper',
        version = '0.1.14',
        description = '',
        long_description = '',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = '',
        author_email = '',
        maintainer = '',
        maintainer_email = '',

        license = '',

        url = '',
        project_urls = {},

        scripts = [],
        packages = [],
        namespace_packages = [],
        py_modules = ['jenkins_scrapper'],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'astroid==2.5.6',
            'autopep8==1.5.7',
            'beautifulsoup4==4.9.3',
            'bs4==0.0.1',
            'certifi==2020.12.5',
            'chardet==4.0.0',
            'idna==2.10',
            'isort==5.8.0',
            'lazy-object-proxy==1.6.0',
            'lxml==4.6.3',
            'mccabe==0.6.1',
            'pycodestyle==2.7.0',
            'pylint==2.8.2',
            'requests==2.25.1',
            'rope==0.19.0',
            'soupsieve==2.2.1',
            'toml==0.10.2',
            'typed-ast==1.4.3',
            'urllib3==1.26.4',
            'wrapt==1.12.1'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
