import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sdi_utils",

    version="0.0.1",

    author="Thorsten Hapke",
    author_email="thorsten.hapke@sap.com",
    description="Mocking SAP Data Intelligence api for local testing",
    long_description= long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/thhapke/gensolution",
    keywords = ['SAP Data Intelligence','local development', 'mocking api'],
    packages=setuptools.find_packages(),
    install_requires=[],
    include_package_data=True,
    classifiers=[
    	'Programming Language :: Python :: 3.5',
    	'Programming Language :: Python :: 3.6',
    	'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)