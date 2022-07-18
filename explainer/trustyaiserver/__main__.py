import argparse
import kserve

from trustyaiserver import TrustyAIModel

DEFAULT_MODEL_NAME = "explainer"

DEFAULT_MAX_ITER = "1000"

parser = argparse.ArgumentParser(parents=[kserve.model_server.parser])
parser.add_argument('--model_name', default=DEFAULT_MODEL_NAME,
                    help='The name that the model is served under.')
parser.add_argument('--max_iter', default=DEFAULT_MAX_ITER,
                    help='The max number of iterations to run.')

parser.add_argument('--predictor_host', help='The host for the predictor', required=True)
args, _ = parser.parse_known_args()

if __name__ == "__main__":
    model = TrustyAIModel(args.model_name, args.predictor_host, max_iter=args.max_iter)
    model.load()
    kserve.ModelServer().start([model], nest_asyncio=True)
