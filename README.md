# kserve-trustyai-explainer

## Local setup

### `docker-compose`

Start the `explainer` and `predictor` services with

```shell
docker-compose up --build -d
```

Once both services have started, the `explainer` will be available 
at [http://127.0.0.1:8888/v1/models/income:explain](http://127.0.0.1:8888/v1/models/income:explain)

You can request an explanation using an HTTP POST request such as

```shell
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
```

The search will take around 60 seconds, after which you would get a response similar to:

```json
{
  "0": {
    "features": "Age",
    "proposed": 40.0,
    "original": 40.0,
    "constrained": false,
    "difference": 0.0
  },
  "1": {
    "features": "Debt",
    "proposed": 3.4913362117281976,
    "original": 3.5,
    "constrained": false,
    "difference": -0.008663788271802364
  },
  "2": {
    "features": "YearsEmployed",
    "proposed": 3.4231348567845665,
    "original": 0.5,
    "constrained": false,
    "difference": 2.9231348567845665
  },
  "3": {
    "features": "Income",
    "proposed": 0.0,
    "original": 0.0,
    "constrained": false,
    "difference": 0.0
  }
}
```

## Kubernetes

To install it with KServe, proper, you need to have [minikube](https://minikube.sigs.k8s.io/docs/start/)
installed.

The explainer container will need to be built using `Docker` or `podman`.   
If you are using `podman` replace `CONTAINER=docker` with `CONTAINER=podman` in [install_k8s.sh](install_k8s.sh).

The deployment can be done by running

```shell
$ install_k8s.sh
```

Check that the predictor is correctly deployed. For instance:

```shell
kubectl get inferenceservices income
```

Should return something similar to:

```
NAME          URL                                      READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                   AGE
income   http://income.default.example.com             True           100                              sklearn-pvc-predictor-default-00001   7m27s
```

Example prediction request:

```shell
curl -H "Host: ${MODEL_NAME}.default.example.com" \
    http://$CLUSTER_IP/v1/models/income:predict \
    -d '{"instances":[[40, 3.5, 0.5, 0]]}'
```

Which should return:

```json
{"predictions": [0]}
```