##!/bin/python

import getopt
import math
import random
import subprocess
import sys
import timeit

# still have that problem!  Have to import things more than once for
# this work.
import decimal
from decimal import Decimal

class RuntimeOptions(object):

    def __init__(self):
        # set options here so they can be accessed.
        self.data_size_option             = False
        self.operations_per_second_option = False
        self.number_of_processor_option   = False
        self.just_show_expected           = False

    def show_help(self):
        print "Comparing expected O(n) running time to actual time taken."
        print "\nOptions:"
        print "-n <data_size>             --  Size of data to test, default is 1000"
        print "-o <operations_per_second>  -- default is 10000"
        print "-p <processor count>        -- default is actual number of cpu of computer"

    def commands(self, argv):
        try:
            opts, args = getopt.getopt(argv, "hn:o:p:e",
                                       ["help","datasize=","operations=", "processors=","expected"])
        except getopt.GetoptError:
            self.show_help()
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.show_help()
                sys.exit()

            elif opt in ("-n", "--datasize"):
                self.data_size_option = arg

            elif opt in ("-o", "--operations"):
                self.operations_per_second_option = arg

            elif opt in ("-p", "--processors"):
                self.number_of_processor_option = arg

            elif opt in ("-e", "--expected"):
                self.just_show_expected = True


def printSeperator(cmd):

    if cmd.just_show_expected == True:
        length = 30
    else:
        length = 46

    separator = "=-"*length+"="
    print separator

# the usual suspects of O(n), leaving out the heavy weights
def functionValue(fn, n):
    functions = [math.log(n, 2), math.sqrt(n), n, n*math.log(n,2), n*n, n*n*n]
    return functions[fn]

# Since we want to compare how long O(fn) lasts, it's all the same if
# our simulation runs fn operations.
def functionSimulator(fn, n):
    count = 0
    times = functionValue(fn, n)
    while count < times:
         count += 1
    return times


def main(argv):

    ## Precision setting for the Decimal module.  Not sure if 10 is
    ## good, but it's worth trying.
    decimal.getcontext().prec = 10

    # extract and reverse output of /proc/cpuinfo
    tmp    = subprocess.check_output(["cat", "/proc/cpuinfo"])
    tmp2   = tmp.splitlines()
    output = tmp2[::-1]

    # grab the bogomips values, there's one for each processors
    bogo_list = [x for x in output if 'bogomips' in x]
    bogomips   = int(float(bogo_list[0].split()[2]))

    # apply the user options if any
    cmd = RuntimeOptions()
    cmd.commands(argv)

    if cmd.number_of_processor_option == False:
        number_of_processors = len(bogo_list)
    else:
        number_of_processors = int(cmd.number_of_processor_option)

    if cmd.operations_per_second_option == False:
        operations_per_second = 10000
    else:
        operations_per_second = int(cmd.operations_per_second_option)

    if cmd.data_size_option == False:
        data_size = 1000
    else:
        data_size = int(cmd.data_size_option)

    # Our best guess as to real operations per second
    mips = number_of_processors * operations_per_second * bogomips

    printSeperator(cmd)

    print "Your computer:  %d processors @ %d bogomips\n"\
           "                data size    = %d\n"\
           "                operations/s = %d\n"\
           "                guessed MIPS = %d\n"% (
            number_of_processors, bogomips, data_size,
               operations_per_second, mips)


    functionName = ["lg n","sqrt of n", "n","n lg n","n^2","n^3"]


    if cmd.just_show_expected == False:

        print "Function      Expected Time    Actual Time      Difference     Percentage      Operations\n"\
              "------------------------------------------------------------------------------------------"
        for f in range(0, len(functionName)):
            expectedTime = Decimal(functionValue(f, data_size))/mips

            start_time = timeit.default_timer()
            times = functionSimulator(f, data_size)
            actualTime = timeit.default_timer() - start_time

            timeDifference = abs(expectedTime - Decimal(actualTime))

            percentage = timeDifference/Decimal(actualTime)

            print " %-11s  %11g      %11g\t%-11g\t%-3g \t%10d " % (
                functionName[f],
                expectedTime,
                actualTime,
                timeDifference,
                percentage,
                times)
    else:
        print "Function      Expected Time    Operations\n"\
              "---------------------------------------------"
        for f in range(0, 6):
            expectedTime = Decimal(functionValue(f, data_size))/mips

            print " %-11s  %11g \t%10d " % (
                functionName[f],
                expectedTime,
                functionValue(f, data_size))


    printSeperator(cmd)

if __name__ == '__main__':
    main(sys.argv[1:])
