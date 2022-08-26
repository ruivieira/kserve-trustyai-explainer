from setuptools import setup, find_packages

tests_require = [
    'pytest',
    'pytest-tornasync',
    'mypy'
]
setup(
    name='trustyaiserver',
    version='0.8.0',
    author_email='rui@redhat.com',
    license='https://github.com/ruivieira/kserve-trustyai-explainer/LICENSE',
    url='https://github.com/ruivieira/kserve-trustyai-explainer',
    description='KServer TrustyAI explainer',
    python_requires='>3.7',
    packages=find_packages("trustyaiserver"),
    install_requires=[
        "kserve>=0.7.0",
        "argparse >= 1.4.0",
        "numpy >= 1.8.2",
        "nest_asyncio>=1.4.0",
        "Jinja2",
        "pandas",
        "matplotlib"
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require}
)
