# ainlp

nlp library which support text processing methods, text match methods, etc


## publish ainlp package method

configure `~/.pypirc` file, add the following lines:

```ini
[ainlp]
repository=https://upload.pypi.org/legacy/
username=__token__
password=pypi-AgEIcHlwaS5vcmcCJDQyNzU0YzYwLTBhNWYtNGI1Zi05OTI5LTBhMjQwMzc1YjEwYwACNnsicGVybWlzc2lvbnMiOiB7InByb2plY3RzIjogWyJhaW5scCJdfSwgInZlcnNpb24iOiAxfQAABiDDY42I73y7epx_fP7Q1MjRES8FJA3dI2b-0tF5-gO0tg
```

then modify version in `setup.py`, run the following commands to publish the new version to pypi:

```shell
python setup.py sdist bdist_wheel
twine upload dist/ainlp-<new version>*
```
