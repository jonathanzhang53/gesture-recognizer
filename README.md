# $1 Gesture Recognizer

## Authors

Katherine Chan, Thomas Ruby, Jonathan Zhang

## Prerequisities

1. Python 3.10+ and pip

2. `pip install -r requirements.txt`

## Online Recognition

`python src/1_dollar.py true`

TODO: insert image and description of process

## Offline / Test Recognition

`python src/1_dollar.py false [OPTIONAL: iterations] [OPTIONAL: num users]`

- Defaults: 10 iterations, 1 user

TODO: insert image and description of process

## Collecting Gesture Data

`python src/gather_gestures.py true [OPTIONAL: username] [OPTIONAL: sample # to resume at]`

TODO: insert image and description of process

Once you collect your batch of user gestures, make sure to copy the data elsewhere before collecting a new batch to ensure that data from different experiments is separated.

## Data Exploration

`python src/audit_gestures.py` after generating user_gestures from gesture data collection (run only ONCE)

TODO: insert GHOST image and description of process

## Numeric Gesture Data Collection and Exploration

TODO
