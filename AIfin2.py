import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import ToTensor
import validators
import torch.optim as optim
import tkinter as tk
from tkinter import messagebox

# Setting up the Loss
loss=nn.BCEWithLogitsLoss()


class PhishingModel(nn.Module):
    def __init__(self, vocab_size,embedding_dim = 16, input_size = 100):
        super(PhishingModel,self).__init__()
        # Lookup table for 256 possible ASCII characters
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.flatten = nn.Flatten()
        # Input size is now (length of URL * size of each embedding vector)
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_size * embedding_dim, 512),
            nn.ReLU(),
            nn.Linear(512,1)
        )

    def forward(self,x):
        # Transform character IDs to vectors
        x = self.embedding(x)
        # Flatten to (Batch, input_length * embedding_dim)
        x = self.flatten(x)
        log=self.linear_relu_stack(x)
        return log

model=PhishingModel(vocab_size=256, input_size=100)
class URLDataset(Dataset):
    # Creating the Dataset
    def __init__(self, urls, labels, max_length=128):
        """
        Args:
            urls (list): List of URL strings.
            labels (list): List of integers (0 for safe, 1 for phishing).
            max_length (int): Fixed length for all URL vectors (padding/truncating).
        """
        self.data = []
        self.max_length = max_length

        for url, label in zip(urls, labels):
            # Use validators to ensure data quality
            if validators.url(url):
                #Get raw ASCII integer values (0-255)
                encoded_url = [ord(char) for char in url[:max_length]]
                # Pad with 0s if the URL is too short
                encoded_url += [0] * (max_length - len(encoded_url))
                
                # Convert to Tensors
                feature = torch.tensor(encoded_url, dtype=torch.long)
                target = torch.tensor([label], dtype=torch.float32)
                
                self.data.append((feature, target))
            else:
                print(f"Skipping invalid URL: {url}")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
# # List for training
# training_urls = [
#     "https://www.espn.com/", 
#     "https://domicilerelais.pro/", 
#     "https://www.ulta.com/", 
#     "https://domicilerelais.pro/74946779", 
#     "https://www.cbsnews.com/", 
#     "https://votredomicile.pro/",
#     "https://www.dhs.gov/",
#     "https://www.youtube.com/watch?v=T3_UNFZHSQU",
#     "https://votredomicile.pro/74946779", 
#     "https://sportybetreedembonus04.weebly.com/",
#     "https://requirments3500040142.weebly.com/",
#     "https://tcbonepiecechapters.com/", 
#     "https://play.pokemonshowdown.com/", 
#     "https://identity.hudl.com/u/login/identifier?state=hKFo2SBBdmZoODZ1YVA0aFBxOU03MG5qdGdXN2pHc3ZfaGNtV6Fur3VuaXZlcnNhbC1sb2dpbqN0aWTZIHpJcDRuNzJiUERMNzRHUVlpSFE5T0l1a2RoQ2lWa1Z6o2NpZNkgbjEzUmZrSHpLb3phTnhXQzVkWlFvYmVXR2Y0V2pTbjU", 
#     "https://github.com/",
#     "https://allegrolokalnie.pl-ofert63006290.click/oferta/procesor-amd-ryzen-7-5800x3d", 
#     "https://tinyurl.com/Shopee15-user",
#     "pinterest.com",
#     "naver.com",
#     "tiktok.com",
#     "weather.com",
#     "https://fair-node.assyrfantasy.in.net/05fe317c-0981-4de2-bc8a-930d369db441/ck-3d80df5d12cdfe6450a782fc87bf66b444.google",
#     "http://115.55.239.151:49191/bin.sh","https://slot-api.covercotehour.in.net/05fe317c-0981-4de2-bc8a-930d369db441/ck-3d80df5d12cdfe6450a782fc87bf66b444.google",
#     "https://layer-check.systemicitylayer.in.net/05fe317c-0981-4de2-bc8a-930d369db441/ck-3d80df5d12cdfe6450a782fc87bf66b444.google",
#     "https://espressobot.gitbook.io/espressobot-docs",
#     "eBay.com",
#     "https://www.microsoft.com/en-us/microsoft-365/outlook/log-in",
#     "http://110.37.118.66:54586/bin.sh",
#     "https://trezointro.wixstudio.com/bridge-en",
#     "https://update-bridge.wixstudio.com/get-bridge",
#     "https://beginstart-com.wixstudio.com/en-us",
#     "https://liveintro.wixstudio.com/en-desktop",
#     "https://bridges-install.wixstudio.com/en-us",
#     "https://srfgsre6.lat/zmoyslfl/1YbAn3/RzH53y",
#     "https://www.biblegateway.com/passage/?search=Proverbs+1&version=ESV",
#     "https://8wjet5fe.lat/zmoyslfl/1YbAn3/RzH53y",
#     "YouTube.com",
#     "https://893nwet.lat/zmoyslfl/1YbAn3/RzH53y",
#     "Facebook.com",
#     "x.com",
#     "Instagram.com",
#     "https://openfront.io/",
#     "https://nandgator.github.io/pyvalidators/stable/api/url/",
#     "https://srfgsre6.lat/zmoyslfl/1YbAn3/RzH53y",
#      "https://auths-livelgr-eng.framer.ai/eng","http://mitamxsklogun.gitbook.io","https://club-italiano.com/web/pages/","https://urlhaus.abuse.ch/url/3814015/","youtube.com/watch?v=m3kR2KK8TEs&source_ve_path=NzY3NTg&embeds_referring_euri=https%3A%2F%2Fwww.nasa.gov%2F","https://rainbet.com/","prosperacan.com","https://betasus-yilbasindakazankazan.com","http://securecloud.hosting"

