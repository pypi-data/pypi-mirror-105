#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#<https://pytorch.org/docs/stable/data.htm>

import argparse

import torch

from .base_datamodule import BaseDataModule


class DataModule(BaseDataModule):

    def __init__(self, args):
        super().__init__(args)
        # configure dataloader
        self.batch_size = args.batch_size
        self.num_workers = args.num_workers
        self.pin_memory = args.pin_memory
        self.drop_last = args.drop_last

    def _prepare_data(self):
        return

    def train_dataloader(self):
        return self._shared_dataloader(self.trainset, shuffle=True)

    def val_dataloader(self):
        return self._shared_dataloader(self.valset)

    def test_dataloader(self):
        return self._shared_dataloader(self.testset)

    def _shared_dataloader(self, dataset, shuffle=False):
        if self._use_dist_sampler:
            sampler = self._shared_sampler(dataset, shuffle)
            return torch.utils.data.DataLoader(
                dataset,
                batch_size=self.batch_size,
                sampler=sampler,
                num_workers=self.num_workers,
                pin_memory=self.pin_memory,
                drop_last=self.drop_last
            )
        else:
            return torch.utils.data.DataLoader(
                dataset,
                batch_size=self.batch_size,
                shuffle=shuffle,
                num_workers=self.num_workers,
                pin_memory=self.pin_memory,
                drop_last=self.drop_last
            )

    def _shared_sampler(self, dataset, shuffle):
        return torch.utils.data.distributed.DistributedSampler(
            dataset, shuffle=shuffle
        )

    @staticmethod
    def add_argparse_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        parser = BaseDataModule.add_argparse_args(parser)
        parser.add_argument(
            '--batch_size',
            default=1,
            type=int,
            help='[DataModule] number of samples per batch to load',
        )
        parser.add_argument(
            '--num_workers',
            default=0,
            type=int,
            help='[DataModule] number of subprocesses to use for data loading',
        )
        parser.add_argument(
            '--pin_memory',
            default=False,
            action='store_true',
            help='[DataModule] set to True to copy Tensors into CUDA pinned memory before returning them',
        )
        parser.add_argument(
            '--drop_last',
            default=False,
            action='store_true',
            help='[DataModule] set to True to drop the last incomplete batch',
        )
        return parser

    @classmethod
    def from_argparse_args(cls, args):
        return cls(args)
