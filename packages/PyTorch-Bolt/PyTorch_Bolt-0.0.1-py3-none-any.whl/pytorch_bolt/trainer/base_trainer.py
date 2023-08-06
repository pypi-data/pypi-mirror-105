#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#<https://pytorch.org/docs/stable/distributed.html>

import abc
import argparse

import torch


class BaseTrainer(abc.ABC):

    def __init__(self, args):
        # setup loggers
        self.loggers = args.loggers
        self.logger = self.loggers.configure_child_logger('trainer')
        self.tracker = self.loggers.configure_tracker()
        self.progressbar = self.loggers.configure_progressbar()
        self.writer = self.loggers.configure_writer()
        # specify device, recommended when using single-node single-GPU training
        self.device = args.device
        # configure distributed data parallel (DDP) training
        self.distributed = args.distributed
        self.use_slurm = args.use_slurm
        self.dist_backend = args.dist_backend        
        self.master_addr = args.master_addr
        self.master_port = args.master_port
        self.world_size = args.world_size
        self.rank = args.rank
        self.local_rank = args.local_rank
        self._setup_env()
        self._setup_device()
        self._init_proc()
        # setup datamodule
        self.datamodule = args.datamodule
        if self.distributed:
            self.datamodule.use_dist_sampler()
        self.train_dataloader = self.datamodule.train_dataloader()
        self.val_dataloader = self.datamodule.val_dataloader()
        self.test_dataloader = self.datamodule.test_dataloader()
        # setup model
        self.model = args.model
        self.criterion = self.model.configure_criterion()
        self.metric = self.model.configure_metric()
        self.optimizer, self.lr_scheduler = self.model.configure_optimizer()
        self._model_to_device()
        self._criterion_to_device()
        self._metric_to_device()
        self.max_epochs = args.max_epochs
        self.verbose = args.verbose

    @abc.abstractmethod
    def _setup_env(self):
        return

    @abc.abstractmethod
    def _setup_device(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _init_proc(self):
        return

    @abc.abstractmethod
    def _destroy_proc(self):
        return

    @abc.abstractmethod
    def _model_to_device(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _criterion_to_device(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _metric_to_device(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _training_epoch(self, epoch, tag='TRAIN'):
        # training_epoch_start
        self.model.train()
        for batch_idx, batch in enumerate(self.train_dataloader):
            # training_step (required)
            # dict, containing at least 2 keys: "loss", "score"
            step_outs = self._training_step(batch_idx, batch)
            # backpropagation
            self.optimizer.zero_grad()
            step_outs['loss'].backward()
            self.optimizer.step()
            # training_step_end
            step_outs = self._training_step_end(batch_idx, batch, step_outs)
        # training_epoch_end
        return self._training_epoch_end()

    @abc.abstractmethod
    def _training_step(self, batch_idx, batch):
        raise NotImplementedError

    @abc.abstractmethod
    def _training_step_end(self, batch_idx, batch, step_outs):
        return

    @abc.abstractmethod
    def _training_epoch_end(self):
        # if return
        # return dict, containing at least 2 keys: "loss", "score"
        return

    @abc.abstractmethod
    def _validation_epoch(self, epoch, dataloader, max_epochs, tag='VAL'):
        # validation_epoch_start
        self.model.eval()
        with torch.no_grad():
            for batch_idx, batch in enumerate(dataloader):
                # validation_step (required)
                # dict, containing at least 2 keys: "loss", "score"
                step_outs = self._validation_step(batch_idx, batch)
                # validation_step_end
                step_outs = self._validation_step_end(batch_idx, batch, step_outs)
        return self._validation_epoch_end()

    @abc.abstractmethod
    def _validation_step(self, batch_idx, batch):
        raise NotImplementedError

    @abc.abstractmethod
    def _validation_step_end(self, batch_idx, batch, step_outs):
        return

    @abc.abstractmethod
    def _validation_epoch_end(self):
        # if return
        # return dict, containing at least 2 keys: "loss", "score"
        return

    @abc.abstractmethod
    def _test_epoch(self, epoch, dataloader, max_epochs, tag='TEST'):
        return self._validation_epoch(epoch, dataloader, max_epochs, tag=tag)

    @abc.abstractmethod
    def fit(self):
        for epoch in range(1, self.max_epochs + 1):
            # one training epoch
            train_epoch_outs = self._training_epoch(epoch)
            # one vlaidation epoch
            val_epoch_outs = self._validation_epoch(epoch, self.val_dataloader, self.max_epochs)
            # lr_scheduler
            if self.lr_scheduler is not None:
                self.lr_scheduler.step()

    @abc.abstractmethod
    def validate(self):
        epoch, max_epochs = 1, 1
        epoch_outs = self._validation_epoch(epoch, self.val_dataloader, max_epochs)

    @abc.abstractmethod
    def test(self):
        epoch, max_epochs = 1, 1
        epoch_outs = self._test_epoch(epoch, self.test_dataloader, max_epochs)

    @abc.abstractmethod
    def destory(self):
        self._destroy_proc()

    @staticmethod
    def add_argparse_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument(
            '--loggers',
            default=None, #required=True,
            help='[Trainer] loggers for training',
        )
        parser.add_argument(
            '--device',
            default=None,
            type=str,
            help='[Trainer] device for training',
        )

        parser.add_argument(
            '--distributed',
            default=False,
            action='store_true',
            help='[Trainer] set to True to use DDP training',
        )
        parser.add_argument(
            '--use_slurm',
            default=False,
            action='store_true',
            help='[Trainer] set to True to use DDP training with Slurm',
        )
        parser.add_argument(
            '--dist_backend',
            default='nccl',
            type=str,
            help='[Trainer] backend for DDP training, "mpi", "gloo" or "nccl"',
        )
        parser.add_argument(
            '--master_addr',
            default='localhost',
            type=str,
            help='[Trainer] master hostname for communication',
        )
        parser.add_argument(
            '--master_port',
            default='29500',
            type=str,
            help='[Trainer] master port for communication',
        )
        parser.add_argument(
            '--world_size',
            default=1,
            type=int,
            help='[Trainer] number of processes participating in the job',
        )
        parser.add_argument(
            '--rank',
            default=0,
            type=int,
            help='[Trainer] rank of the current process',
        )
        parser.add_argument(
            '--local_rank',
            default=0,
            type=int,
            help='[Trainer] local rank of the current process',
        )
        parser.add_argument(
            '--datamodule',
            default=None, #required=True,
            help='[Trainer] datamodule used for traning',
        )
        parser.add_argument(
            '--model',
            default=None, #required=True,
            help='[Trainer] model to train',
        )
        parser.add_argument(
            '--max_epochs',
            default=5,
            type=int,
            help='[Trainer] max epochs for training',
        )
        parser.add_argument(
            '--verbose',
            default=False,
            action='store_true',
            help='[Trainer] set to True to trigger progressbar and writer'
        )
        return parser
