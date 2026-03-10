# 🛸 Quickstart

> Follow this guide to get your machine setup and configured correctly to
> contribute to this project.

## 🔍 Prerequisites

Before you get started, please be sure you've met the following:

- Install the latest LTS versions of [nodejs] and [npm].
- Install [python3.13], [pip] and [python-venv].
- Install [docker] and ensure `docker compose` is available from your terminal.
- You will need the `make` command to access this projects tooling.

> This project has been built and tested on [Linux], [macOS] and [Windows WSL].
> Unfortunately we cannot support other operating systems.

[nodejs]: https://nodejs.org
[npm]: https://www.npmjs.com/
[python3.13]: https://docs.python.org/3.13/
[pip]: https://pypi.org/project/pip/
[python-venv]: https://docs.python.org/3.13/tutorial/venv.html
[docker]: https://docker.com/
[linux]: https://www.redhat.com/en/topics/linux/what-is-linux
[macos]: https://www.apple.com/macos/
[windows wsl]: https://learn.microsoft.com/en-us/windows/wsl/about

## 🚧 Initial Setup

Before you start, it's a good idea to have a directory on your machine where
software projects can be placed. If you already have a location, please skip
this step, adjusting the each command as necessary. Otherwise, run the
following from your terminal to create a local project directory.

```bash
mkdir ~/Projects
```

Next, clone this software project onto your machine and into your project
directory.

```bash
git clone git@github.com:spendkey/spendkey-backend-assessment.git \
    ~/Projects/spendkey-backend-assessment
```

Finally, change into the projects directory.

```bash
cd ~/Projects/spendkey-backend-assessment
```

## ⛽️ Prepare the Project

Run the following command to prepare the project for local development.

```bash
make init && source venv/bin/activate
```

> See `make help` for a list of additional tools.

## 🚀 Running Locally

Before running this project, you'll need to have a database running. For
convenience we've included a `docker-compose.yaml` to make this easy. Simply
run the following command from the project root to get [Postgres] up and
running.

[postgres]: https://www.postgresql.org/

```bash
make database
```

> This will run Postgres in the background to free up your terminal. If you're
> happy to use multiple terminals, use `docker compose up` and proceed in
> another terminal tab/window.

Now a database is running, you can use following command to launch this
project.

```bash
make start
```

With the project running, you can visit <http://localhost:8000> to view the
interactive [OpenAPI] specification and familiarize yourself with the available
endpoints and inputs/outputs. Once you're comfortable, please complete the
[tasks].

> For easier development, the server will restart when files are changed.

[openapi]: https://swagger.io/specification/
[tasks]: /README.md#markdown-header-tasks
