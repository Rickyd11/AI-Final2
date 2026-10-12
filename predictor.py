import torch

class URLPredictor:

    def __init__(self, model, max_length=100):
        self.model = model
        self.max_length = max_length

    def encode_url(self, url):
        encoded = []

        for char in url[:self.max_length]:
            value = ord(char)

            if value >= 256:
                value = 255

            encoded.append(value)

        encoded += [0] * (self.max_length - len(encoded))

        return encoded

    def predict(self, url):
        self.model.eval()

        encoded = self.encode_url(url)

        input_tensor = torch.tensor(encoded, dtype=torch.long).unsqueeze(0)

        with torch.no_grad():
            output = self.model(input_tensor)
            probability = torch.sigmoid(output).item()

        is_phishing = probability >= 0.5

        return{
            "is_phishing": is_phishing, 
            "probability": probability
        }
