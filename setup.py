from setuptools import setup

setup(
    name='slimelearnpy',
    version='0.8.4',    
    description='A very easy to use API wrapper for SlimeLearn written in Python.',
    url='https://github.com/javierburgosv/slimelearn.py',
    author='Javier Burgos',
    author_email='j.b.valdes@hotmail.com',
    license='MIT',
    packages=['slimelearn'],
    install_requires=['websockets>=8.1',
                      'nest-asyncio',                     
                      ],
)