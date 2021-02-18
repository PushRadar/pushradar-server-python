from setuptools import setup

setup(
    name='pushradar',
    version='3.0.2',
    description="PushRadar's official Python server library.",
    url='https://github.com/pushradar/pushradar-server-python',
    author='PushRadar',
    author_email='contact@pushradar.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3',
    ],
    keywords='pushradar realtime websockets channels',
    packages=['pushradar'],
    install_requires=['requests>=2.3.0'],
)
