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

class Utils():

    def __init__(self, filename, delimiter=',', iteration='it', x_axis='x', dim_a='a', dim_b='b', dim_c='c', dim_d='d'):
        """ Load the file contents in a dictionary for future easy access."""
        assert isinstance(filename, str)
        assert isinstance(iteration, str)
        assert isinstance(x_axis, str)
        assert isinstance(dim_a, str)
        assert isinstance(dim_b, str)
        assert isinstance(dim_c, str)
        assert isinstance(dim_d, str)

        self.data = { iteration: [],
                      x_axis: [],
                      dim_a: [],
                      dim_b: [],
                      dim_c: [],
                      dim_d: [],
                    }

        with open(filename, 'r') as f:
            data = csv.reader(f, delimiter=delimiter)
            # Sort lines by run number and and keep sample id in place so that we maintain the correct
            # input for the other functions.
            data = sorted(data, key=lambda d: d[0])
            for row in data:
                self.data[iteration].append(int(row[0]))
                self.data[x_axis].append(int(row[1]))
                self.data[dim_a].append(int(round(float(row[2]))))
                self.data[dim_b].append(float(row[3]))
                self.data[dim_c].append(int(round(float(row[4]))))
                self.data[dim_d].append(float(row[5]))

    def plot_data_sets(
                   data,
                   x_id,
                   y_ids,
                   y_stddev_ids,
                   legend=['set a', 'set b'],
                   title='Comparison',
                   x_label='x',
                   y_label='y',
                   plot_file='plot.png'):
        """ Plot n sets of values for direct comparison."""
        assert isinstance(x_id, str)
        assert isinstance(y_ids, list)
        for e in y_ids:
            assert isinstance(e, str)
        assert isinstance(y_stddev_ids, list)
        for e in y_stddev_ids:
            assert isinstance(e, str)
        assert isinstance(legend, list)
        for e in legend:
            assert isinstance(e, str)
        assert (len(y_ids) == len(y_stddev_ids) == len(legend))

        for i in range(0,len(y_ids)):
            plt.errorbar(data[x_id],data[y_ids[i]],yerr=data[y_stddev_ids[i]],markersize=2.5,linestyle='-',marker='o', capsize=2.5)
        plt.title(title)
        plt.legend(legend)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(plot_file)
        # Flush output. Without this consecutive plots overlap.
        # See: https://stackoverflow.com/questions/17106288/matplotlib-pyplot-will-not-forget-previous-plots-how-can-i-flush-refresh
        plt.gcf().clear()

    # Rows name and cols name is the same for all cases.
    def compute_avg_and_stddev_two_data_sets(self, dim_id, rows_name, cols_name):
        assert isinstance(dim_id, list)
        for e in dim_id:
            assert isinstance(e, str)
        assert isinstance(rows_name, str)
        assert isinstance(cols_name, str)

        # Init.
        rows = max(self.data[rows_name])
        cols = len(set(self.data[cols_name]))
        dim=dict()
        for k in dim_id:
            dim[k]=list()
            dim['stddev_' + k]=list()

        # Transform the original data into a matrix with:
        #   rows = current run
        #   columns = current sample set
        matrix_dim=dict()
        for k in dim_id:
            matrix_dim[k]=np.matrix(self.data[k])
            matrix_dim[k]=matrix_dim[k].reshape(rows, cols)

        # Compute average and standard deviation
        # of the running times for each sample.
        for c in range(0, cols):
            sum=dict()
            stddev_buf=dict()
            for k in dim_id:
                sum[k] = 0
                stddev_buf[k] = list()
            for r in range(0,rows):
                for k in dim_id:
                    sum[k] += matrix_dim[k].item(r,c)
                    stddev_buf[k].append(matrix_dim[k].item(r,c))

            for k in dim_id:
                dim[k].append(sum[k]/rows)
                dim['stddev_' + k].append(np.std(stddev_buf[k]))

        return dim

    def plot_frontend(self, plot_title, plot_file, running_times, running_times_stddev, legend, y_label):
            assert isinstance(plot_title,str)
            assert isinstance(plot_file,str)
            assert isinstance(running_times, list)
            for e in running_times:
                assert isinstance(e, str)
            assert isinstance(running_times_stddev, list)
            for e in running_times_stddev:
                assert isinstance(e, str)
            assert isinstance(legend, list)
            for e in legend:
                assert isinstance(e, str)
            assert isinstance(y_label, str)

            plot_two_data_sets(data,
                            'samples',
                            running_times,
                            running_times_stddev,
                            legend,
                            plot_title,
                            'samples',
                            y_label,
                            plot_file)


    def overwrite_data_set_with_avg(self, dim_id_avg, dim_value_avg):
        # Assume that the list have a semantic order between them: l1[0] -> l2[0].
        assert isinstance(dim_id_avg, list)
        assert isinstance(dim_value_avg, list)

        for d in dim_id_avg:
            self.data[d]=dim_value_avg[dim_id_avg.index(d)]


