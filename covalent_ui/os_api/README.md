# OS WebAPI - V1
## _Built on FastAPI_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Installation

Requires [python](https://www.python.org/) Python 3.8.10 to run.

Install the dependencies.

```sh
git clone https://github.com/AgnostiqHQ/covalent.git
cd Covalent
```
> **_NOTE:_**  Please make sure all the dependencies are installed as per the guide from [CONTRIBUTING.md](https://github.com/Aravind-psiog/os_webapp/blob/main/CONTRIBUTING.md)

## Running the server
```sh
cd covalent_ui/os_api
python3 oswebapi.py start >> this command starts both main.py and app.py
python3 oswebapi.py stop >> this command stops both main.py and app.py
python3 oswebapi.py restart >> this command restarts both main.py and app.py
```
logs can be found at /covalent_ui/os_api/logs folder

#### Testing the app (Swagger)
FastAPI can be fully tested in [localhost](http://127.0.0.1:8000/docs)