from setuptools import setup

VERSION = '2.0.0'
DESCRIPTION = 'Official CocoyoyoLibrairie API packages'
f = open('README.md')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name="cocoyoyo_librairie_api",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="CAMARM-DEV",
    author_email="armand@camponovo.xyz",
    license='MIT',
    packages=['cocoyoyo_librairie_api'],
    install_requires=['requests~=2.25.1',
                      'colorama~=0.4.4',
                      ],
    keywords='conversion',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ],
    long_description_content_type='text/markdown'
)
