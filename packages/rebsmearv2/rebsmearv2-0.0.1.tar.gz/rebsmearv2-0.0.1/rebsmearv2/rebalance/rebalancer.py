#!/usr/bin/env python

class RebalanceExecutor():
    '''
    Object to execute the rebalancing step.

    INPUT: Takes the set of files to be processed.
    OUTPUT: Produces ROOT files with rebalanced event information saved.
    '''
    def __init__(self, files, dataset, treename):
        self.files = files
        self.dataset = dataset
        self.treename = treename