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

class Utils():

    def __init__(self, files: list):
        """ Load the file contents in a dictionary for future easy access."""
        for f in files:
            assert isinstance(f, dict)
            assert 'name' in f
            assert 'delimiter' in f
            assert 'fields' in f
            assert isinstance(f['name'], str)
            assert isinstance(f['delimiter'], str)
            assert isinstance(f['fields'], list)
            for i in f['fields']:
                assert isinstance(i, str)

        self.data = dict()

        for f in files:
            for i in f['fields']:
                self.data[i] = list()

        for file in files:
            with open(file['name'], 'r') as f:
                data = csv.reader(f, delimiter=file['delimiter'])
                # Sort lines by run number and and keep sample id in place so
                # that we maintain the correct input for the other functions.
                data = sorted(data, key=lambda d: d[0])
                for row in data:
                    self.data[file['fields'][0]].append(int(row[0]))
                    self.data[file['fields'][1]].append(int(row[1]))
                    # Three way comparison uses 8 fileds instead of 6. That's why we need
                    # these conditions.
                    for i in range(2,len(file['fields']),2):
                        self.data[file['fields'][i]].append(int(round(float(row[i]))))
                        self.data[file['fields'][i+1]].append(float(row[i+1]))

        print(self.data)

    def plot_data_sets(self, x_id: str, y_ids: list, y_stddev_ids: list, legend: list=['set a', 'set b'],
                       title: str='Comparison', x_label: str='x', y_label: str='y', plot_file: str='plot.png', use_scientific_notation: bool = False, use_stddev: bool = True):
        r"""Plot n sets of values for direct comparison.

        .. note: scientific notation is available for the y axis only. See:
                 https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.ticklabel_format.html
        """
        for e in y_ids:
            assert isinstance(e, str)
        for e in y_stddev_ids:
            assert isinstance(e, str)
        for e in legend:
            assert isinstance(e, str)
        if use_stddev:
            assert (len(y_ids) == len(y_stddev_ids) == len(legend))
        else:
            assert (len(y_ids) == len(legend))

        print("START")
        print(self.data[x_id])
        print("===")
        print(self.data[y_ids[0]])
        print("===")
        print(self.data[y_ids[1]])
        print("===")
        print(legend)


        if use_scientific_notation:
            plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 3))
        j = 0
        for i in range(0,len(y_ids)):
            if use_stddev:
                plt.errorbar(self.data[x_id],self.data[y_ids[i]],yerr=self.data[y_stddev_ids[i]],markersize=2.5,linestyle='-',marker='o', capsize=2.5)
            else:
                prev = j
                j = prev + len(self.data[y_ids[i]])
                print("here===")
                print(self.data[x_id][prev:j])
                print(self.data[y_ids[i]])
                plt.plot(self.data[x_id][prev:j],self.data[y_ids[i]],markersize=2.5,linestyle='-',marker='o')
        plt.title(title)
        plt.legend(legend)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(plot_file)
        # Flush output. Without this consecutive plots overlap.
        # See: https://stackoverflow.com/questions/17106288/matplotlib-pyplot-will-not-forget-previous-plots-how-can-i-flush-refresh
        plt.gcf().clear()

    def compute_avg_and_stddev_data_sets(self, dim_id: list, rows_name: str, cols_name: str) -> dict:
        r"""Compute averages and standard deviations for all input dimensions."""
        for e in dim_id:
            assert isinstance(e, str)

        # Rows name and cols name must be the same for all cases.

        # Init.
        rows = max(self.data[rows_name])
        cols = len(set(self.data[cols_name]))
        dim=dict()
        for k in dim_id:
            dim[k]=list()
            dim['stddev_' + k]=list()

        # Transform the original data into a matrix of size rows x cols, where:
        #   rows = current run
        #   columns = current sample set
        # matrix_dim is a set of matrices.
        matrix_dim=dict()
        for k in dim_id:
            matrix_dim[k]=np.matrix(self.data[k])
            matrix_dim[k]=matrix_dim[k].reshape(rows, cols)

        #   matrix_dim[i]:
        #
        #    Samples    1000    2000    3000    ...
        # Run           ---------------------------
        #           1  | times or probs
        #           2  |
        #           3  |
        #           .. |
        #               sum_0   sum_1   sum_i
        #
        #        avg_i = sum_i / #(runs)

        # Compute average and standard deviation
        # of the running times for each sample.
        for c in range(0, cols):
            sum=dict()
            stddev_buf=dict()
            for k in dim_id:
                sum[k] = 0
                stddev_buf[k] = list()
            for r in range(0,rows):
                # To compute the average, we need to sum elements of the same
                # column so we need to iterate by row.
                for k in dim_id:
                    sum[k] += matrix_dim[k].item(r,c)
                    stddev_buf[k].append(matrix_dim[k].item(r,c))
            for k in dim_id:
                # Compute avgs by column.
                dim[k].append(sum[k]/rows)
                dim['stddev_' + k].append(np.std(stddev_buf[k]))

        return dim

    def overwrite_data_set_with_avg(self, dims_avg: dict):
        for key, value in dims_avg.items():
            if key == 'run_number' or key == 'samples':
                # Remove duplicates from these two sets.
                self.data[key]=sorted(list(set(self.data[key])))
            else:
                self.data[key]=value

    def overwrite_data_set_with_first_experiment_only(self):
        # TODO FIXME.
        for key, value in self.data():
            if key == 'run_number' and value == 1:
                # Remove duplicates from these two sets.
                self.data[key]=sorted(list(set(self.data[key])))
            else:
                self.data[key]=value


