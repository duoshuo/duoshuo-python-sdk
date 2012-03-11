from setuptools import setup, find_packages


setup(
    name="duoshuo-python-sdk",
    version="0.1",
    description="A Python library for using the box API",
    author="Perchouli",
    author_email="jp.chenyang@gmail.com",
    url="https://github.com/duoshuo/duoshuo-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    include_package_data=True,
    zip_safe=False,
)