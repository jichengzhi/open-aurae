import DeviceInfo from '@/components/DeviceInfo.tsx';
import MetricChart from '@/components/MetricChart.tsx';
import { default as ReadingTypeSelector } from '@/components/ReadingTypeSelector.tsx';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card.tsx';
import {
  deviceSelectionAtom,
  metricSelectionAtom,
  readingTypeSelectionAtom,
} from '@/types/atom.ts';
import { useAtomValue } from 'jotai';
import DevicesMap from './components/DevicesMap.tsx';

export default function Home() {
  const device = useAtomValue(deviceSelectionAtom);
  const readingType = useAtomValue(readingTypeSelectionAtom);
  const metric = useAtomValue(metricSelectionAtom);

  // console.log({ device, metric, readingType });

  return (
    <>
      <section className="bg-gray-100 min-h-screen font-sans pb-24">
        <div className="w-[90%] m-auto">
          <h1 className="text-5xl font-bold text-gray-600 py-8 px-0">
            Live Air Quality
          </h1>

          <Card className="h-[50vh] m-auto mb-10">
            <CardContent className="h-full w-full p-0">
              <DevicesMap
                mapStyle="mapbox://styles/mapbox/light-v9"
                viewPort={{
                  latitude: -37.909365,
                  longitude: 145.134424,
                  zoom: 10,
                }}
              />
            </CardContent>
          </Card>

          {device && (
            <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-4 my-10">
              <DeviceInfo device={device} />
            </div>
          )}

          {device && (
            <Card className="font-mono">
              <CardHeader>
                <CardTitle>Metrics Monitor</CardTitle>
                <CardDescription>
                  Real time data is fetched from sensors
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col md:flex-row lg:ml-[50vw] gap-5 content-center pb-5">
                  <ReadingTypeSelector />
                </div>
                {metric && readingType && (
                  <MetricChart
                    metric={metric}
                    deviceId={device.id}
                    readingType={readingType!}
                    latestReadingTime={device.lastReading!.time!}
                  />
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </section>
    </>
  );
}
