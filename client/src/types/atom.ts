import { Device } from '@/types/device.ts';
import { ReadingType } from '@/types/reading.ts';
import { atom } from 'jotai';

const deviceAtom = atom<Device | null>(null);
const metricAtom = atom<string | null>(null);

export const readingTypeSelectionAtom = atom<ReadingType | null>(null);

export const metricSelectionAtom = atom(
  (get) => get(metricAtom),
  (_, set, newMetric: string | null) => {
    set(metricAtom, newMetric);
    set(readingTypeSelectionAtom, null);
  }
);

export const deviceSelectionAtom = atom(
  (get) => get(deviceAtom),
  (_, set, newDevice: Device) => {
    set(deviceAtom, newDevice);
    set(metricSelectionAtom, null);
  }
);
