import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acme-rofl",
    version="0.0.3",
    author="James Vasile",
    author_email="james@opentechstrategies.com",
    description="Respond to ACME challenges, forward all other requests to port 443",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jvasile/acme-rofl",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Development Status :: 4 - Beta",
        "Framework :: Twisted",
        "Operating System :: POSIX",
    ],
    package_dir={"": "src"},
    data_files=[
        ('share/acme-rofl', ['acme-rofl.service', 'README.md'])
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.4",
    entry_points={
        'console_scripts': [
            'acme-rofl=acme_rofl:run',
        ],
    },
)
