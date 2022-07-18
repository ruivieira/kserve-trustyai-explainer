from typing import Dict
# import asyncio
import requests
import kserve

import trustyai

trustyai.init()

print("Started TrustyAI")

from trustyai.model import feature
from trustyai.explainers import CounterfactualExplainer
from trustyai.model import output
from trustyai.model import counterfactual_prediction
from org.kie.kogito.explainability.model import PredictionInput, PredictionOutput
from trustyai.model import Model

PREDICTOR_URL_FORMAT = "http://{0}/v1/models/{1}:predict"


class TrustyAIModel(kserve.Model):  # pylint:disable=c-extension-no-member
    def __init__(
        self,
        name: str,
        predictor_host: str,
        max_iter: str,
    ):
        super().__init__(name)
        self.name = name
        self.predictor_host = predictor_host
        self.ready = False
        self.count = 0
        self.explainer = CounterfactualExplainer(steps=10_000)

    def load(self) -> bool:
        self.ready = True
        return self.ready

    def _predict(self, request):

        _inputs = request["inputs"]
        _goal = request["goal"]

        features = []
        for f in _inputs:
            feature_data = _inputs[f]
            print(feature_data)
            if "domain" in feature_data:
                domain = feature_data["domain"]
                features.append(
                    feature(
                        name=f,
                        value=feature_data["value"],
                        dtype="number",
                        domain=(domain[0], domain[1]),
                    )
                )
            else:
                features.append(
                    feature(name=f, value=feature_data["value"], dtype="number")
                )

        goals = []
        for g in _goal:
            goal_data = _goal[g]
            goals.append(output(name=g, dtype="number", value=goal_data["value"]))

        prediction = counterfactual_prediction(input_features=features, outputs=goals)

        def predict_provider(inputs):
            values = [_feature.value.as_obj() for _feature in inputs[0].features]
            scoring_data = {"instances": [values]}

            predict_url = PREDICTOR_URL_FORMAT.format(self.predictor_host, self.name)

            resp = requests.post(predict_url, json=scoring_data)

            data = resp.json()
            p = data["predictions"][0]
            _output = output(name="Country", dtype="number", value=p, score=1.0)
            return [PredictionOutput([_output])]

        model = Model(predict_provider)

        explanation = self.explainer.explain(prediction, model)

        return explanation

    def explain(self, request: Dict) -> Dict:

        explanation = self._predict(request=request)

        return explanation.as_dataframe().transpose().to_dict()
