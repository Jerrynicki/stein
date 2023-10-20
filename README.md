# **Frontend:**

## SteinApp

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 16.2.1.

### Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

### Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

### Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

### Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

### Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

### Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.

---

# **Backend:**

How to run:

- Install [Python](https://python.org)

- Use the [Setup script](./root/backend/setup.sh) to configure the virtual environment (Windows: copy and paste the commands while inside the root/backend folder)

- When in the virtual environment, start the flask server using the [run_debug.sh script](./root/backend/src/flask_app/run_debug.sh) to create the database

- Create at least one team, otherwise registration won't work (using e.g. [DB Browser for SQLite](https://sqlitebrowser.org/)), the database is located in the var/app-instance directory created at the root of the virtual environment

- Start the flask server using the [run_debug.sh script](./root/backend/src/flask_app/run_debug.sh)

---

# **Stein:**
![funny stone picture](./root/frontend/stein_app/src/assets/funny_stone.jpg)