# ]
# # 0 indicator for real url 1 indicator for phishing url
# training_labels = [0,1,0,1,0,1,0,0,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1]
# # Create the dataset
# dataset = URLDataset(training_urls, training_labels, max_length=100)
# optimizer = optim.Adam(model.parameters(), lr=0.001)
# training_loader=DataLoader(dataset, batch_size=4, shuffle=True)

# print(f"Dataset size: {len(dataset)}") 


# url_tensor, label_tensor = dataset[0]
# print(f"Encoded URL Tensor shape: {url_tensor.shape}")

# epochs = 50 

# for epoch in range(epochs):
#     model.train() # Set PhishingModel to training mode
#     running_loss = 0.0
#     for batch_features, batch_targets in training_loader:
#         optimizer.zero_grad()
#         outputs = model(batch_features)
#         loss_value = loss(outputs, batch_targets)
#         loss_value.backward()
#         optimizer.step()
#         running_loss += loss_value.item()
#         if (epoch + 1) % 10 == 0:
#             # Saving the model incase the code crashes and doesn't cause issues
#             torch.save(model.state_dict(), "phishing_model.pth")
#             print(f"Epoch [{epoch+1}/{epochs}], Average Loss: {running_loss/len(training_loader):.4f}")
#     print("Complete")

def predict_url(url, model, max_length=100):
    # Set to evaluation mode
    model.eval()
    # Disable gradient calculation to save time
    with torch.no_grad():
        encoded = [ord(char) for char in url[:max_length]]
        encoded += [0] * (max_length - len(encoded))
        
        input_tensor = torch.tensor(encoded, dtype=torch.long).unsqueeze(0)
        
        # Get prediction
        output = model(input_tensor)
        # Converts to probability
        probability = torch.sigmoid(output).item()
        # Determines if the link is phishing or not
        if probability >= 0.5:
            status = "Phishing" 
            color="red"
        else: 
           status="Safe"
           color="green"
        result_label.config(text=f"Result: {status}", foreground=color)
        prob_label.config(text=f"Confidence: {probability:%}")

model.load_state_dict(torch.load("phishing_model.pth"))
model.eval()


def middle():
    url = user_input.get().strip()
    predict_url(url,model)
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL")
        return
root=tk.Tk()
root.title("Phishing Detecor")
root.geometry("1000x10000")
root.padx=20
tk.Label(root, text="Enter URL for the AI to predict:", font=("Arial", 18, "bold")).pack(pady=10)
user_input = tk.Entry(root, width=40)
user_input.pack(pady=5)
predict_btn = tk.Button(root, text="Check URL", command=middle, bg="#0078d7", fg="black", font=("Arial", 10, "bold"))
predict_btn.pack(pady=15)
result_label = tk.Label(root, text="Result: Waiting...", font=("Arial", 18))
result_label.pack()

prob_label = tk.Label(root, text="Confidence: 0%", font=("Arial", 18, "italic"))
prob_label.pack()

root.mainloop()
