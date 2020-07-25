from setuptools import find_packages, setup

setup(
    name="jgrestic",
    version="1.0.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["py.typed"]},
    entry_points={"console_scripts": ["jgrestic=jgrestic.main:wrapper"]},
    author="Jacob Glueck",
    author_email="swimgiraffe435@gmail.com",
    description="Restic backup scripts",
)
