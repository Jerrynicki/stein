# Stein
![funny stone picture](./root/frontend/stein_app/src/assets/funny_stone.jpg)

## Setup (Linux)

### Prerequisites

- Node >= v16

- NPM

- Python3

- Python3-venv

- a nice stone nearby 🪨

### Using the install script
- Use the provided `root/setup.sh` script.

Try these steps if it doesn't work:

### Frontend

- `npm install -g @angular/cli`

- In root/frontend/stein_app:

    - `npm install`

    - `ng build`

### Backend

- `python3 -m venv .`

- `source bin/activate`

- `pip3 install -r requirements.txt`

Either run the module `app:create_app()` using a WSGI server, or use the `run_debug.sh` script in src/flask_app to use the flask debug server

If the frontend was built succcessfully, it should work automatically