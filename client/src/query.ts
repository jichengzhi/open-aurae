import { gql } from '@apollo/client';

export const GET_DEVICES = gql`
  query GetDevices {
    devices {
      id
      name
      latitude
      longitude
      lastReading(readingTypes: [pms5003st, ptqs1005, zigbee_temp]) {
        time
        temperature
        pm25
      }
    }
  }
`;

export const GET_SENSOR_METRICS = (metric: string) => gql`
    query GetSensorMetrics(
        $start: Date!,
        $end: Date!,
        $device: String!,
        $readingType: ReadingType!) {
        readings(
            start: $start,
            end: $end,
            device: $device,
            processed: true,
            type: $readingType) {
            time
            ${metric}
        }
    }`;
