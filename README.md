# Styn

Styn is a small student project. From 4 computer science students in Germany.

People can upload Stones to an Instagram-like feed. Where they can comment and rate others Stones.

## Installation

To run Styn locally on your machine Docker needs to be installed and running.

Build the Docker-Image:

```bash
docker build -t styn:latest .
```

Run the Docker-Container with Port-Mapping:

```bash
docker run --name styn -p 8000:8000 styn:latest
```

Styn is now accessible under `localhost:8000`

To keep the Database persistent mount a volume for `/app/instance` e.g.:

```bash
docker run --name styn -v styn-db:/app/instance -p 8000:8000 styn:latest
```

By default, the Container will log to your terminal

To run the Container in the background detach the container:

```bash
docker run -d --name styn -v styn-db:/app/instance -p 8000:8000 styn:latest
```

Styn will now run in the background

To stop and delete the Container:

```bash
docker stop styn
docker rm styn
```

## Usage

To use the API send requests to `/api/`.

For available endpoints check our [OpenAPI](/doc/openapi.yaml) file.

## Public Instance

A public instance can be found on [stein.bellgardt.dev](https://stein.bellgardt.dev).

## Contribution

As this is a study project which will be assessed later, no contributions are currently accepted.

## License

No license chosen yet.

Please do not distribute or modify the Code without our permission.
