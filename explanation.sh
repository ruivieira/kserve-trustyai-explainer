#!/usr/bin/env sh

curl --request POST \
  --url http://127.0.0.1:8888/v1/models/income:explain \
  --header 'Content-Type: application/json' \
  --data '{"inputs": {
        "Age":{ "value": 40, "domain": [0, 100] },
        "Debt": { "value": 3.5, "domain": [0, 10]},
        "YearsEmployed":{ "value": 0.5, "domain": [1, 10]},
        "Income": { "value": 0, "domain": [0, 300]}
    },
    "goal": {
        "Approved": {
        "value": 1
        }
    }
}'