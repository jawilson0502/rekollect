from setuptools import setup

setup(
    name="web_rekollect",
    packages=["web_rekollect"],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-Migrate',
        'Flask-Script',
        'Flask-SQLAlchemy',
        'psycopg2',
        'rekall',
    ],
)
