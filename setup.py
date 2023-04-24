import setuptools

setuptools.setup(
    name="client_GPT",
    version="0.1",
    author="littleknitsstory",
    url="https://github.com/littleknitsstory/client-gpt",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
