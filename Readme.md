# Monitor Airquality

I use this script to read CO2 concentration from a MH-Z19 and air temperature and pressure from an SMB180 sensor connected to a raspberry pi (1. generation B+, I found it lying around...)

## Installation

I would recommend that you create a virtual environment for this project before proceeding with the installation.

```
git clone --recurse-submodules https://github.com/Emrys-Merlin/monitor_airquality.git 
cd monitor_airquality
pip install -r requirements.txt
pip install -e .
```

## Usage

The package installs a commandline tool called `monitor_airquality` which takes as a first positonal argument the location of the sensor and as a second the port at which the measurements are exposed for scraping by prometheus. The `--wait` option specifies the waiting time between sensor readouts in seconds. The default is 10 seconds.

```
monitor_airqality ROOM PORT --wait WAIT
```

The script needs root privileges to access the devices. This might lead to trouble because the virutal environment might not be in the path. Either activate it as root or use the absolute path to the installed cli.