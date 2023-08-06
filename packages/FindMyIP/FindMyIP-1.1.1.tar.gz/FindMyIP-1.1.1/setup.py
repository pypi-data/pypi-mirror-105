from pathlib import Path
from setuptools import setup

# The directory containing this file
HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="FindMyIP",
    packages=["."],
    version="1.1.1",
    description="Find your IP address (both internal(local) and external) or check your connection status.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Mehran-Seifalinia/Find-Your-IP",
    author="Mehran Seifalinia",
    author_email="mehran.seifalinia@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)