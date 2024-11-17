# Service Design and Engineering

## Python dependencies installation

This will create a virtual environment called `.venv`:

- install uv: [Installation](https://docs.astral.sh/uv/getting-started/installation/)
- `uv sync`
- `source .venv/bin/activate`

## Kafka setup

You can start Kafka with the docker compose file defined in this repo, just run:

```bash
sudo docker compose up
```

Kafka will be available on port 9094. To create topics enter the container with:

```bash
sudo docker exec -it unitn-sde-kafka-1 /bin/bash
```

Afterwards you can create a new topic with this command:

```bash
kafka-topics.sh --bootstrap-server localhost:9094 --create --topic <topic_name> --partitions <number_of_partitions>
```

## Run producer and consumer

To start the producer you can do `./main.py producer` and for the consumer `./main.py consumer`. With uv instead of `./main.py` you could use `uv run main.py` without the need to source the virtual environment.

## Run examples and exercises

- `python3 -m lab4.test`: test your configuration and connection with the Broker.
- `python3 -m lab4.examples.example1`: run example 1
- `python3 -m lab4.exercises.exercise1`: run exercise 1
- `python3 -m lab4.assignment.assignment`: run assignment
