from helper_evaluate import compute_accuracy_ray
from helper_evaluate import compute_epoch_loss_ray

import time
import torch
import torch.nn.functional as F

import os
import time
import random
import numpy as np
import tempfile

import ray.train.torch

# NOTE: This is an adaptation of https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/cnn/cnn-alexnet-cifar10.ipynb


def save_checkpoint(epoch, model, loss):
    # Report metrics and checkpoint.
    metrics = {"loss": loss.item(), "epoch": epoch}
    with tempfile.TemporaryDirectory() as temp_checkpoint_dir:
        torch.save(model.state_dict(), os.path.join(temp_checkpoint_dir, "model.pt"))
        # Ray: Report metrics to Ray Train
        ray.train.report(
            metrics,
            checkpoint=ray.train.Checkpoint.from_directory(temp_checkpoint_dir),
        )
    if ray.train.get_context().get_world_rank() == 0:
        print(metrics)


def eval_model(epoch, num_epochs, model, train_loader, valid_loader, log_dict):
    model.eval()

    with torch.set_grad_enabled(False):  # save memory during inference

        train_acc = compute_accuracy_ray(model, train_loader)
        train_loss = compute_epoch_loss_ray(model, train_loader)
        print(
            f"Epoch: {epoch+1:03}/{num_epochs:03} | Train. Acc.: {train_acc:.3f}% | Loss: {train_loss:.4f}"
        )
        log_dict["train_loss_per_epoch"].append(train_loss.item())
        log_dict["train_acc_per_epoch"].append(train_acc.item())

        if valid_loader is not None:
            valid_acc = compute_accuracy_ray(model, valid_loader)
            valid_loss = compute_epoch_loss_ray(model, valid_loader)
            print(
                f"Epoch: {epoch+1:03}/{num_epochs:03} | Valid. Acc.: {valid_acc:.3f}% | Loss: {valid_loss:.4f}"
            )
            log_dict["valid_loss_per_epoch"].append(valid_loss.item())
            log_dict["valid_acc_per_epoch"].append(valid_acc.item())


def train_classifier_simple_ray(
    num_epochs,
    model,
    optimizer,
    train_loader,
    valid_loader=None,
    loss_fn=None,
    logging_interval=100,
    skip_epoch_stats=False,
):

    log_dict = {
        "train_loss_per_batch": [],
        "train_acc_per_epoch": [],
        "train_loss_per_epoch": [],
        "valid_acc_per_epoch": [],
        "valid_loss_per_epoch": [],
    }

    if loss_fn is None:
        loss_fn = F.cross_entropy
    num_batches = len(train_loader)

    start_time = time.time()
    for epoch in range(num_epochs):

        model.train()
        for batch_idx, (features, targets) in enumerate(train_loader):
            # Ray: This is done by `prepare_data_loader`!
            # features = features.to(device)
            # targets = targets.to(device)

            # FORWARD AND BACK PROP
            logits = model(features)

            loss = loss_fn(logits, targets)
            optimizer.zero_grad()
            loss.backward()

            # UPDATE MODEL PARAMETERS
            optimizer.step()

            # LOGGING
            log_dict["train_loss_per_batch"].append(loss.item())

            if not batch_idx % logging_interval:
                print(
                    f"Epoch: {epoch+1:03}/{num_epochs:03} | Batch {batch_idx:04}/{num_batches:04} | Loss: {loss:.4f}"
                )

        save_checkpoint(epoch, model, loss)

        eval_model(epoch, num_epochs, model, train_loader, valid_loader, log_dict)

        print(f"Time elapsed: {((time.time() - start_time)/60):.2f}")

    print(f"Total Training Time: {((time.time() - start_time)/60):.2f}")

    return log_dict


def set_all_seeds(seed):
    os.environ["PL_GLOBAL_SEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def set_deterministic():
    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
    torch.set_deterministic(True)
