import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '@/components/ui/hover-card';
import { useToast } from '@/components/ui/use-toast';
import { Device } from '@/types/device.ts';
import React from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { LuCopy } from 'react-icons/lu';

function DeviceField({
  name,
  value,
  desc,
}: {
  name: string;
  value: string;
  desc: string;
}) {
  const { toast } = useToast();
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{name}</CardTitle>
        <HoverCard>
          <HoverCardTrigger className="cursor-pointer">
            <CopyToClipboard
              text={value}
              onCopy={() =>
                toast({
                  title: 'Copied!',
                  className:
                    'fixed top-0 z-[100] flex max-h-screen w-full flex-col-reverse p-4  sm:right-0  sm:flex-col md:max-w-[420px]',
                  duration: 2000,
                })
              }
            >
              <LuCopy />
            </CopyToClipboard>
          </HoverCardTrigger>
          <HoverCardContent
            align={'center'}
            className="flex items-center justify-center text-sm w-14 p-2"
          >
            <span>Copy</span>
          </HoverCardContent>
        </HoverCard>
      </CardHeader>
      <CardContent className="break-words">
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground">{desc}</p>
      </CardContent>
    </Card>
  );
}

export default function DeviceInfo({
  device,
}: React.ComponentProps<typeof Card> & { device: Device }): React.JSX.Element {
  return (
    <>
      <DeviceField
        name="Device Id"
        value={device.id}
        desc="unique identifier of the device"
      />

      <DeviceField
        name="Device Name"
        value={device.name}
        desc="name of the device"
      />

      <DeviceField
        name="Device Latitude"
        value={device.latitude.toString()}
        desc="Location of the device"
      />

      <DeviceField
        name="Device Longtitude"
        value={device.longitude.toString()}
        desc="Location of the device"
      />
    </>
  );
}
