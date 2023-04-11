# $1 Gesture Recognizer

## Authors

Katherine Chan, Thomas Ruby, Jonathan Zhang

## Prerequisities

1. Python 3.10+ and pip

2. `pip install -r requirements.txt`

## Online Recognition

`python src/1_dollar.py true`

TODO: insert image and description of process

The true parameter signals that the recognition is online or live.

## Offline / Test Recognition

`python src/1_dollar.py false [int: iterations] [int: num users] [string: dataset]`

- Defaults: 10 iterations, 1 user

The false parameter signals that the recognition is offline or not live.

TODO: insert image and description of process

## Collecting Gesture Data

`python src/gather_gestures.py ["1dollar" / "numeric"] [OPTIONAL: username] [OPTIONAL: sample # to resume at]`

Gather either the "1dollar" gesture set or the "numeric" 0-9 gesture set.

Usernames should begin with a prefix character such as 'n' for a subject drawing the numeric gesture set.

TODO: insert image and description of process

## Data Exploration

`python src/audit_gestures.py ['s' / 'n' / other prefix]` after generating user_gestures from gesture data collection (run only ONCE)

Audit directories of subjects by specifying the gesture set prefix.

TODO: insert GHOST image and description of process

## Numeric Gesture Data Collection and Exploration

TODO
