import torch

from helper_evaluate import compute_accuracy_ray
from helper_data import get_dataloaders_cifar10_ray
from helper_train import train_classifier_simple_ray, set_all_seeds
import ray.train.torch
from model import AlexNet
import pickle

# NOTE: This is an adaptation of https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/cnn/cnn-alexnet-cifar10.ipynb

config = {
    "random_seed": 1,
    "learning_rate": 0.0001,
    "num_epochs": 1,
    "batch_size": 256,
    "num_classes": 10,
}


def worker_train_func(config):

    set_all_seeds(config["random_seed"])

    train_loader, valid_loader, test_loader = get_dataloaders_cifar10_ray(
        batch_size=config["batch_size"], validation_fraction=0.1
    )
    # Ray: Prepare Dataloaders for distributed training
    # Shard the datasets among workers and move batches to the correct device
    train_loader = ray.train.torch.prepare_data_loader(train_loader)
    valid_loader = ray.train.torch.prepare_data_loader(valid_loader)
    test_loader = ray.train.torch.prepare_data_loader(test_loader)

    model = AlexNet(config["num_classes"])
    # Ray: Prepare and wrap your model with DistributedDataParallel
    # Move the model to the correct GPU/CPU device
    model = ray.train.torch.prepare_model(model)

    optimizer = torch.optim.Adam(model.parameters(), lr=config["learning_rate"])

    log_dict = train_classifier_simple_ray(
        num_epochs=config["num_epochs"],
        model=model,
        optimizer=optimizer,
        train_loader=train_loader,
        valid_loader=valid_loader,
        logging_interval=50,
    )

    with torch.set_grad_enabled(False):

        train_acc = compute_accuracy_ray(model=model, data_loader=train_loader)
        valid_acc = compute_accuracy_ray(model=model, data_loader=valid_loader)
        test_acc = compute_accuracy_ray(model=model, data_loader=test_loader)

        print(f"Train ACC: {train_acc:.2f}%")
        print(f"Validation ACC: {valid_acc:.2f}%")
        print(f"Test ACC: {test_acc:.2f}%")


use_gpu = torch.cuda.is_available()

# Ray: Configure scaling and resource requirements.
scaling_config = ray.train.ScalingConfig(num_workers=1, use_gpu=use_gpu)

# [5] Launch distributed training job.
trainer = ray.train.torch.TorchTrainer(
    train_loop_per_worker=worker_train_func,
    train_loop_config=config,
    scaling_config=scaling_config,
    run_config=ray.train.RunConfig(storage_path="~/data"),
)
result = trainer.fit()

with open("train_results.pkl", "wb") as resutls_file:
    pickle.dump(result, resutls_file)
