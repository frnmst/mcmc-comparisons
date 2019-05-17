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
RUN_NUMBER_INDEX = 0
SAMPLE_INDEX = 1
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

    def compute_avg(self):
        pass

    def load_time_over_sample_in_arrays(self):
        # We need to extract only the relevant data without altering
        # the main data structure.
        self.time_over_sample['x'] = self.data[SAMPLE_INDEX]
        self.time_over_sample['y'] = list()
        for i in range(TIME_FIELD_START_INDEX,self.number_of_rows,2):
            self.time_over_sample['y'].append(self.data[i])

    def load_prob_over_sample_in_arrays(self):
        self.prob_over_sample['x'] = self.data[SAMPLE_INDEX]
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

    def populate_disposable_data_structure_for_time_over_sample(self):
        self.x = self.time_over_sample['x']
        self.y = self.time_over_sample['y']
        self.legend = self.time_over_sample['legend']
        self.x_label = self.time_over_sample['x label']
        self.y_label = self.time_over_sample['y label']
        self.title = self.time_over_sample['plot title']
        self.file_name = self.time_over_sample['file name']

    def populate_disposable_data_structure_for_prob_over_sample(self):
        self.x = self.prob_over_sample['x']
        self.y = self.prob_over_sample['y']
        self.legend = self.prob_over_sample['legend']
        self.x_label = self.prob_over_sample['x label']
        self.y_label = self.prob_over_sample['y label']
        self.title = self.prob_over_sample['plot title']
        self.file_name = self.prob_over_sample['file name']

    def populate_disposable_data_structure_for_prob_over_time(self):
        self.x = self.prob_over_time['x']
        self.y = self.prob_over_time['y']
        self.legend = self.prob_over_time['legend']
        self.x_label = self.prob_over_time['x label']
        self.y_label = self.prob_over_time['y label']
        self.title = self.prob_over_time['plot title']
        self.file_name = self.prob_over_time['file name']

    def patch_sort_prob_over_time_x_and_y_by_ascending_x_values(self):
        tmp_x = list()
        tmp_y = list()
        for i in range(0,len(self.x)):
            tmp_x.append(0)
            tmp_y.append(0)
            tmp_x[i], tmp_y[i] = zip(*sorted(zip(self.x[i],self.y[i])))
            tmp_x[i] = list(tmp_x[i])
            tmp_y[i] = list(tmp_y[i])
        self.x = tmp_x
        self.y = tmp_y

        # Override to update.
        self.prob_over_time['x'] = self.x
        self.prob_over_time['y'] = self.y

    def patch_x_as_nested_list(self):
        # If x does not contain nested lists we need to replace its original content
        # with nested lists.
        if not any(isinstance(i, list) for i in self.x):
            tmp = list()
            for i in range(0, len(self.y)):
                tmp.append(self.x)
            self.x = tmp

    def compute_avg_and_stddev(self):
        rows = sorted(list(set(self.data[RUN_NUMBER_INDEX])))
        cols = sorted(list(set(self.data[SAMPLE_INDEX])))
        number_of_rows = len(rows)
        number_of_cols = len(cols)

        # Define the standard deviation.
        self.stddev = list()

        stddev = list()
        matrix_it = list()
        avg = list()
        for i in range(0,len(self.y)):
            matrix_it.append(np.array(self.y[i]).reshape(number_of_rows, number_of_cols))
            # average and stddev using the number of rows (axis=0):
            avg.append(np.ndarray.tolist(np.average(matrix_it[i],axis=0)))
            stddev.append(np.ndarray.tolist(np.std(matrix_it[i],axis=0)))
            self.stddev.append(stddev[i])

            #   matrix_it[i]:
            #
            #    Samples ->  1000    2000    3000    ...
            # Run           ---------------------------
            #  |         1  | times or probs
            #  ->        2  |
            #            3  |
            #            .. |
            #            ------------------------------
            #                 sum[0]   sum[1]   sum[i]
            #
            #        avg[i] = sum[i] / #(runs)

            # Override plot data.
            self.y[i] = avg[i]
        self.x = cols

    def plot(self, error_bars: bool = False):
        for i in range(0, len(self.y)):
            if max(self.x[i]) >= 10000:
                plt.ticklabel_format(axis='x', style='sci', scilimits=(0, 3))
            if max(self.y[i]) >= 10000:
                plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 3))
            if error_bars:
                plt.errorbar(self.x[i],self.y[i],yerr=self.stddev[i],markersize=2.5,linestyle='-',marker='o', capsize=2.5)
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
        experiment_filename = experiment_name.replace(' ','_')

        self.time_over_sample['legend'] = ['mh', 'gibbs']
        self.time_over_sample['x label'] = 'samples'
        self.time_over_sample['y label'] = 'running time (ms)'
        self.time_over_sample['plot title'] = experiment_name
        self.time_over_sample['file name'] = 'plot_time_over_sample_mh_vs_gibbs_' + experiment_filename + '.png'

        self.prob_over_sample['legend'] = ['mh', 'gibbs']
        self.prob_over_sample['x label'] = 'samples'
        self.prob_over_sample['y label'] = 'probability (0,1)'
        self.prob_over_sample['plot title'] = experiment_name
        self.prob_over_sample['file name'] = 'plot_prob_over_sample_mh_vs_gibbs_' + experiment_filename + '.png'

        self.prob_over_time['legend'] = ['mh', 'gibbs']
        self.prob_over_time['x label'] = 'running time (ms)'
        self.prob_over_time['y label'] = 'probability (0,1)'
        self.prob_over_time['plot title'] = experiment_name
        self.prob_over_time['file name'] = 'plot_prob_over_time_mh_vs_gibbs_' + experiment_filename + '.png'

        super().__init__(filename, delimiter)

