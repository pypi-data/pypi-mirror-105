#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import time
from typing import List

from torch.utils.tensorboard import SummaryWriter

from .base_loggers import BaseLoggers


class Tracker():

    def __init__(self, keys, reduction):
        if reduction not in ('sum', 'mean'):
            raise ValueError
        self.trkdict = {key: {} for key in keys}
        self.reset()
        self.reduction = reduction

    def __str__(self):
        entries = []
        for key in self.trkdict:
            trkfmt = self._get_trkfmt(key)
            entries.append(
                trkfmt.format(
                    key,
                    self.trkdict[key]['val'],
                    self.trkdict[key]['mean']
                )
            )
        return ' | '.join(entries)

    def _get_trkfmt(self, key):
        strfmt = self.trkdict[key]['strfmt']
        return '{}: {' + strfmt + '} ({' + strfmt + '})'

    def reset(self):
        for key in self.trkdict:
            self.trkdict[key]['val'] = 0.0
            self.trkdict[key]['sum'] = 0.0
            self.trkdict[key]['size'] = 0
            self.trkdict[key]['mean'] = 0.0
            self.trkdict[key]['strfmt'] = ''

    def update(self, key, value, size=1, strfmt=':.4f'):
        if self.reduction == 'sum':
            self.trkdict[key]['val'] = value / size
            self.trkdict[key]['sum'] += value
        elif self.reduction == 'mean':
            self.trkdict[key]['val'] = value
            self.trkdict[key]['sum'] += value * size
        self.trkdict[key]['size'] += size
        self.trkdict[key]['mean'] = self.trkdict[key]['sum'] / self.trkdict[key]['size']
        self.set_strfmt(key, strfmt)

    def set_strfmt(self, key, strfmt):
        self.trkdict[key]['strfmt'] = strfmt #':7.4f'

    def val(self, key):
        return self.trkdict[key]['val']

    def avg(self, key):
        return self.trkdict[key]['mean']


class ProgressBar():

    def __init__(self):
        self.prefix = ''
        self.size = 0
        self.step = 0

    def reset(self, prefix, size, step=None):
        self.prefix = prefix
        self.size = size
        if step is None:
            step = self.size // 10 if self.size > 15 else 1
        self.step = step

    def show(self, idx, logger, tracker):
        barfmt = self._get_barfmt()
        if (idx + 1) % self.step == 0 or (idx + 1) == self.size:
            entries = [self.prefix + barfmt.format(idx)]
            entries += [str(tracker)]
            logger.info(' | '.join(entries))

    def _get_barfmt(self):
        num_digits = len(str(self.size))
        strfmt = ':' + str(num_digits) + 'd'
        return '[{' + strfmt + '}/' + str(self.size) + ']'


class Loggers(BaseLoggers):

    def __init__(self, args):
        super().__init__(args)
        # configure logger
        self.root = ''
        self.loggerfmt = args.loggerfmt
        self.datefmt = args.datefmt
        # configure tracker
        self.tracker_keys = args.tracker_keys
        self.tracker_reduction = args.tracker_reduction

    def configure_root_logger(self, root):
        self.root = root
        logger = logging.getLogger(self.root)
        logger.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers later
        formatter = logging.Formatter(fmt=self.loggerfmt, datefmt=self.datefmt)
        # create file handler which logs even debug messages
        file_handler = logging.FileHandler(self._get_logfile())
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        # create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger

    def _get_logfile(self):
        timestamp = time.strftime('%y%m%d_%H%M%S', time.localtime())
        return self.logs_dir.joinpath('logger-' + timestamp + '.log')

    def configure_child_logger(self, child):
        return logging.getLogger(self.root + '.' + child)

    def configure_tracker(self):
        return Tracker(self.tracker_keys, self.tracker_reduction)

    def configure_progressbar(self):
        return ProgressBar()

    def configure_writer(self):
        return SummaryWriter(log_dir=self.logs_dir)

    @staticmethod
    def add_argparse_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        parser = BaseLoggers.add_argparse_args(parser)
        parser.add_argument(
            '--loggerfmt',
            default='%(asctime)s | %(levelname)-5s | %(name)s - %(message)s',
            type=str,
            help='[Loggers] logger format',
        )
        parser.add_argument(
            '--datefmt',
            default=None,
            type=str,
            help='[Loggers] date format',
        )
        parser.add_argument(
            '--tracker_keys',
            default=None, #required=True,
            type=List[str],
            help='[Loggers] keys to the values to be tracked',
        )
        parser.add_argument(
            '--tracker_reduction',
            default='mean',
            type=str,
            help='[Loggers] reduction to apply to the values to be tracked, "mean" or "sum"',
        )
        return parser

    @classmethod
    def from_argparse_args(cls, args):
        return cls(args)
