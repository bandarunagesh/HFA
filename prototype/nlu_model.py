from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter


def train_nlu(data, configs, model_dir):
    training_data = load_data(data)
    trainer = Trainer(config.load(configs))
    trainer.train(training_data)
    trainer.persist(model_dir, fixed_model_name="priorauthnlu")


def run_nlu():
    interpreter = Interpreter.load('./models/prior_auth_nlu/default/model_20190425-074151')
    print(interpreter.parse(u"I need the top 5 reasons for partial denials"))
    print(interpreter.parse("how many requests with medical records submitted"))
    print(interpreter.parse("Thanks"))


if __name__ == "__main__":
    train_nlu('./data/PriorAuthData.json', './config_files/config.json', './models/prior_auth_nlu')
    run_nlu()
