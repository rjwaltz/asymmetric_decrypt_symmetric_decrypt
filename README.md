### env requirements
 - python = 3.8.10
 - poetry = 1.8.5


### dev steps
 - `poetry install`  |  using `pyproject.toml` and `poetry.lock` to install dependencies
 - `poetry shell`  |  into poetry virtual env, you can use `which python` to check it.
 - `poetry show`  |  verify the dependencies
 - `poetry env info --path`  |  print the poetry virtual env path
 - `python crypto_rsa\main.py`  |  execute main.py
 - `exit 0;`  |  exit the poetry virtual env

### pack
`pyinstaller -c --clean --name decryptool -F crypto_rsa/main.py`