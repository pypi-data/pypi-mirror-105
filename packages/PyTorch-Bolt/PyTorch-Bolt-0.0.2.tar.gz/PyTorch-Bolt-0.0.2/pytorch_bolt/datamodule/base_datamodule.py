#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#<https://pytorch.org/tutorials/recipes/recipes/custom_dataset_transforms_loader.html>

import abc
import argparse
import pathlib


class BaseDataModule(abc.ABC):

    def __init__(self, args):
        self.data_dir = pathlib.Path(args.data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        # prepare data
        self._prepare_data()
        # setup dataset
        self.num_splits = args.num_splits
        self.trainset, self.valset, self.testset = self._setup_dataset()
        # configure dataloader
        self._use_dist_sampler = False

    @abc.abstractmethod
    def _prepare_data(self):
        return

    @abc.abstractmethod
    def _setup_dataset(self):
        # for fit stage

        # for test stage

        # return trainset, valset, testset
        raise NotImplementedError

    def use_dist_sampler(self):
        self._use_dist_sampler = True

    @abc.abstractmethod
    def train_dataloader(self):
        raise NotImplementedError

    @abc.abstractmethod
    def val_dataloader(self):
        raise NotImplementedError

    @abc.abstractmethod
    def test_dataloader(self):
        raise NotImplementedError

    @staticmethod
    def add_argparse_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument(
            '--data_dir',
            default='data',
            type=str,
            help='[DataModule] data directory',
        )
        parser.add_argument(
            '--num_splits',
            default=10,
            type=int,
            help='[DataModule] number of splits for trainset and valset',
        )
        return parser
