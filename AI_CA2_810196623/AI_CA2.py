#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 19:46:02 2020

@author: mac
"""

import pandas as pd
import random
import time
POPULATION_SIZE = 50
ELIMINATION_RATE = 20

class Circuit:
    def __init__(self,gates,inputs):
        self.inputs = inputs
        self.gates = gates
        self.dispatcher = {"AND":self.AND,"OR":self.OR,"XOR":self.XOR,"NAND":self.NAND,"NOR":self.NOR,"XNOR":self.XNOR}
    
    def AND(self,a,b):
        if a and b:
            return True
        else:
            return False
        
    def OR(self,a,b):
        if a or b:
            return True
        else:
            return False
        
    def XOR(self,a,b):
        if a == b:
            return False
        else:
            return True
        
    def NAND(self,a,b):
        if a and b:
            return False
        else:
            return True
        
    def NOR(self,a,b):
        if a or b:
            return False
        else:
            return True
        
    def XNOR(self,a,b):
        if a == b:
            return True
        else:
            return False
        
    def calculate_output(self):
        out = self.dispatcher[self.gates[0]](self.inputs[0],self.inputs[1])
        for i in range(1,len(self.gates)):
            out = self.dispatcher[self.gates[i]] (out,self.inputs[i+1])
        return out

class Solver:
    def __init__(self,data,gens_num):
        self.data = data
        self.gens = ['AND','OR','XOR','NAND','NOR','XNOR']
        self.gens_num = gens_num
        
    def generate_chromosome(self):
        chromosome = []
        for i in range(0,self.gens_num):
            chromosome.append(random.choice(self.gens))
        return chromosome
    
    def fitness(self,chromosome):
        count = 0
        for row in self.data:
            gens_out = Circuit(chromosome,row[:-1]).calculate_output()
            exp_out = row[-1]
            if(gens_out != exp_out):
                count+=1
        return count
    
    def sort_population_based_on_fitness(self,population):
        fitnesses = []
        for p in population:
            fitnesses.append(self.fitness(p))
        zipped_pairs = zip(fitnesses,population)
        sorted_population = [p for f,p in sorted(zipped_pairs)]
        return sorted_population
    
    def mutate(self,chromosome,p):
        mutate = []
        for i,gen in enumerate(chromosome):
            prob = random.random()
            if prob<p:
                mutate.append(random.choice(self.gens))
            else:
                mutate.append(chromosome[i])
        return mutate
                
    def cross_over(self,chromosome1,chromosome2):
        child1 = []
        child2 = []
        points = random.sample(range(1,self.gens_num-1),2)
        points.sort()
        for i in range(0,self.gens_num):
            if(points[0]>i):
                child1.append(chromosome1[i])
                child2.append(chromosome2[i])
            elif(points[1]<i):
                child1.append(chromosome1[i])
                child2.append(chromosome2[i])
            else:
                child1.append(chromosome2[i])
                child2.append(chromosome1[i])
        return child1,child2
        

    def genetic_algorithm(self):
        population = [self.generate_chromosome() for i in range(0,POPULATION_SIZE)]
        rank_sum = POPULATION_SIZE*(POPULATION_SIZE+1)/2
        probability = []
        for i in range(POPULATION_SIZE,0,-1):
            probability.append(i/rank_sum)
        count = 0
        prev_best = len(data)//2
        population = [self.generate_chromosome() for i in range(0,POPULATION_SIZE)]
        rank_sum = POPULATION_SIZE*(POPULATION_SIZE+1)/2
        probability = []
        for i in range(POPULATION_SIZE,0,-1):
            probability.append(i/rank_sum)
        count = 0
        prev_best = len(data)//2
        while True:
            population = self.sort_population_based_on_fitness(population)
            curr_best = self.fitness(population[0])
            
            if(curr_best == prev_best):
                count += 1
            else:
                count = 0
                
            p = curr_best/len(data)
            if(count>=30):
                if((count//20)%2 == 1 and p+0.3<=1):
                    p += 0.3

            if(self.fitness(population[0])==0):
                return population[0]
            
            new_population = []
            """
            selection = random.choices(population, weights=probability,k=POPULATION_SIZE)
            for i in range(POPULATION_SIZE//2):
                parents = random.sample(selection,2)
                prob = random.random()
                if(prob<=0.2):
                    new_population.append(parents[0])
                    new_population.append(parents[1])
                else:
                    child1,child2 = self.cross_over(parents[0],parents[1])
                    new_population.append(self.mutate(child1,p))
                    new_population.append(self.mutate(child2,p))
            """
            size = int((ELIMINATION_RATE*POPULATION_SIZE)/100) 
            new_population.extend(population[:size]) 
            size = int(((100-ELIMINATION_RATE)*POPULATION_SIZE)/100) 
            for i in range(size//2):
                parents = random.choices(population, weights=probability,k=2)
                child1,child2 = self.cross_over(parents[0],parents[1])
                new_population.append(self.mutate(child1,p))
                new_population.append(self.mutate(child2,p))
            population = new_population
            prev_best = curr_best 
        

data = pd.read_csv('truth_table.csv')
file = open('truth_table.csv', "r")
row_num = 0
data = []
for row in file:
    if(row_num!= 0):
        row = row.replace('\n','').split(',')
        row = [ True if x == "TRUE" else False for x in row]
        data.append(row)
    row_num+=1
    
start = time.time()   
solver = Solver(data,9)
print(solver.genetic_algorithm())
print("Time: %s seconds" % (time.time() - start))
    