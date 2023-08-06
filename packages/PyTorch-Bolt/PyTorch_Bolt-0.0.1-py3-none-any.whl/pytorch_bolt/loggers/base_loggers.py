#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import argparse
import pathlib


class BaseLoggers(abc.ABC):

    def __init__(self, args):
        self.logs_dir = pathlib.Path(args.logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    @abc.abstractmethod
    def configure_root_logger(self):
        raise NotImplementedError

    @abc.abstractmethod
    def configure_child_logger(self):
        return

    @abc.abstractmethod
    def configure_tracker(self):
        raise NotImplementedError

    @abc.abstractmethod
    def configure_progressbar(self):
        raise NotImplementedError

    @abc.abstractmethod
    def configure_writer(self):
        raise NotImplementedError

    @staticmethod
    def add_argparse_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument(
            '--logs_dir',
            default='logs',
            type=str,
            help='[Loggers] logs directory',
        )
        return parser
