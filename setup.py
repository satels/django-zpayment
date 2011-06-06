#coding:utf-8
from setuptools import setup

setup(
    name='django-zpayment',
    version=__import__('zpayment').__version__,
    description='ZPayment Merchant Interface support for Django.',
    author='Ivan Petukhov',
    author_email='satels@gmail.com',
    url='http://github.com/satels/',
    packages=['zpayment'],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=['django', 'django-annoying', 'django-payment-webmoney'],
    include_package_data=True,
    zip_safe=False,
)
