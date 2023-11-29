// export class Sensor {
//   device: string;
//   id: string;
//   type: string;
//   name?: string;
//   comments?: string;
//   lastRecord?: Date;
//   readingType: ReadingType;
// }

import { Reading, ReadingType } from './reading.ts';

enum DeviceCategory {
  Zigbee = 'Zigbee',
  Ptqs1005 = 'PTQS1005',
}

export type Sensor = {
  name: DeviceCategory;
  reading_type: ReadingType;
};

const ptqs1005: Sensor = {
  name: DeviceCategory.Ptqs1005,
  reading_type: ReadingType.Ptqs,
};
const zigbeeTemp: Sensor = {
  name: DeviceCategory.Zigbee,
  reading_type: ReadingType.ZigbeeTemp,
};
const zigbeeOccupancy: Sensor = {
  name: DeviceCategory.Zigbee,
  reading_type: ReadingType.ZigbeeOccupancy,
};
const zigbeeContact: Sensor = {
  name: DeviceCategory.Zigbee,
  reading_type: ReadingType.ZigbeeContract,
};

export type Metric = {
  display: string;
  metric: string;
  unit?: string;
  sensors: Sensor[];
};
export const metrics: Metric[] = [
  {
    display: 'Temperature',
    metric: 'temperature',
    unit: '°',
    sensors: [ptqs1005, zigbeeTemp],
  },
  {
    display: 'PM2.5',
    metric: 'pm25',
    unit: 'µg/m3',
    sensors: [ptqs1005],
  },
  {
    display: 'CO2',
    metric: 'co2',
    unit: 'ppm',
    sensors: [ptqs1005],
  },
  {
    display: 'TVOC',
    metric: 'tvoc',
    unit: 'ppm',
    sensors: [ptqs1005],
  },
  {
    display: 'HCHO',
    metric: 'ch2o',
    unit: 'mg/m3',
    sensors: [ptqs1005],
  },
  {
    display: 'Occupancy',
    metric: 'occupancy',
    unit: undefined,
    sensors: [zigbeeOccupancy],
  },
  {
    display: 'Contact',
    metric: 'contact',
    unit: undefined,
    sensors: [zigbeeContact],
  },
];

export class Device {
  id: string;
  latitude: number;
  longitude: number;
  name: string;
  lastReading?: Pick<Reading, 'time' | 'temperature'>;

  constructor(
    id: string,
    latitude: number,
    longitude: number,
    name: string,
    lastReading: {
      time: string;
      temperature: number;
    }
  ) {
    this.id = id;
    this.latitude = latitude;
    this.longitude = longitude;
    this.name = name;
    this.lastReading = lastReading;
  }
}
