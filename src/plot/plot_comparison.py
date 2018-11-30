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
import numpy as np
import csv
import sys

def plot_two_data_sets(data,
                    x_id,
                    y1_id,
                    y2_id,
                    y1_stddev,
                    y2_stddev,
                    legend=['set a', 'set b'],
                    title='Comparison',x_label='x',y_label='y'):
    """ Plot two set of values for direct comparison."""
    assert isinstance(data, dict)

    x1 = x2 = data[x_id]
    y1 = data[y1_id]
    y2 = data[y2_id]
    y1_stddev = data[y1_stddev]
    y2_stddev = data[y2_stddev]
    plt.errorbar(x1,y1,yerr=y1_stddev,markersize=2.5,linestyle='-',marker='o', capsize=2.5)
    plt.errorbar(x2,y2,yerr=y2_stddev,markersize=2.5,linestyle='-',marker='o', capsize=2.5)
    plt.title(title)
    plt.legend(legend)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig('plot.png')


def compute_avg_and_stddev_two_data_sets(data,key_a,key_b,rows_name,cols_name):
    # Init.
    rows = max(data[rows_name])
    cols = len(set(data[cols_name]))
    avg_a = list()
    avg_b = list()
    stddev_a = list()
    stddev_b = list()

    # Transform the original data into a matrix with:
    #   rows = current run
    #   columns = current sample set
    matrix_a = np.matrix(data[key_a])
    matrix_a = matrix_a.reshape(rows, cols)
    matrix_b = np.matrix(data[key_b])
    matrix_b = matrix_b.reshape(rows, cols)

    # Compute average and standard deviation
    # of the running times for each sample.
    for c in range(0, cols):
        sum_a = 0
        sum_b = 0
        stddev_buf_a = list()
        stddev_buf_b = list()
        for r in range(0,rows):
            sum_a += matrix_a.item(r,c)
            sum_b += matrix_b.item(r,c)

            stddev_buf_a.append(matrix_a.item(r,c))
            stddev_buf_b.append(matrix_b.item(r,c))

        avg_a.append(sum_a/rows)
        avg_b.append(sum_b/rows)

        stddev_a.append(np.std(stddev_buf_a))
        stddev_b.append(np.std(stddev_buf_b))

    return avg_a, avg_b, stddev_a, stddev_b


class MhVsGibbsComparison():
    def __init__(self, filename, delimiter=','):
        """ Load the file contents in a dictionary for future easy access."""
        self.data = { 'run_number': [],
                      'samples': [],
                      'mh_time': [],
                      'mh_probability': [],
                      'gibbs_time': [],
                      'gibbs_probability': [],
                    }

        with open(filename, 'r') as f:
            # Skip the first line
            # next(f)
            data = csv.reader(f, delimiter=delimiter)
            # Sort lines by run number and and keep sample id in place so that we maintain the correct
            # input for the other functions.
            data = sorted(data, key=lambda d: d[0])
            for row in data:
                self.data['run_number'].append(int(row[0]))
                self.data['samples'].append(int(row[1]))
                self.data['mh_time'].append(int(row[2]))
                self.data['mh_probability'].append(float(row[3]))
                self.data['gibbs_time'].append(int(row[4]))
                self.data['gibbs_probability'].append(float(row[5]))

    def plot_mh_vs_gibbs(self, plot_title):
        assert isinstance(plot_title,str)
        plot_two_data_sets(self.data,
                        'samples',
                        'mh_time',
                        'gibbs_time',
                        'mh_time_stddev',
                        'gibbs_time_stddev',
                        ['mh', 'gibbs'],
                        plot_title,
                        'samples',
                        'running time (ms)')

    def overwrite_data_set(self,mh_times_avg,gibbs_times_avg,mh_times_stddev,gibbs_times_stddev):
        self.data['mh_time']=mh_times_avg
        self.data['gibbs_time']=gibbs_times_avg
        self.data['run_number']=sorted(list(set(self.data['run_number'])))
        self.data['samples']=sorted(list(set(self.data['samples'])))
        self.data['mh_time_stddev']=mh_times_stddev
        self.data['gibbs_time_stddev']=gibbs_times_stddev

    def generic_mh_vs_gibbs_avg(self):
        mh_times_avg,gibbs_times_avg,mh_times_stddev,gibbs_times_stddev = compute_avg_and_stddev_two_data_sets(self.data,'mh_time','gibbs_time','run_number','samples')
        self.overwrite_data_set(mh_times_avg,gibbs_times_avg,mh_times_stddev,gibbs_times_stddev)

    # arithm_sample
    def arithm_sample_mh_vs_gibbs(self):
        self.plot_mh_vs_gibbs('arithm_sample mh vs gibbs avg')

    def arithm_sample_mh_vs_gibbs_avg(self):
        self.generic_mh_vs_gibbs_avg()
        self.arithm_sample_mh_vs_gibbs()

    # test33_sample
    def test33_sample_mh_vs_gibbs(self):
        self.plot_mh_vs_gibbs('test33_sample mh vs gibbs avg')

    def test33_sample_mh_vs_gibbs_avg(self):
        self.generic_mh_vs_gibbs_avg()
        self.test33_sample_mh_vs_gibbs()

    # test66_sample
    def test66_sample_mh_vs_gibbs(self):
        self.plot_mh_vs_gibbs('test66_sample mh vs gibbs avg')

    def test66_sample_mh_vs_gibbs_avg(self):
        self.generic_mh_vs_gibbs_avg()
        self.test66_sample_mh_vs_gibbs()

    # Prob avg && stddev TODO


def main():
    # This is necessary to save the plot to a file instead of displaying it directly.
    matplotlib.use('Agg')
    # Get the file name from argv. This decides the type of plot.
    file_name=sys.argv[1]
    if file_name == 'arithm_sample.csv':
        speeds = MhVsGibbsComparison(file_name,',')
        speeds.arithm_sample_mh_vs_gibbs_avg()
    elif file_name == 'test33_sample.csv':
        speeds = MhVsGibbsComparison(file_name,',')
        speeds.test33_sample_mh_vs_gibbs_avg()
    elif file_name == 'test66_sample.csv':
        speeds = MhVsGibbsComparison(file_name,',')
        speeds.test66_sample_mh_vs_gibbs_avg()

if __name__ == '__main__':
    main()
