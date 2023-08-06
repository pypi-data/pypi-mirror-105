from setuptools import setup


def read_files(files):
    data = []
    for file in files:
        with open(file, encoding='utf-8') as f:
            data.append(f.read())
    return "\n".join(data)


meta = {}
with open('praetorian_fabric/version.py') as f:
    exec(f.read(), meta)

setup(
    name='praetorian-fabric',
    version=meta['__version__'],
    packages=[
        'praetorian_fabric',
    ],
    install_requires=[
        'python-dotenv==0.15.*',
        'fabric>=2.5.0',
        'praetorian-api-client>=0.4.2'
    ],
    url='https://github.com/Praetorian-Defence/praetorian-fabric',
    license='MIT',
    author='Adam Žúrek',
    author_email='adamzurek14@gmail.com',
    description='Praetorian Fabric library extends standard `fabric` library, to maintain communication with '
                'praetorian services. Main purpose is to make necessary connections and provide suitable data.',
    long_description=read_files(['README.md', 'CHANGELOG.md']),
    long_description_content_type='text/markdown',
    classifiers=[
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
        'Topic :: Security'
    ]
)
