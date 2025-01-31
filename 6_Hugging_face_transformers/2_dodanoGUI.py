import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
import evaluate
import numpy as np


class SentimentAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sentiment Analysis Trainer")
        self.root.geometry("800x600")

        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Dataset parameters
        ttk.Label(main_frame, text="Dataset Parameters", font=('Helvetica', 12, 'bold')).grid(row=0, column=0,
                                                                                              columnspan=2, pady=10)

        ttk.Label(main_frame, text="Test Size:").grid(row=1, column=0, sticky=tk.W)
        self.test_size = ttk.Entry(main_frame)
        self.test_size.insert(0, "0.1")
        self.test_size.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="Random Seed:").grid(row=2, column=0, sticky=tk.W)
        self.random_seed = ttk.Entry(main_frame)
        self.random_seed.insert(0, "42")
        self.random_seed.grid(row=2, column=1, sticky=tk.W)

        # Model parameters
        ttk.Label(main_frame, text="Model Parameters", font=('Helvetica', 12, 'bold')).grid(row=3, column=0,
                                                                                            columnspan=2, pady=10)

        ttk.Label(main_frame, text="Model Checkpoint:").grid(row=4, column=0, sticky=tk.W)
        self.model_checkpoint = ttk.Entry(main_frame)
        self.model_checkpoint.insert(0, "distilbert-base-uncased")
        self.model_checkpoint.grid(row=4, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="Learning Rate:").grid(row=5, column=0, sticky=tk.W)
        self.learning_rate = ttk.Entry(main_frame)
        self.learning_rate.insert(0, "2e-5")
        self.learning_rate.grid(row=5, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="Batch Size:").grid(row=6, column=0, sticky=tk.W)
        self.batch_size = ttk.Entry(main_frame)
        self.batch_size.insert(0, "16")
        self.batch_size.grid(row=6, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="Number of Epochs:").grid(row=7, column=0, sticky=tk.W)
        self.num_epochs = ttk.Entry(main_frame)
        self.num_epochs.insert(0, "2")
        self.num_epochs.grid(row=7, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="Max Sequence Length:").grid(row=8, column=0, sticky=tk.W)
        self.max_length = ttk.Entry(main_frame)
        self.max_length.insert(0, "128")
        self.max_length.grid(row=8, column=1, sticky=tk.W)

        # Output parameters
        ttk.Label(main_frame, text="Output Parameters", font=('Helvetica', 12, 'bold')).grid(row=9, column=0,
                                                                                             columnspan=2, pady=10)

        ttk.Label(main_frame, text="Save Directory:").grid(row=10, column=0, sticky=tk.W)
        self.save_directory = ttk.Entry(main_frame)
        self.save_directory.insert(0, "my_finetuned_model")
        self.save_directory.grid(row=10, column=1, sticky=tk.W)

        # Progress display
        ttk.Label(main_frame, text="Progress", font=('Helvetica', 12, 'bold')).grid(row=11, column=0, columnspan=2,
                                                                                    pady=10)

        self.progress_text = scrolledtext.ScrolledText(main_frame, height=10, width=70)
        self.progress_text.grid(row=12, column=0, columnspan=2, pady=5)

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=13, column=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(button_frame, text="Start Training", command=self.start_training)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_training, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.training_running = False

    def log_progress(self, message):
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)

    def start_training(self):
        if self.training_running:
            return

        self.training_running = True
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)

        # Start training in a separate thread
        training_thread = threading.Thread(target=self.run_training)
        training_thread.start()

    def stop_training(self):
        self.training_running = False
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)

    def run_training(self):
        try:
            self.log_progress("Loading dataset...")
            dataset = load_dataset("yelp_polarity")

            test_size = float(self.test_size.get())
            seed = int(self.random_seed.get())

            split_dataset = dataset["train"].train_test_split(test_size=test_size, seed=seed)
            train_dataset = split_dataset["train"]
            val_dataset = split_dataset["test"]
            test_dataset = dataset["test"]

            self.log_progress("Loading tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(self.model_checkpoint.get())

            max_length = int(self.max_length.get())

            def tokenize_function(example):
                return tokenizer(
                    example["text"],
                    padding="max_length",
                    truncation=True,
                    max_length=max_length
                )

            self.log_progress("Tokenizing datasets...")
            train_dataset_tokenized = train_dataset.map(tokenize_function, batched=True)
            val_dataset_tokenized = val_dataset.map(tokenize_function, batched=True)
            test_dataset_tokenized = test_dataset.map(tokenize_function, batched=True)

            self.log_progress("Loading model...")
            model = AutoModelForSequenceClassification.from_pretrained(
                self.model_checkpoint.get(),
                num_labels=2
            )

            training_args = TrainingArguments(
                output_dir=self.save_directory.get(),
                eval_strategy="epoch",
                save_strategy="epoch",
                learning_rate=float(self.learning_rate.get()),
                per_device_train_batch_size=int(self.batch_size.get()),
                per_device_eval_batch_size=int(self.batch_size.get()),
                num_train_epochs=int(self.num_epochs.get()),
                logging_steps=200,
                load_best_model_at_end=True,
                metric_for_best_model="accuracy"
            )

            accuracy_metric = evaluate.load("accuracy")
            f1_metric = evaluate.load("f1")

            def compute_metrics(eval_pred):
                logits, labels = eval_pred
                predictions = np.argmax(logits, axis=-1)
                acc = accuracy_metric.compute(predictions=predictions, references=labels)
                f1 = f1_metric.compute(predictions=predictions, references=labels, average="weighted")
                return {
                    "accuracy": acc["accuracy"],
                    "f1": f1["f1"]
                }

            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=train_dataset_tokenized,
                eval_dataset=val_dataset_tokenized,
                compute_metrics=compute_metrics
            )

            self.log_progress("Starting training...")
            trainer.train()

            self.log_progress("Evaluating on test set...")
            test_results = trainer.evaluate(test_dataset_tokenized)
            self.log_progress(f"Test results: {test_results}")

            self.log_progress("Saving model and tokenizer...")
            trainer.save_model(self.save_directory.get())
            tokenizer.save_pretrained(self.save_directory.get())
            self.log_progress(f"Model saved to {self.save_directory.get()}")

            messagebox.showinfo("Success", "Training completed successfully!")

        except Exception as e:
            self.log_progress(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            self.training_running = False
            self.root.after(0, self.stop_training)


if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentAnalysisGUI(root)
    root.mainloop()