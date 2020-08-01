import setuptools

with open("readme.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sql_quiz",
    version="0.0.1",
    author="Joel Burton",
    author_email="joel@joelburton.com",
    description="A CLI/quiz system for PostgreSQL.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/joelburton/sql_quiz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Education :: Testing",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'sql_quiz=sql_quiz.main:main',
        ],
    },
    package_data={
        'sql_quiz': ['pgclirc']
    },
    install_requires=[
        'pgcli',
        'pyyaml',
    ]
)
