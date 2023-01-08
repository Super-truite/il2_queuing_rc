import setuptools

with open("il2_queuing_rc/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="il2_queuing_rc", # Replace with your own username
    version="0.1",
    author="super-truite",
    author_email="author@example.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Super-truite/il2_queuing_rc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
