# badge

The goal of this simple script is to generate Github badge-like using Pillow.
Color used here are taken from Google material color pallet.

Finally I used python click library to create a cli.


## Getting started

First clone the repo:

`git clone https://github.com/ChristfriedBalizou/badge.git`

Install the requirements. I run the test using a Debian 10 (Buster) and a
python 3.7

`pip install -r requirements.txt`

## Usage

```
Usage: badge.py [OPTIONS]

  Command line interface to use badge

Options:
  --label TEXT          The badge label.
  --message TEXT        Message to display in the badge.
  --output TEXT         Image output path
  --status [1|2|3|4|5]  Status of badge color switch
  --help                Show this message and exit.
```

## Showcase

* Badge with a FAILURE status=1
  ```bash
  python badge.py --label build --message failed --status 1 --output failed.png
  ```
  ![Build Status](https://github.com/ChristfriedBalizou/badge/raw/master/showcase/failed.png "Build Falling")
  
* Badge with a PENDING status=2
  ```bash
  python badge.py --label build --message running --status 2 --output running.png
  ```
  ![Build Status](https://github.com/ChristfriedBalizou/badge/raw/master/showcase/running.png "Build Running")

* Badge with a INFO status=3
  ```bash
  python badge.py --label production --message v1.0 --status 3 --output production.png
  ```
  ![Running Version](https://github.com/ChristfriedBalizou/badge/raw/master/showcase/production.png "Running version")
  
* Badge with a UNKNWON status=4
  ```bash
  python badge.py --label development --message ? --status 4 --output unknown.png
  ```
  ![Running Version](https://github.com/ChristfriedBalizou/badge/raw/master/showcase/unknown.png "Unknown status")
  
* Badge with a PASSING status=5
  ```bash
  python badge.py --label build --message passing --status 5 --output passing.png
  ```
  ![Build Status](https://github.com/ChristfriedBalizou/badge/raw/master/showcase/passing.png "Build Passing")

