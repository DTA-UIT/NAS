import os, sys
import copy
import numpy as np
import matplotlib.pyplot as plt
import random
from NASBench.NASBench import NASBench
from source.nasbench.nasbench import api

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class NAS101(NASBench):
    __model_path = None
    def __init__(self):
        super().__init__()
        
        """ 
        Constants for NASBench101
        """
        INPUT = 'input'
        OUTPUT = 'output'
        CONV3X3 = 'conv3x3-bn-relu'
        CONV1X1 = 'conv1x1-bn-relu'
        MAXPOOL3X3 = 'maxpool3x3'
        NUM_VERTICES = 7
        MAX_EDGES = 9
        EDGE_SPOTS = NUM_VERTICES * (NUM_VERTICES - 1) / 2   # Upper triangular matrix
        OP_SPOTS = NUM_VERTICES - 2   # Input/output vertices are fixed
        ALLOWED_OPS = [CONV3X3, CONV1X1, MAXPOOL3X3]
        ALLOWED_EDGES = [0, 1]   # Binary adjacency matrix
        
        url = os.path.dirname(__file__)
        self.op_names = [INPUT, CONV1X1, CONV3X3, CONV3X3, CONV3X3, MAXPOOL3X3, OUTPUT] 
        self.api = api.NASBench(f"{url[:-len('/NASBench')] + '/source/nasbench/nasbench_full.tfrecord'}")
        
    
    def query_bench(self, ind, metric=None):
        """
        Arguments:
        metric (optional) --  metric to query ('module_adjacency', 
                                               'module_operations', 
                                               'trainable_parameters', 
                                               'training_time', 
                                               'train_accuracy', 
                                               'validation_accuracy', 
                                               'test_accuracy')
        """  
        self.cell = api.ModelSpec(ind, self.op_names)

        try:
            self.query_result = self.api.query(self.cell) 
        except:
            print(f"Cell {self.cell.__dict__['original_matrix']} is invalid for NASBench101")    
            self.api._check_spec(self.cell)

        # if not self.api.is_valid(self.cell):
        #     print(self.api._check_spec(self.cell))
        #     raise Exception("Invalid NASBench101 cell") 
        return self.query_result if metric == None else self.query_result[metric] 
    
    def repair_connection(self, ind):
        INPUT = 'input'
        OUTPUT = 'output'
        CONV1X1 = 'conv1x1-bn-relu'
        CONV3X3 = 'conv3x3-bn-relu'
        MAXPOOL3X3 = 'maxpool3x3'
        NUM_VERTICES = 7
        MAX_EDGES = 9
        EDGE_SPOTS = NUM_VERTICES * (NUM_VERTICES - 1) / 2   # Upper triangular matrix
        OP_SPOTS = NUM_VERTICES - 2   # Input/output vertices are fixed
        ALLOWED_OPS = [CONV3X3, CONV1X1, MAXPOOL3X3]
        ALLOWED_EDGES = [0, 1]   # Binary adjacency matrix

        ops_none = []
        ops = [INPUT]
        for i in range(0, 5):
            if ind[i] == 0:
                ops_none.append(i)
            elif ind[i] == 1:
                ops.append(CONV1X1)
            elif ind[i] == 2:
                ops.append(CONV3X3)
            else:
                ops.append(MAXPOOL3X3)
        ops.append(OUTPUT)
        
        print(ind)
        print(ops)
        # return 