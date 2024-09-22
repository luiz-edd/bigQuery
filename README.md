# Project Setup

This guide provides instructions for setting up and running the project, which includes Metabase with ClickHouse integration, Airbyte, and other related services.

## 1. Build Docker Image for Metabase with ClickHouse

Navigate to the `repos/metabase-clickhouse-driver` directory and build the Docker image with the ClickHouse plugin:

```bash
./build_docker_image.sh v0.50.26 1.50.2 my-metabase-with-clickhouse:v0.0.1
```

This command integrates the ClickHouse plugin into Metabase, enabling visualization support.

## 2. Create and Run Airbyte Container

Navigate to the `repos/airbyte-0.52.0` directory and start the Airbyte container:

```bash
./run-ab-platform.sh
```

This command sets up the Airbyte container.

## 3. Configure and Start Docker Services

1. Create your own `.env` file using `.env_sample` as a template.
2. Run the following command inside the `docker/` directory to start the services:

    ```bash
    docker-compose up -d
    ```

## 4. Verify Container Status and Obtain IP Address

1. Check if all containers are running by inspecting the Docker network:

    ```bash
    docker network inspect docker_default
    ```

2. Copy the IPv4 address of the PostgreSQL container. Update the `host` variable in `scripts/populate.py` on the host machine with this address. For example:

    ```python
    host="172.18.0.3"
    ```

## 5. Run the Populate Script

Execute the Python script to populate the database:

```bash
python3 populate.py
```

## Accessing Services

You can access the following services via the specified URLs:

- **Metabase**: [http://localhost:3000](http://localhost:3000)
- **Airbyte**: [http://localhost:8000](http://localhost:8000)
- **CloudBeaver**: [http://localhost:8978](http://localhost:8978)
- **ClickHouse**: [http://localhost:8123/play](http://localhost:8123/play)

## Credentials

Usernames and passwords are available in `docs/localhost_address.txt`.
