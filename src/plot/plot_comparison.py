#!/usr/bin/env python3
#
# plot_comparison.py
#
# BSD 2-Clause License
#
# Copyright (c) 2018, Franco Masotti
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.ticker as tk
import numpy as np
import csv
import sys

# See the CSV file structure on the readme file.
TIME_FIELD_START_INDEX = 2
PROB_FIELD_START_INDEX = 3

class Utils():
    def __init__(self, filename: str, delimiter: str = ','):
        # Do not reload the file more than once.
        try:
            self.data is None
        except AttributeError:
            self.data = dict()

            with open(filename, 'r') as f:
                data = csv.reader(f, delimiter=delimiter)
                # Sort lines by run number and and keep sample id in place so
                # that we maintain the correct input for the other functions.
                data = sorted(data, key=lambda d: d[0])
                for row in data:
                    self.number_of_rows = len(row)
                    for i in range(0,len(row),2):
                        if i not in self.data and i+1 not in self.data:
                            self.data[i] = list()
                            self.data[i+1] = list()
                        self.data[i].append(int(round(float(row[i]))))
                        self.data[i+1].append(float(row[i+1]))

            # Assume data dict is sorted by run number.
            # Get the last index of the smallest number. This corresponds to the first run.
            self.last_index_of_first_run = len(self.data[0]) - 1 - self.data[0][::-1].index(min(self.data[0]))


        print(self.data)

    def compute_avg(self):
        pass

    def load_time_over_sample_in_arrays(self):
        # We need to extract only the relevant data without altering
        # the main data structure.
        self.time_over_sample['x'] = self.data[1]
        self.time_over_sample['y'] = list()
        for i in range(TIME_FIELD_START_INDEX,self.number_of_rows,2):
            self.time_over_sample['y'].append(self.data[i])
        print(self.time_over_sample)

    def load_prob_over_sample_in_arrays(self):
        self.prob_over_sample['x'] = self.data[1]
        self.prob_over_sample['y'] = list()
        for i in range(PROB_FIELD_START_INDEX,self.number_of_rows,2):
            self.prob_over_sample['y'].append(self.data[i])

    def load_prob_over_time_in_arrays(self):
        self.prob_over_time['x'] = list()
        self.prob_over_time['y'] = list()
        for i in range(TIME_FIELD_START_INDEX,self.number_of_rows,2):
            self.prob_over_time['x'].append(self.data[i])
        for i in range(PROB_FIELD_START_INDEX,self.number_of_rows,2):
            self.prob_over_time['y'].append(self.data[i])

    def patch_time_over_sample_array_with_first_experiment_only(self):
        x = list()
        y = list()
        # we need to add 1 because of list slices in Python.
        # Iterate through all the x and y lists and extract the first
        # self.last_index_of_first_run values. These values
        # correspond to the first experiment only.
        x = self.time_over_sample['x'][0:self.last_index_of_first_run + 1]
        for i in range(0, len(self.time_over_sample['y'])):
            y.append(list())
            y[i] = self.time_over_sample['y'][i][0:self.last_index_of_first_run + 1]
        self.time_over_sample['x'] = x
        self.time_over_sample['y'] = y

    def patch_prob_over_sample_array_with_first_experiment_only(self):
        x = list()
        y = list()
        x = self.prob_over_sample['x'][0:self.last_index_of_first_run + 1]
        for i in range(0, len(self.prob_over_sample['y'])):
            y.append(list())
            y[i] = self.prob_over_sample['y'][i][0:self.last_index_of_first_run + 1]
        self.prob_over_sample['x'] = x
        self.prob_over_sample['y'] = y

    def patch_prob_over_time_array_with_first_experiment_only(self):
        x = list()
        y = list()
        for i in range(0, len(self.prob_over_time['y'])):
            x.append(list())
            x[i] = self.prob_over_time['x'][i][0:self.last_index_of_first_run + 1]
            y.append(list())
            y[i] = self.prob_over_time['y'][i][0:self.last_index_of_first_run + 1]
        self.prob_over_time['x'] = x
        self.prob_over_time['y'] = y

    def populate_disposable_data_structure_for_time_over_sample_plot(self):
        self.x = self.time_over_sample['x']
        self.y = self.time_over_sample['y']
        self.legend = self.time_over_sample['legend']
        self.x_label = self.time_over_sample['x label']
        self.y_label = self.time_over_sample['y label']
        self.title = self.time_over_sample['plot title']
        self.file_name = self.time_over_sample['file name']

    def populate_disposable_data_structure_for_prob_over_sample_plot(self):
        self.x = self.prob_over_sample['x']
        self.y = self.prob_over_sample['y']
        self.legend = self.prob_over_sample['legend']
        self.x_label = self.prob_over_sample['x label']
        self.y_label = self.prob_over_sample['y label']
        self.title = self.prob_over_sample['plot title']
        self.file_name = self.prob_over_sample['file name']

    def populate_disposable_data_structure_for_prob_over_time_plot(self):
        self.x = self.prob_over_time['x']
        self.y = self.prob_over_time['y']
        self.legend = self.prob_over_time['legend']
        self.x_label = self.prob_over_time['x label']
        self.y_label = self.prob_over_time['y label']
        self.title = self.prob_over_time['plot title']
        self.file_name = self.prob_over_time['file name']

    def compute_avg_and_stddev(self):
        pass

    def patch_x_if_necessary(self):
        # If x does not contain nested lists we need to replace its original content
        # with nested lists.
        if not any(isinstance(i, list) for i in self.x):
            tmp = list()
            for i in range(0, len(self.y)):
                tmp.append(self.x)
            self.x = tmp

    def plot(self, error_bars: bool = False, scientific_notation: bool = False):
        self.patch_x_if_necessary()
        for i in range(0, len(self.y)):
            if error_bars:
                pass
            else:
                plt.plot(self.x[i], self.y[i],markersize=2.5,linestyle='-',marker='o')

        plt.title(self.title)
        plt.legend(self.legend)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.savefig(self.file_name)
        # Flush output. Without this consecutive plots overlap.
        # See: https://stackoverflow.com/questions/17106288/matplotlib-pyplot-will-not-forget-previous-plots-how-can-i-flush-refresh
        plt.gcf().clear()


