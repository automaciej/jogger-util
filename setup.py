# coding: utf-8

from distutils.core import setup

setup(name='jogger-util',
      version='0.1.1',
      description='Experimental utility to mass edit your jogger.pl blog entries',
      author='Maciej Bliziński',
      author_email='maciej.blizinski@gmail.com',
      url='https://github.com/automatthias/jogger-util',
      packages=['jogger'],
      package_dir={'jogger': 'jogger'},
      package_data={'jogger': ['testdata/*.html']},
      entry_points={
        'console_scripts': [
          'jogger-set-all-entries = jogger.comments_on_all_entries:main'
        ],
      },
      install_requires=[
        'beautifulsoup4>=4.0.0',
        'requests>=2.0.0',
      ],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
      ],
)
