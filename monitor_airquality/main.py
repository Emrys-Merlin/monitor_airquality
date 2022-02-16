import logging
from time import sleep
from typing import Dict

import click
import mh_z19
from Adafruit_BMP.BMP085 import BMP085
from prometheus_client import Gauge, start_http_server

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)


class Sensor:
    """Encapsulate MH-Z19 and SMB180 sensor
    """
    def __init__(self, room: str):
        """Initialize sensor object

        Parameters
        ----------
        room : str
            Location of the sensor
        """
        self.room = room
        self.co2_device = 'MH-Z19'
        self.temp_device = 'SMB180'

        self.bmp = BMP085()

        self.co2_gauge = Gauge(
            'co2_gauge_ppm',
            'MH-Z19 CO2 sensor',
            ['room', 'device_name', 'device_type']
            )
        self.temp_gauge = Gauge(
            'temperature_gauge_c', 
            'MH-Z19 CO2 sensor',
            ['room', 'device_name', 'device_type']
        )
        self.press_gauge = Gauge(
            'pressure_gauge_kpa',
            'SMB180 air pressure sensor', 
            ['room', 'device_name', 'device_type']
            )

        mh_z19.abc_off()

    def read(self) -> Dict[str, float]:
        """Read sensor values

        Returns
        -------
        Dict[str, float]
            Dict containing CO2 concentration, airpressure, and temperature
        """

        res = {}

        co2 = mh_z19.read_co2valueonly()
        self.co2_gauge.labels(
            room=self.room,
            device_name=self.co2_device,
            device_type=self.co2_device,
        ).set(co2)
        res['co2'] = co2

        temp = self.bmp.read_temperature()
        self.temp_gauge.labels(
            room=self.room,
            device_name=self.temp_device,
            device_type=self.temp_device,
        ).set(temp)
        res['temperature'] = temp

        press = self.bmp.read_pressure() / 1000
        self.press_gauge.labels(
            room=self.room,
            device_name=self.temp_device,
            device_type=self.temp_device,
        ).set(press)
        res['pressure'] = press

        return res


@click.command()
@click.argument('room', type=click.STRING)
@click.argument('port', type=click.INT)
@click.option('--wait', '-w', type=click.INT, default=10,
              help='Waiting time between sensor reads')
def main(room: str, port: int, wait: int):
    """Monitor airquality

    Script to read CO2 concentration, temperature, and airpressure
    from ROOM. Metrics will be exposed in prometheus format on PORT.
    \f

    Parameters
    ----------
    room : str
        Location of the sensor
    port : int
        Port where measurements are exposed
    wait : int
        Waiting time between sensor readouts
    """
    start_http_server(port)

    sensor = Sensor(room)

    while True:
        res = sensor.read()
        logger.info(res)

        sleep(wait)


if __name__ == "__main__":
    main()