class MhVsGibbs(Utils):

    def __init__(self, filename, delimiter=','):
        super().__init__(filename, delimiter, 'run_number', 'samples', 'mh_time', 'mh_prob', 'gibbs_time', 'gibbs_prob')

    def plot_mh_vs_gibbs_times(self, plot_title, plot_file):
        plot_frontend(self.data, plot_title, plot_file, ['mh_time', 'gibbs_time'], ['mh_time_stddev', 'gibbs_time_stddev'], ['mh', 'gibbs'],'running time (ms)')

    def plot_mh_vs_gibbs_probs(self, plot_title, plot_file):
        plot_frontend(self.data, plot_title, plot_file, ['mh_prob', 'gibbs_prob'], ['mh_prob_stddev', 'gibbs_prob_stddev'], ['mh', 'gibbs'], 'probability [0,1]')

    def overwrite_avg_data_set(self,mh_times_avg,gibbs_times_avg,mh_times_stddev,gibbs_times_stddev):
        self.overwrite_data_set_with_avg(['mh_time', 'gibbs_time', 'run_number', 'samples', 'mh_time_stddev', 'gibbs_time_stddev'],
                                    [mh_times_avg, gibbs_times_avg, sorted(list(set(self.data['run_number']))), sorted(list(set(self.data['samples']))), mh_times_stddev, gibbs_times_stddev])

    def overwrite_prob_data_set(self,mh_probs_avg,gibbs_probs_avg,mh_probs_stddev,gibbs_probs_stddev):
        self.overwrite_data_set_with_avg(['mh_prob', 'gibbs_prob', 'run_number', 'samples', 'mh_prob_stddev', 'gibbs_prob_stddev'],
                                    [mh_probs_avg, gibbs_probs_avg, sorted(list(set(self.data['run_number']))), sorted(list(set(self.data['samples']))), mh_probs_stddev, gibbs_probs_stddev])

    def mh_vs_gibbs_times_avg(self):
        times_avg, stddev_times_avg = self.compute_avg_and_stddev_two_data_sets(['mh_time','gibbs_time'],'run_number','samples')
        mh_times_avg,gibbs_times_avg,mh_times_stddev,gibbs_times_stddev = None
        self.overwrite_data_set_with_avg(mh_times_avg,gibbs_times_avg,mh_times_stddev,gibbs_times_stddev)

    def mh_vs_gibbs_probs_avg(self):
        mh_probs_avg,gibbs_probs_avg,mh_probs_stddev,gibbs_probs_stddev = self.compute_avg_and_stddev_two_data_sets('mh_prob','gibbs_prob','run_number','samples')
        self.overwrite_prob_data_set(mh_probs_avg,gibbs_probs_avg,mh_probs_stddev,gibbs_probs_stddev)


