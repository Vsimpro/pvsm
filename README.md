# Tech Demo: Programmatic Vulnerability Scanning & Management
Showcasing a system to automate the running of vulnerability & testing tools, and storing their results into a database for easier access, analysis & integration.


## Overview
This is a demo showcasing an automated approach to programmatic running & storing of vulnerability scanner results. Results are stored into a database for easier access, future data-analysis, and to allow chaining of tools. The aim of this solution is to facilitate efficient scanning, tracking, and management of vulnerabilities across multiple tools & methdos.

> ⚠️ Remember that the tools are being run on your server! You, and you only are responsible for any misuse of this software.

# Usage

This software isn't really meant to be run as a complete solution as is, but rather show a way of building a Python wrapper of sorts to tooling. To run & tinker with the demo, install the following and run + tinker with `main.py`

You need the following software:
```
git
docker
python3
```

Git clone this repository:
```bash
git clone https://github.com/Vsimpro/pvsm
```

You need to install the following dependencies to run the code: 
```bash
cd pvsm
pip install -r requirements.txt
```

Run using:
```
python3 main.py -t <TARGET_IP>
```

## Further explanation & thoughts.

