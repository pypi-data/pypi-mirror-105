#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import time

import torch

from .base_trainer import BaseTrainer


class Trainer(BaseTrainer):

    def __init__(self, args):
        super().__init__(args)

    def _setup_env(self):
        if self.distributed:
            # TCP initialization environment variables:
            # MASTER_ADDR, MASTER_PORT, WORLD_SIZE, RANK
            # <https://pytorch.org/docs/stable/distributed.html#environment-variable-initialization>
            os.environ['MASTER_ADDR'] = str(self.master_addr)
            os.environ['MASTER_PORT'] = str(self.master_port)
            # Slurm overwrite
            if self.use_slurm:
                os.environ['MASTER_ADDR'] = os.environ['SLURM_SUBMIT_HOST']
                os.environ['WORLD_SIZE'] = os.environ['SLURM_NTASKS']
                os.environ['RANK'] = os.environ['SLURM_PROCID']
                os.environ['LOCAL_RANK'] = os.environ['SLURM_LOCALID']
            # world_size = nproc_per_node * nnodes, nproc_per_node = GPUS_PER_NODE
            self.world_size = int(os.environ['WORLD_SIZE'])
            # rank = nproc_per_node * node_rank + local_rank
            self.rank = int(os.environ['RANK'])
            # <https://pytorch.org/docs/stable/distributed.html#launch-utility>
            self.local_rank = int(os.environ['LOCAL_RANK'])
        self.logger.debug(
            'WORLD_SIZE: {}, RANK: {}, LOCAL_RANK: {}'.format(
                self.world_size, self.rank, self.local_rank
            )
        )

    @staticmethod
    def get_rank():
        # single-node single-GPU training
        rank = 0
        # multi-node multi-GPU traning using torch.distributed.launch
        if 'RANK' in os.environ:
            rank = int(os.environ['RANK'])
        # multi-node multi-GPU training with Slurm
        elif 'SLURM_PROCID' in os.environ:
            rank = int(os.environ['SLURM_PROCID'])
        return rank

    def _setup_device(self):
        gpus_per_node = torch.cuda.device_count()
        if self.rank == 0:
            self.logger.debug('running on {}-GPU node'.format(gpus_per_node))
        if self.device is None:
            # single-node single-GPU training
            self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
            # multi-node multi-GPU training
            if self.distributed:
                self.device = torch.device(type='cuda', index=self.local_rank)
        self.logger.debug('running on {} device'.format(self.device))

    def _init_proc(self):
        if self.distributed:
            torch.distributed.init_process_group(backend=self.dist_backend)

    def _destroy_proc(self):
        if self.distributed:
            torch.distributed.destroy_process_group()

    def _model_to_device(self):
        self.model = self.model.to(self.device)
        if self.distributed:
            # currently `SyncBatchNorm` only supports `DistributedDataParallel` (DDP)
            # with single GPU per process
            # <https://pytorch.org/docs/stable/generated/torch.nn.SyncBatchNorm.html>
            self.model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.model)
            self.model = torch.nn.parallel.DistributedDataParallel(
                self.model,
                device_ids=[self.local_rank],
                output_device=self.local_rank
            )

    def _criterion_to_device(self):
        self.criterion = self.criterion.to(self.device)

    def _metric_to_device(self):
        self.metric = self.metric.to(self.device)

    def _get_prefix(self, epoch, max_epochs, tag):
        return (tag + ': [{:' + str(len(str(max_epochs))) + 'd}/{} ({:3.0f}%)] ').format(
            epoch, max_epochs, (100.0 * epoch / max_epochs)
        )

    def _training_epoch(self, epoch, tag='TRAIN'):
        # training_epoch_start
        if self.distributed:
            self.train_dataloader.sampler.set_epoch(epoch)
        self.tracker.reset()
        if self.progressbar is not None:
            self.progressbar.reset(
                self._get_prefix(epoch, self.max_epochs, tag),
                len(self.train_dataloader)
            )
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
            # tracker
            self.tracker.update('loss', step_outs['loss'].item(), size=batch[0].size(0))
            self.tracker.update('score', step_outs['score'].item(), size=batch[0].size(0))
            # furthermore
            step_outs = self._training_step_end(batch_idx, batch, step_outs)
            # progressbar
            if self.verbose:
                self.progressbar.show(batch_idx, self.logger, self.tracker)
        # training_epoch_end
        self.logger.info(
            self._get_prefix(epoch, self.max_epochs, tag) + '| loss: {} | score: {}'.format(
                self.tracker.avg('loss'), self.tracker.avg('score')
            )
        )
        # writer
        if self.verbose:
            self.writer.add_scalar('loss/' + tag, self.tracker.avg('loss'), epoch)
            self.writer.add_scalar('score/' + tag, self.tracker.avg('score'), epoch)
        return self._training_epoch_end()

    def _training_step(self, batch_idx, batch):
        return self._shared_step(batch_idx, batch)

    def _training_step_end(self, batch_idx, batch, step_outs):
        return

    def _training_epoch_end(self):
        # if return
        # return dict, containing at least 2 keys: "loss", "score"
        return

    def _validation_epoch(self, epoch, dataloader, max_epochs, tag='VAL'):
        # validation_epoch_start
        if self.distributed:
            dataloader.sampler.set_epoch(epoch)
        self.tracker.reset()
        if self.progressbar is not None:
            self.progressbar.reset(self._get_prefix(epoch, max_epochs, tag), len(dataloader))
        self.model.eval()
        with torch.no_grad():
            for batch_idx, batch in enumerate(dataloader):
                # validation_step (required)
                # dict, containing at least 2 keys: "loss", "score"
                step_outs = self._validation_step(batch_idx, batch)
                # validation_step_end
                # tracker
                self.tracker.update('loss', step_outs['loss'].item(), size=batch[0].size(0))
                self.tracker.update('score', step_outs['score'].item(), size=batch[0].size(0))
                # furthermore
                step_outs = self._validation_step_end(batch_idx, batch, step_outs)
                # progressbar
                if self.verbose:
                    self.progressbar.show(batch_idx, self.logger, self.tracker)
        # validation_epoch_end
        self.logger.info(
            self._get_prefix(epoch, max_epochs, tag) + '| loss: {} | score: {}'.format(
                self.tracker.avg('loss'), self.tracker.avg('score')
            )
        )
        # writer
        if self.verbose:
            self.writer.add_scalar('loss/' + tag, self.tracker.avg('loss'), epoch)
            self.writer.add_scalar('score/' + tag, self.tracker.avg('score'), epoch)
        return self._validation_epoch_end()

    def _validation_step(self, batch_idx, batch):
        return self._shared_step(batch_idx, batch)

    def _validation_step_end(self, batch_idx, batch, step_outs):
        return

    def _validation_epoch_end(self):
        # if return
        # return dict, containing at least 2 keys: "loss", "score"
        return

    def _shared_step(self, batch_idx, batch):
        # forward propagation
        inputs, targets = batch
        inputs, targets = inputs.to(self.device), targets.to(self.device)
        outputs = self.model(inputs)
        loss = self.criterion(outputs, targets)
        score = self.metric(outputs, targets)
        return {'loss': loss, 'score': score}

    # TODO
    def _test_epoch(self, epoch, dataloader, max_epochs, tag='TEST'):
        return self._validation_epoch(epoch, dataloader, max_epochs, tag=tag)

    def fit(self):
        #best_score = 0.0
        if self.rank == 0:
            self.logger.info('TRAINING started')
        since = time.time()
        for epoch in range(1, self.max_epochs + 1):
            # one training epoch
            train_epoch_outs = self._training_epoch(epoch)
            # one vlaidation epoch
            val_epoch_outs = self._validation_epoch(epoch, self.val_dataloader, self.max_epochs)
            # lr_scheduler
            if self.lr_scheduler is not None:
                self.lr_scheduler.step()
            # TODO: checkpoint handler
            #best_score = max(best_score, val_epoch_outs['score'])

        time_elapsed = time.time() - since
        if self.rank == 0:
            self.logger.info(
                'TRAINING finished in {:.0f} min {:.0f} sec'.format(
                    time_elapsed // 60, time_elapsed % 60
                )
            )

    def validate(self):
        if self.rank == 0:
            self.logger.info('VALIDATION started')
        epoch, max_epochs = 1, 1
        since = time.time()
        epoch_outs = self._validation_epoch(epoch, self.val_dataloader, max_epochs)
        time_elapsed = time.time() - since
        if self.rank == 0:
            self.logger.info(
                'VALIDATION finished in {:.0f} min {:.0f} sec'.format(
                    time_elapsed // 60, time_elapsed % 60
                )
            )

    def test(self):
        if self.rank == 0:
            self.logger.info('TEST started')
        epoch, max_epochs = 1, 1
        since = time.time()
        epoch_outs = self._test_epoch(epoch, self.test_dataloader, max_epochs)
        time_elapsed = time.time() - since
        if self.rank == 0:
            self.logger.info(
                'TEST finished in {:.0f} min {:.0f} sec'.format(
                    time_elapsed // 60, time_elapsed % 60
                )
            )

    def destory(self):
        self.writer.close()
        self._destroy_proc()

    @staticmethod
    def add_argparse_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        parser = BaseTrainer.add_argparse_args(parser)
        return parser

    @classmethod
    def from_argparse_args(cls, args):
        return cls(args)
