import albumentations as A
import pytorch_lightning as pl
from torch.utils.data import DataLoader, Subset

import wandb
from utils import RandomPaste

from .dataset import LabeledDataset, SyntheticDataset


class Spheres(pl.LightningDataModule):
    def __init__(self):
        super().__init__()

    def train_dataloader(self):
        transform = A.Compose(
            [
                A.Resize(wandb.config.IMG_SIZE, wandb.config.IMG_SIZE),
                A.Flip(),
                A.ColorJitter(),
                RandomPaste(wandb.config.SPHERES, wandb.config.DIR_SPHERE),
                A.GaussianBlur(),
                A.ISONoise(),
            ],
        )

        dataset = SyntheticDataset(image_dir=wandb.config.DIR_TRAIN_IMG, transform=transform)
        dataset = Subset(dataset, list(range(0, len(dataset), len(dataset) // 10000 + 1)))

        return DataLoader(
            dataset,
            shuffle=True,
            batch_size=wandb.config.BATCH_SIZE,
            num_workers=wandb.config.WORKERS,
            pin_memory=wandb.config.PIN_MEMORY,
        )

    def val_dataloader(self):
        dataset = LabeledDataset(image_dir=wandb.config.DIR_VALID_IMG)
        dataset = Subset(dataset, list(range(0, len(dataset), len(dataset) // 100 + 1)))

        return DataLoader(
            dataset,
            shuffle=False,
            batch_size=1,
            num_workers=wandb.config.WORKERS,
            pin_memory=wandb.config.PIN_MEMORY,
        )
