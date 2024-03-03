import torch
from torchvision import datasets
from torch.utils.data import DataLoader
from torch.utils.data import SubsetRandomSampler
from torchvision import transforms
from filelock import FileLock
import os

# NOTE: This is an adaptation of https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/cnn/cnn-alexnet-cifar10.ipynb


def get_dataloaders_cifar10_ray(batch_size, num_workers=0, validation_fraction=0.1):

    train_transforms = transforms.Compose(
        [
            transforms.Resize((70, 70)),
            transforms.RandomCrop((64, 64)),
            transforms.ToTensor(),
        ]
    )

    test_transforms = transforms.Compose(
        [
            transforms.Resize((70, 70)),
            transforms.RandomCrop((64, 64)),
            transforms.ToTensor(),
        ]
    )
    # Ray: to avoid download the data multiple times when workers run on the same host
    with FileLock(os.path.expanduser("~/data.lock")):
        train_dataset = datasets.CIFAR10(
            root="data", train=True, transform=train_transforms, download=True
        )

        valid_dataset = datasets.CIFAR10(
            root="data", train=True, transform=test_transforms
        )

        test_dataset = datasets.CIFAR10(
            root="data", train=False, transform=test_transforms
        )

        num = int(validation_fraction * 50000)
        train_indices = torch.arange(0, 50000 - num)
        valid_indices = torch.arange(50000 - num, 50000)

        train_sampler = SubsetRandomSampler(train_indices)
        valid_sampler = SubsetRandomSampler(valid_indices)

        valid_loader = DataLoader(
            dataset=valid_dataset,
            batch_size=batch_size,
            num_workers=num_workers,
            sampler=valid_sampler,
        )

        train_loader = DataLoader(
            dataset=train_dataset,
            batch_size=batch_size,
            num_workers=num_workers,
            drop_last=True,
            sampler=train_sampler,
        )

        test_loader = DataLoader(
            dataset=test_dataset,
            batch_size=batch_size,
            num_workers=num_workers,
            shuffle=False,
        )

        return train_loader, valid_loader, test_loader
