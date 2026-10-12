
import torch
from torch import nn


class PhishingModel(nn.Module):
    def __init__(self, vocab_size=256, embedding_dim=16, input_size=100, hidden_size=512):
        super().__init__()

        # Convert URL characters into embeddings.
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        # Flatten the embeddings before classification.
        self.flatten = nn.Flatten()

        # Keep these layer indexes consistent with the saved model.
        self.linear_relu_stack = nn.Sequential(nn.Linear(input_size * embedding_dim, hidden_size), nn.ReLU(), nn.Linear(hidden_size, 1))

    def forward(self, x):
        x = self.embedding(x)
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits
