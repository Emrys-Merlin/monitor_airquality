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
    def __init__(self, room: str, temp_offset: float = 0.):
        """Initialize sensor object

        Parameters
        ----------
        room : str
            Location of the sensor
        temp_offset : float
            Correction offset for temperature measurement
        """
        self.room = room
        self.co2_device = 'MH-Z19'
        self.temp_device = 'SMB180'
        self.temp_offset = temp_offset

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
        co2 = mh_z19.read_co2valueonly()
        temp = self.bmp.read_temperature() + self.temp_offset
        press = self.bmp.read_pressure() / 1000

        res = dict(
            co2=co2,
            temperature=temp,
            pressure=press
        )

        self.co2_gauge.labels(
            room=self.room,
            device_name=self.co2_device,
            device_type=self.co2_device,
        ).set(co2)

        self.temp_gauge.labels(
            room=self.room,
            device_name=self.temp_device,
            device_type=self.temp_device,
        ).set(temp)

        self.press_gauge.labels(
            room=self.room,
            device_name=self.temp_device,
            device_type=self.temp_device,
        ).set(press)

        return res


@click.command()
@click.argument('room', type=click.STRING)
@click.argument('port', type=click.INT)
@click.option('--wait', '-w', type=click.INT, default=10,
              help='Waiting time between sensor reads')
@click.option(
    '--temp_offset', '-t', type=float, default=0.,
    help='Set temperature offset'
)
def main(room: str, port: int, wait: int, temp_offset: float):
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
    temp_offset : float
        Offset for temperature measurements
    """
    start_http_server(port)

    sensor = Sensor(room, temp_offset=temp_offset)

    while True:
        res = sensor.read()
        logger.info(res)

        sleep(wait)


if __name__ == "__main__":
    main()