class MhVsGibbsVsRejection(Utils):
    def __init__(self, filename, delimiter=',', experiment_name='arithm_sample_three'):
        self.time_over_sample = dict()
        self.prob_over_sample = dict()
        self.prob_over_time = dict()
        experiment_filename = experiment_name.replace(' ','_')

        self.time_over_sample['legend'] = ['mh', 'gibbs', 'rejection']
        self.time_over_sample['x label'] = 'samples'
        self.time_over_sample['y label'] = 'running time (ms)'
        self.time_over_sample['plot title'] = experiment_name
        self.time_over_sample['file name'] = 'plot_time_over_sample_mh_vs_gibbs_vs_rejection_' + experiment_filename + '.png'

        self.prob_over_sample['legend'] = ['mh', 'gibbs', 'rejection']
        self.prob_over_sample['x label'] = 'samples'
        self.prob_over_sample['y label'] = 'probability (0,1)'
        self.prob_over_sample['plot title'] = experiment_name
        self.prob_over_sample['file name'] = 'plot_prob_over_sample_mh_vs_gibbs_vs_rejection_' + experiment_filename + '.png'

        self.prob_over_time['legend'] = ['mh', 'gibbs', 'rejection']
        self.prob_over_time['x label'] = 'running time (ms)'
        self.prob_over_time['y label'] = 'probability (0,1)'
        self.prob_over_time['plot title'] = experiment_name
        self.prob_over_time['file name'] = 'plot_prob_over_time_mh_vs_gibbs_vs_rejection_' + experiment_filename + '.png'

        super().__init__(filename, delimiter)

