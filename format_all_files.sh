#!/usr/bin/env zsh

autopep8 --in-place --aggressive --aggressive --recursive .
black -l 79 --experimental-string-processing .
autopep8 --in-place --aggressive --aggressive --recursive .