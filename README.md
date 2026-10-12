# AI-Phishing-URL-Detector

Overview:
The project is a AI-powered phishing detection software that allows for users to submit a url link that they are suspicious of and return a probability of the likelihood that the url is a phishing url.

This project uses Pytorch to train a neural network to recognize patterns in the urls that may indicate phishing, such as suspicious subdomains, unusual character combinations, and random-looking strings.

How it works:
The model treats each URL as a sequence of characters instead of analyzing it as a complete web address.

1. Character Encoding: Each character in the URL is represented by a numerical value based on its ASCII value (0–255).
2. Embedding Layer: The model converts each character value into a vector representation. This helps the model learn patterns between characters and their positions within a URL.
3. Flattening: The character vectors are combined into a single sequence of numbers that can be processed by the next layers.
4. Neural Network: The flattened data passes through fully connected layers that use ReLU activation functions to learn patterns associated with phishing and legitimate URLs.
5. Prediction: The model outputs a score that is converted into a probability using a sigmoid function. A higher score indicates that the URL is more likely to be phishing, while a lower score indicates that it is more likely to be legitimate.

Technology Used
- Python — Main programming language
- PyTorch — Neural network development and training
- Tkinter — Graphical user interface
- URL Validation — Checks whether the input is formatted as a valid URL


