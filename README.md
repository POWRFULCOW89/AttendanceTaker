# AttendanceTaker

A selenium-based automation tool to help take attendance in [Moodle](https://moodle.org)-based platforms. 

## Installation

1. Download the ZIP or clone the repo
```sh
git clone https://github.com/POWRFULCOW89/AttendanceTaker/
```

2. Setup a virtual environment:
```sh
python3 -m venv /path/to/new/virtual/environment
```
3. Activate the virtual environment:
```sh
.\env\Scripts\activate
```

4. Install the dependencies
```sh
pip install -r requirements.txt
```

5. Install the PhantomJS driver from [here](https://phantomjs.org/download.html) and place on the directory.

## Usage

An example is provided at ```example.py```. We first need the base URL of the platform, such as "https://avalid.moodleplatform.com.uk".
We then instantiate the AttendanceTaker by doing:

```py
AT = AttendanceTaker(base_url_here)
```

We then load up our credentials from ```credentials.json``` and login:

```py
AT.load_credentials(json_file)
AT.login()
```

To take attendance, we go to the course and search the attendance links:

```py
AT.navigateToCourseById(1111)
AT.takeAttendance()
```

And we're done! It is recommended to clean up afterwards:

```py
AT.logout()
AT.exit()
```

You can debug the driver's current page with

```py
AT.currentPage()
```
## TODO:

- [ ] Tests
- [ ] Setup CRON jobs
- [ ] GUI for non technical users
 
