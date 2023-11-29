import Loading from '@/components/Loading.tsx';
import { GET_SENSOR_METRICS } from '@/query.ts';
import { Reading, ReadingType } from '@/types/reading.ts';
import { useQuery } from '@apollo/client';
import { plainToInstance } from 'class-transformer';
import moment from 'moment/moment';
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

function formatXTick(time: string): string {
  return moment(time).format('HH:mm');
}

export default function MetricChart({
  metric,
  deviceId,
  readingType,
  latestReadingTime,
}: {
  metric: string;
  deviceId: string;
  readingType: ReadingType;
  latestReadingTime: string | Date;
}) {
  const { loading, data } = useQuery(GET_SENSOR_METRICS(metric), {
    variables: {
      start: moment
        .utc(latestReadingTime)
        .subtract(7, 'days')
        .format('YYYY-MM-DD'),
      end: moment.utc(latestReadingTime).format('YYYY-MM-DD'),
      device: deviceId,
      metric: metric,
      readingType: readingType,
    },
    pollInterval: 10_000,
  });

  if (loading) {
    return <Loading />;
  }

  const readings: Reading[] = (data.readings || []).map((obj: object) =>
    plainToInstance(Reading, obj)
  );

  console.log(readings);

  return (
    <ResponsiveContainer height={300}>
      <LineChart
        data={readings}
        margin={{ top: 5, right: 20, bottom: 5, left: 0 }}
      >
        <Line type="monotone" dataKey={metric} stroke="#8884d8" />
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis
          dataKey="time"
          tickFormatter={formatXTick}
          padding={{ left: 20, right: 20 }}
        />
        <YAxis />
        <Tooltip />
      </LineChart>
    </ResponsiveContainer>
  );
}
