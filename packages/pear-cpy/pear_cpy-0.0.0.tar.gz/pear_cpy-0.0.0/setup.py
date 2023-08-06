from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "pear_cpy",
    version = "0.0.0",
    url = "https://github.com/g3rrit/pear_cpy",
    author = "Gerrit Proessl",
    author_email="grproessl@web.de",
    license = "MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Build instructions
    ext_modules = [Extension("pear_cpy",
                             ["pear_cpy.bycython.c", "pear_cpy.c"],
                             include_dirs=[],
                             language="c")]
)
