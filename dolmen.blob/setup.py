# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.blob'
version = '0.5.0'
readme = open(join('src', 'dolmen', 'blob', "README.txt")).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'ZODB3 >= 3.9.0',
    'dolmen.builtins >= 0.3.1',
    'dolmen.file >= 0.5.1',
    'grokcore.component',
    'grokcore.view',
    'setuptools',
    'zope.component >= 3.9.1',
    'zope.contenttype',
    'zope.copy >= 3.5.0',
    'zope.file',
    'zope.filerepresentation',
    'zope.interface',
    'zope.location >= 3.7.0',
    'zope.mimetype',
    'zope.publisher',
    'zope.schema',
    ]

tests_require = [
    'transaction',
    'zope.container',
    'zope.size',
    'zope.testing',
    'zope.security',
    'zope.traversing',
    'zope.app.testing',
    'zope.app.appsetup',
    ]

setup(name=name,
      version=version,
      description='Dolmen zodb blob handlers',
      long_description=readme + '\n\n' + history,
      keywords='Grok Zope3 CMS Dolmen',
      author='Souheil Chelfouh',
      author_email='trollfot@gmail.com',
      url='',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Zope3',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
      )