class MhVsGibbs(Utils):
    def __init__(self, filename, delimiter=',', fields = ['run_number', 'samples', 'mh_time', 'mh_prob', 'gibbs_time', 'gibbs_prob']):
        self.file={ 'name': filename, 'delimiter': delimiter, 'fields': fields }
        files=[self.file]
        super().__init__(files)

        self.times_over_samples_x_id = 'samples'
        self.times_over_samples_y_ids=['mh_time','gibbs_time']
        self.times_over_samples_stddev_y_ids=['stddev_mh_time','stddev_gibbs_time']
        self.times_over_samples_legend=['mh', 'gibbs']
        self.times_over_samples_x_label='samples'
        self.times_over_samples_y_label='running time (ms)'

        self.probs_over_samples_x_id = 'samples'
        self.probs_over_samples_y_ids = ['mh_prob','gibbs_prob']
        self.probs_over_samples_stddev_y_ids=['stddev_mh_prob','stddev_gibbs_prob']
        self.probs_over_samples_legend=['mh', 'gibbs']
        self.probs_over_samples_x_label='samples'
        self.probs_over_samples_y_label='probability [0,1]'

        # time needs to be created separately.
        self.probs_over_times_x_id = 'time'
        self.probs_over_times_y_ids = ['mh_prob','gibbs_prob']
        self.probs_over_times_stddev_y_ids=['stddev_mh_prob','stddev_gibbs_prob']
        self.probs_over_times_legend=['mh', 'gibbs']
        self.probs_over_times_x_label='running time (ms)'
        self.probs_over_times_y_label='probability [0,1]'

        self.dim_id=self.file['fields'][2:]

    def plot_times_over_samples(self, plot_title, plot_file):
            self.plot_data_sets(self.times_over_samples_x_id,
                            self.times_over_samples_y_ids,
                            self.times_over_samples_stddev_y_ids,
                            self.times_over_samples_legend,
                            plot_title,
                            self.times_over_samples_x_label,
                            self.times_over_samples_y_label,
                            plot_file,
                            True,
                            True)

    def plot_probs_over_samples(self, plot_title, plot_file):
            self.plot_data_sets(self.probs_over_samples_x_id,
                            self.probs_over_samples_y_ids,
                            self.probs_over_samples_stddev_y_ids,
                            self.probs_over_samples_legend,
                            plot_title,
                            self.probs_over_samples_x_label,
                            self.probs_over_samples_y_label,
                            plot_file,
                            False,
                            True)

    def plot_probs_over_times(self, plot_title, plot_file):
            self.plot_data_sets(self.probs_over_times_x_id,
                            self.probs_over_times_y_ids,
                            self.probs_over_times_stddev_y_ids,
                            self.probs_over_times_legend,
                            plot_title,
                            self.probs_over_times_x_label,
                            self.probs_over_times_y_label,
                            plot_file,
                            False,
                            False)

    def replace_dataset_to_avg(self):
        avgs = self.compute_avg_and_stddev_data_sets(self.dim_id,'run_number','samples')
        avgs['run_number']=self.data['run_number']
        avgs['samples']=self.data['samples']
        self.overwrite_data_set_with_avg(avgs)


class ArithmSampleMhVsGibbs(MhVsGibbs):
    def arithm_sample_mh_vs_gibbs(self, keep_first_experiment_only=False):
        if keep_first_experiment_only:
            self.data['time'] = self.data['mh_time'] +  self.data['mh_time']
            self.plot_times_over_samples('arithm_sample mh vs gibbs times','plot_arithm_sample_mh_vs_gibbs_times.png')
            self.plot_probs_over_samples('arithm_sample mh vs gibbs probs','plot_arithm_sample_mh_vs_gibbs_probs.png')
            self.plot_probs_over_times('arithm_sample mh vs gibbs probs over time','plot_arithm_sample_mh_vs_gibbs_probs_over_time.png')
        else:
            self.data['time'] = self.data['mh_time'] + self.data['gibbs_time']
            self.plot_probs_over_times('arithm_sample mh vs gibbs probs over time avg','plot_arithm_sample_mh_vs_gibbs_probs_over_time_avg.png')
            self.replace_dataset_to_avg()
            self.plot_times_over_samples('arithm_sample mh vs gibbs times avg','plot_arithm_sample_mh_vs_gibbs_times_avg.png')
            self.plot_probs_over_samples('arithm_sample mh vs gibbs probs avg','plot_arithm_sample_mh_vs_gibbs_probs_avg.png')



