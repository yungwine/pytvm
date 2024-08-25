import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
class bdist_wheel(_bdist_wheel):
    plat_name = 'manylinux2014_x86_64'

    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False


class BinaryDistribution(setuptools.dist.Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True


setuptools.setup(
    name="pytvm",
    version="0.0.14",
    author="Maksim Kurbatov",
    author_email="cyrbatoff@gmail.com",
    description="Python TVM emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages('.', exclude=['.idea', 'tests', 'examples']),
    package_data={'pytvm': ['engine/**/*']},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
    ],
    url="https://github.com/yungwine/pytvm",
    python_requires='>=3.9',
    py_modules=["pytvm"],
    # cmdclass={'bdist_wheel': bdist_wheel},
    install_requires=[
        "pytoniq-core>=0.1.31",
    ],
    distclass=BinaryDistribution
)
