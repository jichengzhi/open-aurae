# Open Aurae

## Run services separately

```shell
# create docker network
docker network create aurae

# setup cassandra
docker run -d --name aurae-cassandra -p 9042:9042 -v /data/aurae-data:/var/lib/cassandra --network="aurae" cassandra:5

# setup MQTT broker
docker run -d --name aurae-mq -p 1883:1883 -p 9001:9001 --network="aurae" eclipse-mosquitto:2 mosquitto -c /mosquitto-no-auth.conf

# build backend image
docker build -t aurae-server server/

# setup backend server
docker run -d --name aurae-server -p 8000:8000 --env-file server.local.env --network="aurae" aurae-server
```

An example of contents in `.env` file is below:

```text
; address of MQTT broker
MQTT_BROKER=localhost

; address of cassandra host
CASSANDRA_SEED=127.0.0.1

; tell cassandra driver not to complain if we use sync_table()
CQLENG_ALLOW_SCHEMA_MANAGEMENT=1

; secret key used to parse jwt token
SECRET_KEY=secret
```

## Auth0

[JSON Web Token Claims](https://www.iana.org/assignments/jwt/jwt.xhtml)