#!/usr/bin/env sh
cd predictor || exit
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python python -m sklearnserver --model_dir ./  --model_name income --protocol seldon.http --http_port 8888