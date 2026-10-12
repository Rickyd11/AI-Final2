import torch

from model import PhishingModel
from predictor import URLPredictor
from gui import PhishingGUI
from config import (VOCAB_SIZE, EMBEDDING_DIM, MAX_URL_LENGTH, HIDDEN_SIZE, MODEL_PATH)


def load_model():

    model = PhishingModel(vocab_size=VOCAB_SIZE, embedding_dim=EMBEDDING_DIM, input_size=MAX_URL_LENGTH, hidden_size=HIDDEN_SIZE)

    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))

    return model


def main():

    model = load_model()

    predictor = URLPredictor(model, max_length=MAX_URL_LENGTH)

    app = PhishingGUI(predictor)

    app.run()


if __name__ == "__main__":
    main()
