# -*- coding: utf-8 -*-
__author__ = 'Taikor'
from py_utility import system
import time
import pickle

folder_path = r"C:\workspace\Taikor_NLP_service\HotSpotClustering\DerivativeClustering\test_derivative"


class DerivativeClustering():
    def __init__(self, _folder_path):
        self.clusters = list()
        self.texts = list()
        self.excludes = list()
        self.files = system.listdir_enchanced(_folder_path)
        for file in self.files:
            self.texts.append(system.get_content(file))

    def get_clause(self, text):
        all_clauses = list()
        sentences = text.split(r"。")
        for sentence in sentences:
            clauses = sentence.split(r"，")
            for clause in clauses:
                x = clause.split(r",")
                for y in x:
                    z = y.split(r".")
                    for item in z:
                        all_clauses.append(item)
        return all_clauses

    def derivative_index(self, text_x, text_y):
        clauses_x = self.get_clause(text_x)
        clauses_y = self.get_clause(text_y)
        clauses_intersection = set(clauses_x) & set(clauses_y)
        print("x section number: "+str(len(set(clauses_x))))
        print("y section number: "+str(len(set(clauses_y))))
        print("intersection section number: "+str(len(clauses_intersection)))
        x_index = len(clauses_intersection)/len(clauses_x)
        y_index = len(clauses_intersection)/len(clauses_y)
        _derivative_index = (x_index + y_index)/2
        return _derivative_index, clauses_intersection

    def find_derivative(self, current_index):
        texts = self.texts
        cluster = [self.files[current_index]]
        if current_index not in self.excludes:
            for i in range(current_index, (len(texts)-1)):
                if i not in self.excludes:
                    index, intersection = self.derivative_index(texts[current_index], texts[i+1])
                    print(index)
                    print(intersection)
                    if index > 0.3:
                        cluster.append(self.files[i+1])
                        self.excludes.append(i+1)
        return cluster

    def clustering(self):
        for i in range(len(self.files)-1):
            self.clusters.append(self.find_derivative(i))
            print("Ieration: " + str(i))
        return self.clusters

timer = system.running_timer()
d = DerivativeClustering(folder_path)
clusters = d.clustering()

time_consumed = timer.end()

print(clusters)

print(time_consumed)





