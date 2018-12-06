#!/usr/bin/env bash

# TODO FIXME

pushd "./amcmc/xsb"
xsb -e "compile('startup_experiments.P'),halt."
xsb startup_experiments
popd
