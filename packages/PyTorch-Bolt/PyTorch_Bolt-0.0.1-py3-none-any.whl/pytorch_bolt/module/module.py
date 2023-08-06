#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

import torch


class Module(torch.nn.Module):

    def __init__(self):
        super().__init__()
        # setup model

        #self.model = self._setup_model()
        # configure criterion and metric

        # configure optimizer and lr_scheduler

    @abc.abstractmethod
    def _setup_model(self):
        raise NotImplementedError

    #def forward(self, inputs):
    #    return self.model(inputs)

    # return parameters that have requires_grad=True
    # `parameters_to_update` can be useful for transfer learning
    @abc.abstractmethod
    def parameters_to_update(self):
        raise NotImplementedError

    # return criterion
    @abc.abstractmethod
    def configure_criterion(self):
        raise NotImplementedError

    # return metric
    @abc.abstractmethod
    def configure_metric(self):
        raise NotImplementedError

    # return optimizer (and lr_scheduler)
    @abc.abstractmethod
    def configure_optimizer(self):
        raise NotImplementedError
