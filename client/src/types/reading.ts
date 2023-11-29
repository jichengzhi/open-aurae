export enum ReadingType {
  Ptqs = 'ptqs1005',
  Pms = 'pms5003st',
  ZigbeeTemp = 'zigbee_temp',
  ZigbeeOccupancy = 'zigbee_occupancy',
  ZigbeeContract = 'zigbee_contact',
  ZigbeeVibration = 'zigbee_vibration',
  ZigbeePower = 'zigbee_power',
}

export class Reading {
  time?: string;

  battery?: number;
  voltage?: number;

  temperature?: number;
  humidity?: number;
  tvoc?: number;
  co2?: number;

  pd05?: number;
  pd10?: number;
  pd25?: number;
  pd50?: number;
  pd100?: number;
  pd100g?: number;
  pm1?: number;
  pm10?: number;
  pm25?: number;
  cf_pm1?: number;
  cf_pm10?: number;
  cf_pm25?: number;
  pmv10?: number;
  pmv25?: number;
  pmv100?: number;
  pmv_total?: number;
  pmvtotal?: number;
  ch2o?: number;
  occupancy?: boolean;
  illuminance?: number;
  contact?: boolean;
  state?: string;
  power?: number;
  consumption?: number;
  angle?: number;
  angle_x?: number;
  angle_y?: number;
  angle_z?: number;
  angle_x_absolute?: number;
  angle_y_absolute?: number;
  action?: string;
}
