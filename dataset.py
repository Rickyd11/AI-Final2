import torch
from torch.utils.data import Dataset
import validators

class URLDataset(Dataset):

    def __init__(self, urls, labels, max_length=100):
        self.data = []
        self.max_length = max_length

        for url, label in zip(urls, labels):

            if not validators.url(url):
                print(f"Skipping invalid URL: {url}")
                continue

            encoded_url = self.encode_url(url)

            feature = torch.tensor(encoded_url, dtype=torch.long)
            label = torch.tensor([label], dtype=torch.float32)

            self.data.append(feature, label)

    def encode_url(self , url):
        encoded = []

        for char in url[:self.max_length]:
            value = ord(char)

            # Keep values inside the embedding vocabulary
            if value >= 256:
                value = 255

            encoded.append(value)

        encoded += [0] * (self.max_length - len(encoded))
        return encoded

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]
