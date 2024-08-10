import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='agenda_template',
    version='1.0',
    packages=setuptools.find_packages(),
    scripts=[
        'scripts/make_agenda.py',
    ],
    author='Louise Scherrer, Martin Jacquet',
    author_email='martin.jacquet@posteo.net',
    description='Python scripts for automated generation of an agenda based on an html/css template.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/louise-scherrer/agenda-template/tree/main/template',
    license='None',
)