"""
class MhVsGibbsVsRejection(MhVsGibbs):
    def __init__(self, filename, delimiter=',', fields = ['run_number', 'samples', 'mh_time', 'mh_prob', 'gibbs_time', 'gibbs_prob', 'rejection_time', 'rejection_prob']):
        super().__init__(filename, delimiter, fields)

        self.times_over_samples_x_id = 'samples'
        self.times_over_samples_y_ids=['mh_time','gibbs_time','rejection_time']
        self.times_over_samples_stddev_y_ids=['stddev_mh_time','stddev_gibbs_time', 'stddev_rejection_time']
        self.times_over_samples_legend=['mh', 'gibbs', 'rejection']
        self.times_over_samples_x_label='samples'
        self.times_over_samples_y_label='running time (ms)'

        self.probs_over_samples_stddev_y_ids=['stddev_mh_prob','stddev_gibbs_prob', 'stddev_rejection_prob']
        self.probs_over_samples_x_id = 'samples'
        self.probs_over_samples_y_ids = ['mh_prob','gibbs_prob','rejection_prob']
        self.probs_over_samples_legend=['mh', 'gibbs', 'rejection']
        self.probs_over_samples_x_label='samples'
        self.probs_over_samples_y_label='probability [0,1]'

        self.dim_id=self.file['fields'][2:]

class ArithmSampleMhVsGibbsVsRejection(MhVsGibbsVsRejection):
    def arithm_sample_mh_vs_gibbs_vs_rejection(self, keep_first_experiment_only):
        self.replace_dataset_to_avg()
        self.plot_times_over_samples('arithm_sample mh vs gibbs vs rejection times avg','plot_arithm_sample_mh_vs_gibbs_vs_rejection_times.png')
        self.plot_probs_over_samples('arithm_sample mh vs gibbs vs rejection probs avg','plot_arithm_sample_mh_vs_gibbs_vs_rejection_probs.png')
"""

def main():
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
    if file_name_a == 'arithm_sample.csv' and file_name_b == 'arithm_cond_prob.csv':
        speeds = ArithmFourWayComparison({ 'no_amcmc': file_name_a , 'amcmc': file_name_b }, delimiter)
        speeds.arithm_four_way_comparison_avg()
    elif file_name_a == 'test33_sample.csv' and file_name_b == 'test33_cond_prob.csv':
        speeds = Test33FourWayComparison({ 'no_amcmc': file_name_a , 'amcmc': file_name_b }, delimiter)
        speeds.test33_four_way_comparison_avg()
    elif file_name_a == 'arithm_sample.csv':
        speeds = ArithmSampleMhVsGibbs(file_name_a,delimiter)
        speeds.arithm_sample_mh_vs_gibbs(keep_first_experiment_only)
    elif file_name_a == 'arithm_sample_three.csv':
        speeds = ArithmSampleMhVsGibbsVsRejection(file_name_a,delimiter)
        speeds.arithm_sample_mh_vs_gibbs_vs_rejection(keep_first_experiment_only)
    elif file_name_a == 'arithm_rejection_sample.csv':
        print("plot code needs refactoring")
        #speeds = ArithmRejectionSampleMhVsGibbs(file_name_a,delimiter)
        #speeds.arithm_rejection_sample_mh_vs_gibbs_avg()
    elif file_name_a == 'test33_sample.csv':
        print("plot code needs refactoring")
        #speeds = Test33SampleMhVsGibbs(file_name_a,delimiter)
        #speeds.test33_sample_mh_vs_gibbs_avg()
    elif file_name_a == 'test66_sample.csv':
        print("plot code needs refactoring")
        #speeds = Test66SampleMhVsGibbs(file_name_a,delimiter)
        #speeds.test66_sample_mh_vs_gibbs_avg()
    elif file_name_a == 'test33_cond_prob.csv':
        print("plot code needs refactoring")
        #speeds = Test33CondProbAdaptOnVsAdaptOff(file_name_a,delimiter)
        #speeds.test33_cond_prob_adapt_on_vs_adapt_off_avg()
    elif file_name_a == 'test66_cond_prob.csv':
        print("plot code needs refactoring")
        #speeds = Test66CondProbAdaptOnVsAdaptOff(file_name_a,delimiter)
        #speeds.test66_cond_prob_adapt_on_vs_adapt_off_avg()
    elif file_name_a == 'arithm_cond_prob.csv':
        print("plot code needs refactoring")
        #speeds = ArithmCondProbAdaptOnVsAdaptOff(file_name_a,delimiter)
        #speeds.arithm_cond_prob_adapt_on_vs_adapt_off_avg()

if __name__ == '__main__':
    main()
