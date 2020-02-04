from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import rasa_core
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig
from rasa_core.run import serve_application

logger = logging.getLogger(__name__)


def train_dialogue(domain_file='domain.yml',
                   model_path='models/dialogue',
                   train_data_file='data/stories.md'):
    fallback = FallbackPolicy(fallback_action_name="action_default_fallback",
                              core_threshold=0.3,
                              nlu_threshold=0.3)
    agent = Agent(domain_file, policies=[MemoizationPolicy(),
                                         KerasPolicy(max_history=3, epochs=200, batch_size=50),
                                         fallback])
    data = agent.load_data(train_data_file)

    agent.train(data)
    agent.persist(model_path)
    return agent


def run_provider_bot():
    interpreter = RasaNLUInterpreter('./models/prior_auth_nlu/default/model_20190425-074151')
    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
    agent = Agent.load('./models/dialogue', interpreter=interpreter, action_endpoint=action_endpoint)
    rasa_core.run.serve_application(agent, channel='cmdline')


if __name__ == '__main__':
    train_dialogue()
    run_provider_bot()