class ArithmSampleMhVsGibbs(MhVsGibbs):
    def arithm_sample_mh_vs_gibbs(self):
        self.plot_mh_vs_gibbs_times('arithm_sample mh vs gibbs times avg',
                              'plot_arithm_sample_mh_vs_gibbs_times.png')
        self.plot_mh_vs_gibbs_probs('arithm_sample mh vs gibbs probs avg',
                              'plot_arithm_sample_mh_vs_gibbs_probs.png')

    def arithm_sample_mh_vs_gibbs_avg(self):
        self.mh_vs_gibbs_times_avg()
        self.mh_vs_gibbs_probs_avg()
        self.arithm_sample_mh_vs_gibbs()


class Test33SampleMhVsGibbs(MhVsGibbs):
    def test33_sample_mh_vs_gibbs(self):
        self.plot_mh_vs_gibbs_times('test33_sample mh vs gibbs times avg',
                              'plot_test33_sample_mh_vs_gibbs_times.png')
        self.plot_mh_vs_gibbs_probs('test33_sample mh vs gibbs probs avg',
                              'plot_test33_sample_mh_vs_gibbs_probs.png')

    def test33_sample_mh_vs_gibbs_avg(self):
        self.mh_vs_gibbs_times_avg()
        self.mh_vs_gibbs_probs_avg()
        self.test33_sample_mh_vs_gibbs()


class Test66SampleMhVsGibbs(MhVsGibbs):
    def test66_sample_mh_vs_gibbs(self):
        self.plot_mh_vs_gibbs_times('test66_sample mh vs gibbs times avg',
                              'plot_test66_sample_mh_vs_gibbs_times.png')
        self.plot_mh_vs_gibbs_probs('test66_sample mh vs gibbs probs avg',
                              'plot_test66_sample_mh_vs_gibbs_probs.png')

    def test66_sample_mh_vs_gibbs_avg(self):
        self.mh_vs_gibbs_times_avg()
        self.mh_vs_gibbs_probs_avg()
        self.test66_sample_mh_vs_gibbs()


class Amcmc(Utils):
    def __init__(self, filename, delimiter=','):
        super().__init__(filename, delimiter, 'run_number', 'samples', 'adapt_on_time', 'adapt_on_prob', 'adapt_off_time', 'adapt_off_prob')

    def plot_adapt_on_vs_adapt_off_times(self, plot_title, plot_file):
        plot_frontend(self.data, plot_title, plot_file, ['adapt_on_time','adapt_off_time'], ['adapt_on_time_stddev','adapt_off_time_stddev'], ['adapt_on', 'adapt_off'], 'running time (ms)')

    def plot_adapt_on_vs_adapt_off_probs(self, plot_title, plot_file):
        plot_frontend(self.data, plot_title, plot_file, ['adapt_on_prob','adapt_off_prob'], ['adapt_on_prob_stddev','adapt_off_prob_stddev'], ['adapt_on', 'adapt_off'], 'probability [0,1]')

    def overwrite_avg_data_set(self,adapt_on_times_avg,adapt_off_times_avg,adapt_on_times_stddev,adapt_off_times_stddev):
        self.overwrite_data_set_with_avg(['adapt_on_time', 'adapt_off_time', 'run_number', 'samples', 'adapt_on_time_stddev', 'adapt_off_time_stddev'],
                                    [adapt_on_times_avg, adapt_off_times_avg, sorted(list(set(self.data['run_number']))), sorted(list(set(self.data['samples']))), adapt_on_times_stddev, adapt_off_times_stddev])

    def overwrite_prob_data_set(self,adapt_on_probs_avg,adapt_off_probs_avg,adapt_on_probs_stddev,adapt_off_probs_stddev):
        self.overwrite_data_set_with_avg(['adapt_on_prob', 'adapt_off_prob', 'run_number', 'samples', 'adapt_on_prob_stddev', 'adapt_off_prob_stddev'],
                                    [adapt_on_probs_avg, adapt_off_probs_avg, sorted(list(set(self.data['run_number']))), sorted(list(set(self.data['samples']))), adapt_on_probs_stddev, adapt_off_probs_stddev])

    def adapt_on_vs_adapt_off_times_avg(self):
        avgs = self.compute_avg_and_stddev_two_data_sets(['adapt_on_time','adapt_off_time','adapt_on_prob','adapt_off_prob'],'run_number','samples')
