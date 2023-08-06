del /s dist
python setup.py bdist_wheel sdist
twine upload dist/*