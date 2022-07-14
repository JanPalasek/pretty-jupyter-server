# Pretty Jupyter Server

It is a web server for a future online demo for [Pretty Jupyter](https://github.com/JanPalasek/pretty-jupyter).

## Installation

```sh
sh env/install.sh # or ./env/install.ps1 for windows powershell
```

## Running

```sh
# assumption: activated environment

python -m uvicorn pretty_jupyter_server:app --reload
```

## Documentation

The app is a very simple fastapi web application. It exposes only one endpoint:

- `nbconvert`: As a parameter it expects a file.