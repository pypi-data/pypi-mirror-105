from setuptools import setup


setup(
    name='pycalltrace',
    version='0.2',
    url='https://github.com/kwsy/calltrace',
    license='BSD',
    author='dongsheng zhang',
    author_email='xigongda200608@163.com',
    description='record and trace the function call chain',
    py_modules= ['pycalltrace',],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
