import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mmath",
    version="1.0.5",
    author="Groupe 25",
    author_email="analyse25info@gmail.com",
    description="Un simple module mathématique pour calculer le sinus d'un réel avec précision.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Atepir/analyse-groupe-25",
    project_urls={
        "Bug Tracker": "https://github.com/Atepir/analyse-groupe-25/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)