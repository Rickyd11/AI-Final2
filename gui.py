
import tkinter as tk
from tkinter import messagebox


class PhishingGUI:
    def __init__(self, predictor):
        self.predictor = predictor

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Phishing URL Detector")
        self.root.geometry("600x400")
        self.root.minsize(500, 350)
        self.root.configure(bg="#f4f6f8")

        # Main container
        self.main_frame = tk.Frame(
            self.root,
            bg="#f4f6f8",
            padx=30,
            pady=25
        )
        self.main_frame.pack(fill="both", expand=True)

        # Title
        self.title_label = tk.Label(self.main_frame, text="Phishing URL Detector", font=("Arial", 20, "bold"), bg="#f4f6f8", fg="#1f2937")
        self.title_label.pack(pady=(0, 10))

        # Description
        self.description_label = tk.Label(self.main_frame, text="Enter a URL to check the model's prediction.", font=("Arial", 11), bg="#f4f6f8", fg="#4b5563")
        self.description_label.pack(pady=(0, 20))

        # URL input label
        self.url_label = tk.Label(self.main_frame, text="Website URL", font=("Arial", 11, "bold"), bg="#f4f6f8", fg="#1f2937")
        self.url_label.pack(anchor="w")

        # URL input field
        self.url_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=50, relief="solid", bd=1)
        self.url_entry.pack(fill="x", ipady=8, pady=(5, 15))
        self.url_entry.bind("<Return>", lambda event: self.check_url())

        # Check button
        self.check_button = tk.Button(self.main_frame, text="Check URL", command=self.check_url, font=("Arial", 12, "bold"), bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", relief="flat", cursor="hand2", padx=20, pady=8)
        self.check_button.pack(pady=(0, 20))

        # Prediction result
        self.result_label = tk.Label(self.main_frame, text="Enter a URL to begin.", font=("Arial", 14, "bold"), bg="#f4f6f8", fg="#374151", wraplength=500)
        self.result_label.pack(pady=(0, 10))

        # Prediction probability
        self.probability_label = tk.Label(self.main_frame, text="", font=("Arial", 11), bg="#f4f6f8", fg="#4b5563")
        self.probability_label.pack()

        # Disclaimer
        self.disclaimer_label = tk.Label(self.main_frame, text=("This is a machine-learning prediction, not a guarantee " "that a website is safe or malicious."), font=("Arial", 9), bg="#f4f6f8", fg="#6b7280", wraplength=500, justify="center")
        self.disclaimer_label.pack(side="bottom", pady=(20, 0))

    def check_url(self):
        # Read and clean the URL
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showwarning("Missing URL", "Please enter a URL before checking.")
            self.url_entry.focus_set()
            return

        # Prevent the interface from showing an old result
        self.result_label.config(text="Checking URL...", fg="#374151")
        self.probability_label.config(text="")
        self.root.update_idletasks()

        try:
            # Get the prediction from the predictor
            result = self.predictor.predict(url)

            is_phishing = result["is_phishing"]
            probability = float(result["probability"])

            # Display the prediction
            if is_phishing:
                self.result_label.config(text="Warning: Model predicts this URL is phishing.", fg="#dc2626")
            else:
                self.result_label.config(text="Model predicts this URL is likely legitimate.", fg="#15803d")

            # Display the model's phishing score
            self.probability_label.config(text=f"Phishing score: {probability:.2%}")

        except Exception as error:
            self.result_label.config(text="Unable to check this URL.", fg="#dc2626")
            self.probability_label.config(text="")

            messagebox.showerror("Prediction Error",f"An error occurred while checking the URL:\n\n{error}")

    def run(self):
        self.root.mainloop()
