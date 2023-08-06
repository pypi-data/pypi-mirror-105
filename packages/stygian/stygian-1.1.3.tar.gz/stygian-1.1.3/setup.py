import setuptools


def no_local_develop_scheme(version):
    if version.branch == "develop" and not version.dirty:
        return ""
    else:
        from setuptools_scm.version import get_local_node_and_date
        return get_local_node_and_date(version)


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="stygian",
    use_scm_version={'write_to': 'stygian/version.py',
                     'local_scheme': no_local_develop_scheme},
    setup_requires=['setuptools_scm'],
    author="Suprock Technologies, LLC",
    author_email="inquiries@suprocktech.com",
    description="Headless recording program for Asphodel devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/suprocktech/stygian",
    packages=setuptools.find_packages(),
    keywords="asphodel suprock apd",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
        "Topic :: System :: Hardware",
    ],
    python_requires=">=3.6",
    install_requires=[
        "asphodel",
        "boto3",
        "hyperborea",
        "numpy",
        "psutil",
        "PySide2",
        "requests",
        "setproctitle",
    ],
    entry_points={
        'console_scripts': [
            'stygian = stygian.__main__:main',
        ],
    },
    zip_safe=False,
)
