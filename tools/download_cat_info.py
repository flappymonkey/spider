#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time
import datetime
sys.path.append('../comm_lib')
import utils
def usage(argv0):
    print argv0 + ' type = 1 or 2 filename'
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        usage(sys.argv[0])
        exit(-1)
    type = sys.argv[1]
    filename = sys.argv[2]
    utils.get_cats_info(type, filename)
