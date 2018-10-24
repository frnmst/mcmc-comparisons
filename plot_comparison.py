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
import csv


def plot_comparison(x1,x2,y1,y2,legend=['set a', 'set b'],title='Comparison',xlabel='x',ylabel='y'):
    """ Plot two set of values for direct comparison."""
    plt.plot(x1,y1,markersize=2.5,linestyle='-', marker='o')
    plt.plot(x2,y2,markersize=2.5,linestyle='-', marker='o')
    plt.title(title)
    plt.legend(legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig('plot.png')

def plot_data_comparison(data,x_id,y1_id,y2_id,legend,title,x_label,y_label):
    x1 = x2 = data[x_id]
    y1 = data[y1_id]
    y2 = data[y2_id]
    plot_comparison(x1,
                    x2,
                    y1,
                    y2,legend,
                    title.replace('_',' '),
                    x_label,
                    y_label)


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

    def arithm_sample_mh_vs_gibbs(self):
        plot_data_comparison(self.data,
                             'samples',
                             'mh_time',
                             'gibbs_time',
                             ['mh', 'gibbs'],
                             'arith_sample_mh_vs_gibbs',
                             'samples',
                             'running time (ms)')


def main():
    matplotlib.use('Agg')
    speeds = Comparison('arithm_sample.csv',',')
    speeds.arithm_sample_mh_vs_gibbs()

if __name__ == '__main__':
    main()
