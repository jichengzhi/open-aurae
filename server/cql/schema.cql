CREATE KEYSPACE IF NOT EXISTS aurae
    WITH REPLICATION = {
        'class' : 'SimpleStrategy',
        'replication_factor' : 1
        };

CREATE TYPE IF NOT EXISTS aurae.building_location (
    building_id uuid,
    floor int,
    room text,
    map_x decimal,
    map_y decimal
    );

CREATE TABLE IF NOT EXISTS aurae.building
(
    id   uuid primary key,
    name text
);

CREATE TABLE IF NOT EXISTS aurae.correction
(
    device       text,
    reading_type text,
    metric       text,
    expression   text,
    primary key ((device, reading_type), metric)
);

CREATE TABLE IF NOT EXISTS aurae.device
(
    id          text primary key,
    building    frozen<building_location>,
    last_record timestamp,
    latitude    decimal,
    longitude   decimal,
    name        text
);

CREATE TABLE IF NOT EXISTS aurae.reading
(
    device           text,
    date             date,
    processed        boolean,
    time             timestamp,
    reading_type     text,
    action           text,
    angle            decimal,
    angle_x          decimal,
    angle_x_absolute decimal,
    angle_y          decimal,
    angle_y_absolute decimal,
    angle_z          decimal,
    battery          decimal,
    cf_pm1           decimal,
    cf_pm10          decimal,
    cf_pm25          decimal,
    ch2o             decimal,
    co2              decimal,
    consumption      decimal,
    contact          boolean,
    humidity         decimal,
    illuminance      decimal,
    ip_address       text,
    latitude         decimal,
    longitude        decimal,
    occupancy        boolean,
    pd05             decimal,
    pd10             decimal,
    pd100            decimal,
    pd100g           decimal,
    pd25             decimal,
    pd50             decimal,
    pm1              decimal,
    pm10             decimal,
    pm25             decimal,
    pmv10            decimal,
    pmv100           decimal,
    pmv25            decimal,
    pmv_total        decimal,
    pmvtotal         decimal,
    power            decimal,
    sensor_id        text,
    state            text,
    temperature      decimal,
    tvoc             decimal,
    voltage          decimal,
    primary key ((device, date, processed), time, reading_type)
)
            with clustering order by (time desc, reading_type asc);

CREATE TABLE IF NOT EXISTS aurae.sensor
(
    id          text primary key,
    comments    text,
    device      text,
    last_record timestamp,
    name        text,
    type        text
);

CREATE INDEX IF NOT EXISTS sensor_device_idx
    on aurae.sensor (device);

CREATE TABLE IF NOT EXISTS aurae.user
(
    id       text primary key,
    devices  list<text>,
    name     text,
    password text,
    username text
);

CREATE INDEX IF NOT EXISTS user_devices_index
    on aurae.user (devices);

