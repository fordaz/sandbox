import torch
import torch.nn.functional as F
import numpy as np
from itertools import product

# NOTE: This is an adaptation of https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/cnn/cnn-alexnet-cifar10.ipynb


def compute_accuracy_ray(model, data_loader):
    model.eval()
    with torch.no_grad():
        correct_pred, num_examples = 0, 0
        for i, (features, targets) in enumerate(data_loader):
            # Ray: This is done by `prepare_data_loader`!
            # features = features.to(device)
            # targets = targets.to(device)

            logits = model(features)
            _, predicted_labels = torch.max(logits, 1)
            num_examples += targets.size(0)
            correct_pred += (predicted_labels == targets).sum()
    return correct_pred.float() / num_examples * 100


def compute_epoch_loss_ray(model, data_loader):
    model.eval()
    curr_loss, num_examples = 0.0, 0
    with torch.no_grad():
        for features, targets in data_loader:
            # Ray: This is done by `prepare_data_loader`!
            # features = features.to(device)
            # targets = targets.to(device)
            logits = model(features)
            loss = F.cross_entropy(logits, targets, reduction="sum")
            num_examples += targets.size(0)
            curr_loss += loss

        curr_loss = curr_loss / num_examples
        return curr_loss
