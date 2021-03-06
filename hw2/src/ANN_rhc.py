"""
Backprop NN training on titanic data
"""
import os
import csv
import time
import sys
sys.path.append('./ABAGAIL/ABAGAIL.jar')
from modules.ann import train, initialize_instances, errorOnDataSet
from func.nn.backprop import BackPropagationNetworkFactory
from shared import SumOfSquaresError, DataSet
from opt.example import NeuralNetworkOptimizationProblem
from func.nn.backprop import RPROPUpdateRule, BatchBackPropagationTrainer
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
from func.nn.activation import LogisticSigmoid

# Network parameters found "optimal" in Assignment 1
INPUT_LAYER = 48
HIDDEN_LAYER1 = 5
HIDDEN_LAYER2 = 5
HIDDEN_LAYER3 = 5
OUTPUT_LAYER = 1
TRAINING_ITERATIONS = 20000
OUTFILE = './../logs/RHC_LOG.csv'

def main():
    """Run this experiment"""
    training_ints = initialize_instances('./../data/bank_train.csv')
    testing_ints = initialize_instances('./../data/bank_test.csv')
    factory = BackPropagationNetworkFactory()
    measure = SumOfSquaresError()
    data_set = DataSet(training_ints)
    acti = LogisticSigmoid()
    rule = RPROPUpdateRule()
    classification_network = factory.createClassificationNetwork([INPUT_LAYER, HIDDEN_LAYER1, OUTPUT_LAYER],acti)
    nnop = NeuralNetworkOptimizationProblem(data_set, classification_network, measure)
    oa = RandomizedHillClimbing(nnop)
    train(oa, classification_network, 'RHC', training_ints, testing_ints, measure, TRAINING_ITERATIONS, OUTFILE)



if __name__ == "__main__":
    with open(OUTFILE,'w') as f:
        f.write('{},{},{},{},{},{}\n'.format('iteration','MSE_trg','MSE_tst','acc_trg','acc_tst','f1_trg', 'f1_tst', 'elapsed'))
    main()
