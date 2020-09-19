from setuptools import find_packages, setup
from pathlib import Path

setup(
    name="jgrestic",
    version=(Path(__file__).parent / "VERSION").open().read().strip(),
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["py.typed"]},
    entry_points={"console_scripts": ["jgrestic=jgrestic.main:main"]},
    author="Jacob Glueck",
    author_email="swimgiraffe435@gmail.com",
    description="Restic backup scripts",
)
