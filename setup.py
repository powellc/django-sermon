from setuptools import setup, find_packages

setup(
    name='django-sermon',
    version=__import__('sermon').__version__,
    license="BSD",

    install_requires = ['django-markup-mixin','django-extensions',],

    description='A simple reusable application for managing sermons in a Django application.',
    long_description=open('README.rst').read(),

    author='Colin Powell',
    author_email='colin@onecardinal.com',

    url='http://github.com/powellc/django-sermon',
    download_url='http://github.com/powellc/django-sermon/downloads',

    include_package_data=True,

    packages=['sermon'],

    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
