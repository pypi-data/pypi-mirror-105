from setuptools import setup

setup(
    name="creache",
    version="0.1",
    description="A tool that looks to convert structs to class entities in swift",
    author="Markim Shaw",
    author_email="ms79723@gmail.com",
    license="MIT",
    packages=["creache"],
    zip_safe=False,
    scripts=["bin/creache"],
    install_requires=["re", "asyncio", "click"],
)
