import accelerate
import torch
from torch.utils.data import DataLoader, Dataset

import transformers
from transformers import (
    DistilBertConfig,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
)


class SimpleDataset(Dataset):
    def __init__(self):

        # Dummy data: 10 samples
        self.labels = [0] * 10
        self.input_ids = torch.randint(1, 1000, (10, 64))

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {
            "input_ids": self.input_ids[idx].to(dtype=torch.long),
            "labels": torch.tensor(self.labels[idx], dtype=torch.long),
        }
        return item


# Initialize a dataset
dataset = SimpleDataset()

# Load a pre-configured model and tokenizer
config = DistilBertConfig(num_labels=2)
model = DistilBertForSequenceClassification(config)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",  # Output directory for model predictions and checkpoints
    num_train_epochs=10,  # Total number of training epochs
    per_device_train_batch_size=2,  # Batch size per device during training
    warmup_steps=500,  # Number of warmup steps for learning rate scheduler
    weight_decay=0.01,  # Strength of weight decay
    logging_dir="./logs",  # Directory for storing logs
    logging_steps=10,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Start training
trainer.train()
