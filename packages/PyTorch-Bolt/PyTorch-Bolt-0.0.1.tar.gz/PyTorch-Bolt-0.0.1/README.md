# PyTorch Bolt

PyTorch Bolt is

* a simple PyTorch wrapper making multi-node multi-GPU training much easier on Slurm



PyTorch Bolt supports to

* use single-node single-GPU training on a specified GPU device

* use multi-node (or single-node) multi-GPU [`DistributedDataParallel`](https://pytorch.org/docs/master/generated/torch.nn.parallel.DistributedDataParallel.html) (DDP) training
  - with [`torch.distributed.launch`](https://pytorch.org/docs/stable/distributed.html#launch-utility) module
  - with [Slurm](https://slurm.schedmd.com/quickstart.html) cluster workload manager



## Quickstart



### Dependencies and Installation

#### Package Dependencies

`pip` will handle all package dependencies.



#### Install Pytorch Bolt

```bash
$ pip install pytorch_bolt
```



## Documentation

### Module `DataModule`

```python
class pytorch_bolt.DataModule(data_dir='data', num_splits=10, batch_size=1, num_workers=0, pin_memory=False, drop_last=False)
```

#### `use_dist_sampler()`

Can be called to trigger `DistributedSampler` when using `DistributedDataParallel` (DDP).

#### `train_dataloader()`

Returns `Dataloader` for trainset.

#### `val_dataloader()`

Returns  `Dataloader` for valset.

#### `test_dataloader()`

Returns  `Dataloader` for testset.

#### `add_argparse_args(parent_parser)`

Returns `argparse` parser. (**Staticmethod**)



**Practical template**:

```python
import pytorch_bolt

class MNISTDataModule(pytorch_bolt.DataModule):

    def __init__(self, args):
        super().__init__(args)
        # arguments for customized dataset
    
    # optional helper function can be used
    def _prepare_data(self):
        pass  

    def _setup_dataset(self):
        # trainset and valset for fit stage
        # `self.num_splits` can be used for splitting trainset and valset 
        # testset for test stage
        return trainset, valset, testset

    @staticmethod
    def add_argparse_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        parser = DataModule.add_argparse_args(parser)
        # TODO
        return parser

    @classmethod
    def from_argparse_args(cls, args):
        return cls(args)
```



### Module `Module`

```python
class pytorch_bolt.Module()
```

#### `parameters_to_update()`

Returns model parameters that have `requires_grad=True`.

#### `configure_criterion()`

Returns criterion.

#### `configure_metric()`

Returns metric.

#### `configure_optimizer()`

Returns optimizer (and learning rate scheduler).



**Practical template**:

```python
import pytorch_bolt

class Model(pytorch_bolt.Module):

    def __init__(self, args):
        super().__init__()
        # hyperparameters for model
        self.model = self._setup_model()
        # hyperparameters for criterion, metric, optimizer and lr_scheduler

    def _setup_model(self):
        # TODO
        return model

    def forward(self, inputs):
        return self.model(inputs)

    # return parameters that have requires_grad=True
    # `parameters_to_update` can be useful for transfer learning
    def parameters_to_update(self):
        return
    
    # return criterion
    def configure_criterion(self):
        return
    
    # return metric
    def configure_metric(self):
        return

    # return optimizer (and lr_scheduler)
    def configure_optimizer(self):
        return
      
    @staticmethod
    def add_argparse_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        # TODO     
        return parser

    @classmethod
    def from_argparse_args(cls, args):
        return cls(args)
```



### Module `Loggers`

```python
class pytorch_bolt.Loggers(logs_dir='logs', loggerfmt='%(asctime)s | %(levelname)-5s | %(name)s - %(message)s', datefmt=None, tracker_keys=None (Required), tracker_reduction='mean')
```

#### `configure_root_logger(root)`

Returns `root` logger.

#### `configure_child_logger(child)`

Returns `root.child` logger.

#### `configure_tracker()`

Returns tracker for tracking forward propagation step outputs and statistics.

#### `configure_progressbar()`

Returns progress bar for showing forward propagation step progress and details. 

#### `configure_writer()`

Returns Tensorboard writer for visualizing forward propagation epoch outputs.

#### `add_argparse_args(parent_parser)`

Returns `argparse` parser. (**Staticmethod**)

#### `from_argparse_args(args)`

`Loggers` constructor.



### Module `Trainer`

```python
class pytorch_bolt.Trainer(loggers=None (Required), device=None, distributed=False, use_slurm=False, dist_backend='nccl', master_addr='localhost', master_port='29500', world_size=1, rank=0, local_rank=0, datamodule=None (Required), model=None (Required), max_epochs=5, verbose=False)
```

#### `get_rank()`

Gets rank of current process. (**Staticmethod**)

#### `fit()`

Fits the model on trainset, validating each epoch on valset.

#### `validate()`

Validates trained model by running one epoch on valset.

#### `test()`

Tests trained model by running one epoch on testset.

#### `destroy()`

Destroys trainer..

#### `add_argparse_args(parent_parser)`

Returns `argparse` parser. (**Staticmethod**)

#### `from_argparse_args(args)`

`Trainer` constructor.



**Practical template for customized trainer**: 

```python
import pytorch_bolt

class MyTrainer(pytorch_bolt.Trainer):
    
    def _training_step(self, batch_idx, batch):
        return

    def _training_step_end(self, batch_idx, batch, step_outs):
        return
    
    # if return
    # return dict, containing at least 2 keys: "loss", "score"
    def _training_epoch_end(self):        
        return
```



## Related Projects

* Inspired by [Pytorch Lightning](https://www.pytorchlightning.ai/)



## Appendix

### Environment Variable Mapping

**WORLD_SIZE** | **SLURM_NTASKS** (and **SLURM_NPROCS** for backwards compatibility)

> Same as **-n, --ntasks**

**RANK** | **SLURM_PROCID**

> The MPI rank (or relative process ID) of the current process

**LOCAL_RANK** | **SLURM_LOCALID**

> Node local task ID for the process within a job.

**MASTER_ADDR** | **SLURM_SUBMIT_HOST**

> The hostname of the machine from which **sbatch** was invoked.

**NPROC_PER_NODE** | **SLURM_NTASKS_PER_NODE**

> Number of tasks requested per node. Only set if the **--ntasks-per-node** option is specified.

**NNODES** | **SLURM_JOB_NUM_NODES** (and **SLURM_NNODES** for backwards compatibility)

> Total number of nodes in the job's resource allocation.

**NODE_RANK** | **SLURM_NODEID**

> ID of the nodes allocated.

**SLURM_JOB_NODELIST** (and **SLURM_NODELIST** for backwards compatibility)

> List of nodes allocated to the job.



### Reference

* [Sbatch Output Environment Variables](https://slurm.schedmd.com/sbatch.html#lbAK)

* [`torch.distributed` TCP Initialization Environment Variables](https://pytorch.org/docs/stable/distributed.html#environment-variable-initialization)

