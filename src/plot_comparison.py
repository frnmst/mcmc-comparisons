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


def plot_comparison(data,x_id,y1_id,y2_id,legend=['set a', 'set b'],title='Comparison',x_label='x',y_label='y'):
    """ Plot two set of values for direct comparison."""
    x1 = x2 = data[x_id]
    y1 = data[y1_id]
    y2 = data[y2_id]
    plt.plot(x1,y1,markersize=2.5,linestyle='-', marker='o')
    plt.plot(x2,y2,markersize=2.5,linestyle='-', marker='o')
    plt.title(title)
    plt.legend(legend)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig('plot.png')


class Comparison():
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
            for row in data:
                self.data['run_number'].append(int(row[0]))
                self.data['samples'].append(int(row[1]))
                self.data['mh_time'].append(int(row[2]))
                self.data['mh_probability'].append(float(row[3]))
                self.data['gibbs_time'].append(int(row[4]))
                self.data['gibbs_probability'].append(float(row[5]))

    def compute_avg_run_time(self):
        total_runs = max(self.data['run_number'])
        sample_iterations = len(set(self.data['samples']))
        mh_times = list()
        gibbs_times = list()

        # Transform the original data into a matrix with:
        #   rows = current run
        #   columns = current sample set
        mh_matrix = np.matrix(self.data['mh_time'])
        mh_matrix = mh_matrix.reshape(total_runs, sample_iterations)
        gibbs_matrix = np.matrix(self.data['gibbs_time'])
        gibbs_matrix = gibbs_matrix.reshape(total_runs, sample_iterations)

        # Compute the average for each sample iteration.
        for sample_it in range(0, sample_iterations):
            mh_sum = 0
            gibbs_sum = 0
            for run in range(0,total_runs):
                mh_sum += mh_matrix.item(run,sample_it)
                gibbs_sum += gibbs_matrix.item(run,sample_it)
            mh_times.append(mh_sum/total_runs)
            gibbs_times.append(gibbs_sum/total_runs)

        # Override the original data sets.
        self.data['mh_time']=mh_times
        self.data['gibbs_time']=gibbs_times
        self.data['run_number']=sorted(list(set(self.data['run_number'])))
        self.data['samples']=sorted(list(set(self.data['samples'])))

    def arithm_sample_mh_vs_gibbs(self):
        plot_comparison(self.data,
                        'samples',
                        'mh_time',
                        'gibbs_time',
                        ['mh', 'gibbs'],
                        'arith sample mh vs gibbs avg',
                        'samples',
                        'running time (ms)')

    def arithm_sample_mh_vs_gibbs_avg(self):
        self.compute_avg_run_time()
        self.arithm_sample_mh_vs_gibbs()


def main():
    # Necessary to save the plot to a file instead of displaying it directly.
    matplotlib.use('Agg')
    speeds = Comparison('arithm_sample.csv',',')
    speeds.arithm_sample_mh_vs_gibbs_avg()

if __name__ == '__main__':
    main()
