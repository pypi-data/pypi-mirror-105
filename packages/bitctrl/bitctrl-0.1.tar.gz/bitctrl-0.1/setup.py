from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name="bitctrl",
    version="0.1",
    description='Turn your microbit into a controller',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='momea007',
    author_email='momea007@hotmail.com',
    keywords='microbit',
    license='MIT',
    packages=['bitctrl'],
    install_requires=['pyserial','keyboard'],
    include_package_data=True,
    zip_safe=False
    )