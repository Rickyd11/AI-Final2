import torch
from torch import nn
from torch.utils.data import DataLoader

class ModelTrainer:

    def __init__( self,model, learning_rate=0.001, batch_size=4):
        self.model = model
        self.loss_function = nn.BCEWithLogitsLoss()

        self.optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        self.batch_size = batch_size

    def train(self, dataset, epochs=50):
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

        for epoch in range(epoch):
            self.model.train()

            running_loss = 0.0

            for features, targets in loader:

                self.optimizer.zero_grad()
                outputs = self.model(features)
                loss = self.loss_function(outputs, targets)

                loss.backward()
                self.optimizer.step()

                running_loss += loss.item()

                average_loss = running_loss / len(loader)
                print(f"Epoch {epoch + 1}/{epochs} "f"- Loss: {average_loss:.4f}")

        print("Training Complete")


    def save(self,path):
        torch.save(self.model.state_dict(), path)


