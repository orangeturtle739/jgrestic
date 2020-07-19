from setuptools import setup, find_packages

setup(
    name="jgrestic",
    version="1.0.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["jgrestic=jgrestic.main:wrapper"]},
    author="Jacob Glueck",
    author_email="swimgiraffe435@gmail.com",
    description="Restic backup scripts",
)
