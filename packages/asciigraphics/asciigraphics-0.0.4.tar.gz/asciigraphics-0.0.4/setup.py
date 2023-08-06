from setuptools import setup
with open("README.md","r") as fh:
  long_description = fh.read()
setup(
  name = 'asciigraphics',
  version = '0.0.4',
  description = 'Do Pixel Graphics with ascii charecters',
  py_modules = ["asciianim"],
  package_dir = {'':'src'},
  classifiers = [
    "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
    "Operating System :: Microsoft :: Windows :: Windows 10 ",
    "Operating System :: POSIX :: Linux"
  ],
  long_description = long_description,
  long_description_content_type = "text/markdown",
  install_requires = [
    "cursor",
    "pyautogui",
    "numpy",
    "dataclasses"
  ],
  extras_require = {
    "dev": [
      "pytest>=3.7",
    ]
  },
  url="https://github.com/beaterblank/ascii-graphics",
  author = "G.Mohan teja",
  author_email="mohanteja.g2019@vitstudent.ac.in",
  )
