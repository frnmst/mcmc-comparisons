#!/bin/bash

# Increase the run label by one. If run_label == task_number we get an error
# for the first task, since a value of 0 would be passed to
# the prolog program. The run label is infact also the number of total
# iterations in tests.pl (if we use the iterative version) so it cannot be
# less than 1.
swipl -s ./prolog/tests 1 10000 1000 $(($1+1)) 1
