import { deviceSelectionAtom } from '@/types/atom.ts';
import { Device } from '@/types/device.ts';
import { useQuery } from '@apollo/client';
import { plainToInstance } from 'class-transformer';
import { useSetAtom } from 'jotai';
import mapboxgl, { Popup } from 'mapbox-gl';
import React from 'react';
import Map, { Marker, ViewState } from 'react-map-gl';
import { GET_DEVICES } from '../query.ts';
import Loading from './Loading.tsx';

function buildPopup({ name, latitude, longitude, lastReading }: Device): Popup {
  const latest = lastReading || { time: 'N/A', temperature: NaN };

  const html = `
        <p>
          <b>${name}</b>
        </p>
        <p>${latest.time}</p>
        <p>Temperature: ${latest.temperature}</p>`;

  return new mapboxgl.Popup()
    .setLngLat({ lon: longitude, lat: latitude })
    .setHTML(html);
}

function Anchor(): React.JSX.Element {
  return (
    <div
      aria-description="a blue dot marking a device on the map"
      className="bg-[#516b91] rounded-full w-4 h-4"
    ></div>
  );
}

interface DevicesMapProps {
  mapStyle: string;
  viewPort: {
    longitude: number;
    latitude: number;
    zoom: number;
  };
}

export default function DevicesMap({ viewPort, mapStyle }: DevicesMapProps) {
  const [viewState, setViewState] =
    React.useState<Pick<ViewState, 'longitude' | 'latitude' | 'zoom'>>(
      viewPort
    );

  const setDevice = useSetAtom(deviceSelectionAtom);

  const { loading, data, error } = useQuery(GET_DEVICES, {
    pollInterval: 10_000,
  });

  if (error) {
    throw new Error(`Failed to get devices for map! ${error.message}`);
  } else if (loading) {
    return <Loading />;
  }

  const devices: Device[] = (data?.devices || [])
    .map((device: object) => plainToInstance(Device, device))
    .filter((device: Device) => device.lastReading);

  if (!devices) return <Loading />;

  return (
    <Map
      {...viewState}
      mapboxAccessToken="pk.eyJ1IjoibW9uYXNoYXVyYWUiLCJhIjoiY2pyMGJqbzV2MDk3dTQ0bndqaHA4d3hzeSJ9.TDvqYvsmY1DHhE8N8_UbFg"
      style={{ width: '100%', height: '100.5%' }}
      mapStyle={mapStyle}
      onMove={(evt) => setViewState(evt.viewState)}
      onZoom={(evt) => setViewState(evt.viewState)}
    >
      {devices.map((device) => (
        <Marker
          key={device.id}
          longitude={device.longitude}
          latitude={device.latitude}
          color="red"
          popup={buildPopup(device)}
          onClick={() => setDevice(device)}
        >
          <Anchor />
        </Marker>
      ))}
    </Map>
  );
}
