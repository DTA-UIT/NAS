from ZeroCostNas.foresight.dataset import get_cifar_dataloaders
import argparse

dataset = 'cifar10'
train_loader, test_loader = get_cifar_dataloaders(64, 64, dataset, 2)
dataset_args = 'imagenet' if dataset == 'ImageNet16-120' else dataset

args = argparse.Namespace(api_loc='', 
                          outdir='',
                          init_w_type='none', # Initialize weight
                          init_b_type='none', # Initialize bias
                          batch_size=64,      # Batch size
                          dataset=dataset_args,
                          gpu=0,
                          num_data_workers=2,
                          dataload='random',
                          dataload_info=1,
                          seed=1,
                          write_freq=1,
                          start=0,
                          end=0,
                          noacc=False
                          )

"""
NATS-Bench
"""
from numpy import genfromtxt
from NASBench import NATS

api = NATS.NATS(use_colab=False)
api.evaluate_arch(args=args, ind=[2, 3, 1, 0, 4, 2], dataset=dataset, measure='synflow', train_loader=train_loader)


"""
NAS-Bench-101
"""

# from NASBench import NAS101
# from ZeroCostNas.foresight.dataset import get_cifar_dataloaders
# import numpy as np
# import argparse

# api = NAS101.NAS101(use_colab=False)
# print(api.evaluate_arch(args, ind=[2, 3, 0, 2, 2, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
#         0, 1, 1, 0], measure='macs', train_loader=train_loader))