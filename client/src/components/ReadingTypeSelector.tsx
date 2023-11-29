import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { metricSelectionAtom, readingTypeSelectionAtom } from '@/types/atom.ts';
import { Metric, Sensor, metrics } from '@/types/device.ts';
import { ReadingType } from '@/types/reading.ts';
import { useAtom } from 'jotai';
import * as R from 'ramda';
import React from 'react';

function metricDisplayText(metric: Metric): string {
  const unit = metric.unit ? `(${metric.unit})` : '';
  return `${metric.display} ${unit}`;
}

function MetricOption(metric: Metric): React.JSX.Element {
  return (
    <SelectItem key={metric.metric} value={metric.metric}>
      {metricDisplayText(metric)}
    </SelectItem>
  );
}

function SensorOption(sensor: Sensor): React.JSX.Element {
  return (
    <SelectItem key={sensor.reading_type} value={sensor.reading_type}>
      {sensor.name}
    </SelectItem>
  );
}

function sensorsOfMetric(metric: string | null): Sensor[] {
  if (!metric) {
    return [];
  }
  return R.find(R.propEq(metric, 'metric'), metrics)!.sensors;
}

interface SelectorProps extends React.ComponentPropsWithoutRef<typeof Select> {}

export default function ReadingTypeSelector(
  props: SelectorProps
): React.JSX.Element {
  const [metric, setMetric] = useAtom(metricSelectionAtom);
  const [readingType, setReadingType] = useAtom(readingTypeSelectionAtom);

  const sensors = sensorsOfMetric(metric);

  return (
    <>
      <Select value={metric || ''} onValueChange={setMetric} {...props}>
        <SelectTrigger className="focus-visible:ring-transparent">
          <SelectValue placeholder="Choose metric" />
        </SelectTrigger>
        <SelectContent>{R.map(MetricOption, metrics)}</SelectContent>
      </Select>

      <Select
        value={readingType || ''}
        onValueChange={(val) => setReadingType(val as ReadingType)}
        {...props}
      >
        <SelectTrigger className="focus-visible:ring-transparent">
          <SelectValue placeholder="Choose sensor" />
        </SelectTrigger>
        <SelectContent>{R.map(SensorOption, sensors)}</SelectContent>
      </Select>
    </>
  );
}