if __name__ == '__main__':
    # This is necessary to save the plot to a file instead of displaying it directly.
    matplotlib.use('Agg')
    # Get the file names from argv. This decides the type of plot.
    experiment_name_a=sys.argv[1]
    file_name_a=sys.argv[2]
    keep_first_experiment_only = bool(sys.argv[3])

    if len(sys.argv) == 6:
        experiment_name_b=sys.argv[4]
        file_name_b=sys.argv[5]
    else:
        # Plot a single test.
        experiment_name_b=''
        file_name_b=''

    delimiter=','
    if keep_first_experiment_only:
        error_bars = False
        experiment_name_preamble=str()
    else:
        error_bars = True
        experiment_name_preamble='avg of '
    if experiment_name_a == 'arithm_sample':
        speeds = MhVsGibbs(file_name_a,delimiter,experiment_name_preamble + 'arithm_sample')

        speeds.load_time_over_sample_in_arrays()
        if keep_first_experiment_only:
            speeds.patch_time_over_sample_array_with_first_experiment_only()
        speeds.populate_disposable_data_structure_for_time_over_sample()
        if not keep_first_experiment_only:
            speeds.compute_avg_and_stddev()
        speeds.patch_x_as_nested_list()
        speeds.plot(error_bars)

        speeds.load_prob_over_sample_in_arrays()
        if keep_first_experiment_only:
            speeds.patch_prob_over_sample_array_with_first_experiment_only()
        speeds.populate_disposable_data_structure_for_prob_over_sample()
        if not keep_first_experiment_only:
            speeds.compute_avg_and_stddev()
        speeds.patch_x_as_nested_list()
        speeds.plot(error_bars)

        if keep_first_experiment_only:
            speeds.load_prob_over_time_in_arrays()
            # See the next comment.
            speeds.patch_prob_over_time_array_with_first_experiment_only()
            speeds.populate_disposable_data_structure_for_prob_over_time()
            speeds.patch_sort_prob_over_time_x_and_y_by_ascending_x_values()
            # Average and stddev does not make sense for this type of plot
            # because prob is not groupable by time.
            speeds.patch_x_as_nested_list()
            speeds.plot()
    elif experiment_name_a == 'arithm_sample_three':
        speeds = MhVsGibbsVsRejection(file_name_a,delimiter,experiment_name_preamble + 'arithm_sample_three')

        speeds.load_time_over_sample_in_arrays()
        if keep_first_experiment_only:
            speeds.patch_time_over_sample_array_with_first_experiment_only()
        speeds.populate_disposable_data_structure_for_time_over_sample()
        if not keep_first_experiment_only:
            speeds.compute_avg_and_stddev()
        speeds.patch_x_as_nested_list()
        error_bars = False
        if not keep_first_experiment_only:
            error_bars = True
        speeds.plot(error_bars)

        speeds.load_prob_over_sample_in_arrays()
        if keep_first_experiment_only:
            speeds.patch_prob_over_sample_array_with_first_experiment_only()
        speeds.populate_disposable_data_structure_for_prob_over_sample()
        if not keep_first_experiment_only:
            speeds.compute_avg_and_stddev()
        speeds.patch_x_as_nested_list()
        error_bars = False
        if not keep_first_experiment_only:
            error_bars = True
        speeds.plot(error_bars)

        if keep_first_experiment_only:
            speeds.load_prob_over_time_in_arrays()
            # See the next comment.
            speeds.patch_prob_over_time_array_with_first_experiment_only()
            speeds.populate_disposable_data_structure_for_prob_over_time()
            speeds.patch_sort_prob_over_time_x_and_y_by_ascending_x_values()
            # Average and stddev does not make sense for this type of plot
            # because prob is not groupable by time.
            speeds.patch_x_as_nested_list()
            speeds.plot()
    elif experiment_name_a == 'hmm_sample_three':
        speeds = MhVsGibbsVsRejection(file_name_a,delimiter,experiment_name_preamble + 'hmm_sample_three')

        speeds.load_time_over_sample_in_arrays()
        if keep_first_experiment_only:
            speeds.patch_time_over_sample_array_with_first_experiment_only()
        speeds.populate_disposable_data_structure_for_time_over_sample()
        if not keep_first_experiment_only:
            speeds.compute_avg_and_stddev()
        speeds.patch_x_as_nested_list()
        error_bars = False
        if not keep_first_experiment_only:
            error_bars = True
        speeds.plot(error_bars)

        speeds.load_prob_over_sample_in_arrays()
        if keep_first_experiment_only:
            speeds.patch_prob_over_sample_array_with_first_experiment_only()
        speeds.populate_disposable_data_structure_for_prob_over_sample()
        if not keep_first_experiment_only:
            speeds.compute_avg_and_stddev()
        speeds.patch_x_as_nested_list()
        error_bars = False
        if not keep_first_experiment_only:
            error_bars = True
        speeds.plot(error_bars)

        if keep_first_experiment_only:
            speeds.load_prob_over_time_in_arrays()
            # See the next comment.
            speeds.patch_prob_over_time_array_with_first_experiment_only()
            speeds.populate_disposable_data_structure_for_prob_over_time()
            speeds.patch_sort_prob_over_time_x_and_y_by_ascending_x_values()
            # Average and stddev does not make sense for this type of plot
            # because prob is not groupable by time.
            speeds.patch_x_as_nested_list()
            speeds.plot()
    else:
        print('code needs to be re-implemented. refer to older git commits')
