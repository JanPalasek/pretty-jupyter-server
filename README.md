# Pretty Jupyter Server

It is a web server for an online demo app for [Pretty Jupyter](https://github.com/JanPalasek/pretty-jupyter) package.

The whole demo app consists of two parts:

- Frontend: http://janpalasek.com/pretty-jupyter.html
- Backend: https://pretty-jupyter.herokuapp.com/ (only REST API endpoint, no frontend)

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

The app is a very simple FastAPI web application. It exposes only one endpoint:

- `nbconvert`: POST only. As a parameter it expects an ipynb file.