class MhVsGibbs(Utils):
    def __init__(self, filename, delimiter=',', experiment_name='arithm_sample'):
        self.time_over_sample = dict()
        self.prob_over_sample = dict()
        self.prob_over_time = dict()

        self.time_over_sample['x id'] = 'samples'
        self.time_over_sample['y ids'] = ['mh time','gibbs time']
        self.time_over_sample['stddev y ids'] = ['stddev mh time','stddev gibbs time']
        self.time_over_sample['legend'] = ['mh', 'gibbs']
        self.time_over_sample['x label'] = 'samples'
        self.time_over_sample['y label'] = 'running time (ms)'
        self.time_over_sample['plot title'] = 'time over sample mh vs gibbs ' + experiment_name
        self.time_over_sample['file name'] = 'plot_time_over_sample_mh_vs_gibbs.png'

        self.prob_over_sample['x id'] = 'samples'
        self.prob_over_sample['y ids'] = ['mh prob','gibbs prob']
        self.prob_over_sample['stddev y ids'] = ['stddev mh prob','stddev gibbs prob']
        self.prob_over_sample['legend'] = ['mh', 'gibbs']
        self.prob_over_sample['x label'] = 'samples'
        self.prob_over_sample['y label'] = 'probability (0,1)'
        self.prob_over_sample['plot title'] = 'prob over sample mh vs gibbs ' + experiment_name
        self.prob_over_sample['file name'] = 'plot_prob_over_sample_mh_vs_gibbs.png'

        self.prob_over_time['x id'] = 'time'
        self.prob_over_time['y ids'] = ['mh prob','gibbs prob']
        self.prob_over_time['stddev y ids'] = ['stddev mh prob','stddev gibbs prob']
        self.prob_over_time['legend'] = ['mh', 'gibbs']
        self.prob_over_time['x label'] = 'running time (ms)'
        self.prob_over_time['y label'] = 'probability (0,1)'
        self.prob_over_time['plot title'] = 'prob over time mh vs gibbs ' + experiment_name
        self.prob_over_time['file name'] = 'plot_prob_over_time_mh_vs_gibbs.png'

        super().__init__(filename, delimiter)


if __name__ == '__main__':
    # This is necessary to save the plot to a file instead of displaying it directly.
    matplotlib.use('Agg')
    # Get the file names from argv. This decides the type of plot.
    file_name_a=sys.argv[1]
    keep_first_experiment_only = bool(sys.argv[2])
    print(keep_first_experiment_only)
    print(sys.argv[1])
    print(sys.argv[2])
    if len(sys.argv) == 4:
        # Plot two tests.
        file_name_b=sys.argv[3]
    else:
        # Plot a single test.
        file_name_b=''
    delimiter=','
    if file_name_a == 'arithm_sample.csv':
        speeds = MhVsGibbs(file_name_a,delimiter,'arithm_sample')
        speeds.load_time_over_sample_in_arrays()
        speeds.patch_time_over_sample_array_with_first_experiment_only()
        speeds.populate_disposable_data_structure_for_time_over_sample_plot()
        speeds.plot()
        print(speeds.time_over_sample)
        speeds.load_prob_over_sample_in_arrays()
        speeds.patch_prob_over_sample_array_with_first_experiment_only()
        speeds.populate_disposable_data_structure_for_prob_over_sample_plot()
        speeds.plot()
        print(speeds.prob_over_sample)
        speeds.load_prob_over_time_in_arrays()
        speeds.patch_prob_over_time_array_with_first_experiment_only()
        speeds.populate_disposable_data_structure_for_prob_over_time_plot()
        speeds.plot()
        print(speeds.prob_over_time)
    else:
        print('code needs to be re-implemented. refer to older git commits')