#        adapt_on_times_avg,adapt_off_times_avg,adapt_on_times_stddev,adapt_off_times_stddev = None
#        self.overwrite_avg_data_set(adapt_on_times_avg,adapt_off_times_avg,adapt_on_times_stddev,adapt_off_times_stddev)
        adapt_on_times=print(avgs)
        print('here')

    def adapt_on_vs_adapt_off_probs_avg(self):
        adapt_on_probs_avg,adapt_off_probs_avg,adapt_on_probs_stddev,adapt_off_probs_stddev = self.compute_avg_and_stddev_two_data_sets('adapt_on_prob','adapt_off_prob','run_number','samples')
        self.overwrite_prob_data_set(adapt_on_probs_avg,adapt_off_probs_avg,adapt_on_probs_stddev,adapt_off_probs_stddev)


class Test33CondProbAdaptOnVsAdaptOff(Amcmc):
    def test33_cond_prob_adapt_on_vs_adapt_off(self):
        self.plot_adapt_on_vs_adapt_off_times('test33_cond_prob adapt_on vs adapt_off times avg',
                              'plot_test33_cond_prob_adapt_on_vs_adapt_off_times.png')
        self.plot_adapt_on_vs_adapt_off_probs('test33_cond_prob adapt_on vs adapt_off probs avg',
                              'plot_test33_cond_prob_adapt_on_vs_adapt_off_probs.png')

    def test33_cond_prob_adapt_on_vs_adapt_off_avg(self):
        self.adapt_on_vs_adapt_off_times_avg()
        self.adapt_on_vs_adapt_off_probs_avg()
        self.test33_cond_prob_adapt_on_vs_adapt_off()

def main():
    # This is necessary to save the plot to a file instead of displaying it directly.
    matplotlib.use('Agg')
    # Get the file name from argv. This decides the type of plot.
    file_name=sys.argv[1]
    delimiter=','
    print(file_name)
    if file_name == 'arithm_sample.csv':
        speeds = ArithmSampleMhVsGibbs(file_name,delimiter)
        speeds.arithm_sample_mh_vs_gibbs_avg()
    elif file_name == 'test33_sample.csv':
        speeds = Test33SampleMhVsGibbs(file_name,delimiter)
        speeds.test33_sample_mh_vs_gibbs_avg()
    elif file_name == 'test66_sample.csv':
        speeds = Test66SampleMhVsGibbs(file_name,delimiter)
        speeds.test66_sample_mh_vs_gibbs_avg()
    elif file_name == 'test33_cond_prob.csv':
        speedsA = Test33CondProbAdaptOnVsAdaptOff(file_name,delimiter)
#        speedsA.test33_cond_prob_adapt_on_vs_adapt_off_avg()
        speedsB = Test33SampleMhVsGibbs('test33_sample.csv',delimiter)
        speedsA.adapt_on_vs_adapt_off_times_avg()
        speedsB.mh_vs_gibbs_times_avg()
#        print(speedsA.data)
#        print(speedsB.data)
#        self.plot_adapt_on_vs_adapt_off_times('test33_cond_prob adapt_on vs adapt_off times avg',
#                              'plot_test33_cond_prob_adapt_on_vs_adapt_off_times.png')
        # 1.0. unite the data dictionaries from CondProb and Sample.
        # 1.1. Instead of uniting dicts, fix the compute_avg_and_stddev_two_data_sets func to accepts any number of sets.
        ## https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
        dData = {**speedsA.data, **speedsB.data}
        print(dData)

        Utils.plot_data_sets(dData,
                        'samples',
                        ['adapt_on_time','adapt_off_time', 'mh_time', 'gibbs_time'],
                        ['adapt_on_time_stddev','adapt_off_time_stddev', 'mh_time_stddev', 'gibbs_time_stddev'],
                        ['adapt_on', 'adapt_off', 'mh', 'gibbs'],
                        'u',
                        'samples',
                        'running time (ms)',
                        'testing.png')

        # 2. create a plot interface function that accepts the new dict

if __name__ == '__main__':
    main()
