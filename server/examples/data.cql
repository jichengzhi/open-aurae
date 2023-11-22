INSERT INTO aurae.device (id, building, last_record, latitude, longitude, name)
VALUES ('dev-wsd',
        {building_id: d557a89b-f493-423d-993b-c4ffec2e9d79, floor:1, room:'05', map_x: -37.90942914507165, map_y:145.13550910254588 },
        '2023-11-19 18:44:19.000',
        -37.90942914507165,
        145.13550910254588,
        'device in the woodside building');

INSERT INTO aurae.device (id, building, last_record, latitude, longitude, name)
VALUES ('dev-ltb',
        {building_id: d557a89b-f493-423d-993b-c4ffec2e9d79, floor: 1, room: '05', map_x: -37.91364766959355, map_y: 145.13258672583743 },
        '2023-11-19 18:44:19.000',
        -37.91364766959355,
        145.13258672583743,
        'device in the learning and teaching building');

INSERT INTO aurae.sensor (id, comments, device, last_record, name, type)
VALUES ('wsd-tmp',
        'temperature sensor on the woodside device',
        'dev-wsd',
        '2023-10-19 19:06:17.000',
        'wsd temperature sensor',
        'temperature');

INSERT INTO aurae.sensor (id, comments, device, last_record, name, type)
VALUES ('wsd-vibration',
        'vibration sensor on the woodside device',
        'dev-wsd',
        '2023-10-19 19:06:17.000',
        'wsd vibration sensor',
        'vibration');

INSERT INTO aurae.sensor (id, comments, device, last_record, name, type)
VALUES ('wsd-aq',
        'air quality sensor on the woodside device',
        'dev-wsd',
        '2023-10-19 19:06:17.000',
        'wsd qir quality sensor',
        'air-quality');


INSERT INTO aurae.user (id, devices, name, password, username)
VALUES ('u-foo',
        ['dev-woodside'],
        'foo',
        'pwd',
        'foo');