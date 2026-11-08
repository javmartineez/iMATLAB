"""
imatlab_benchmark.py

Discrete Mathematics - IMAT
ICAI, Universidad Pontificia Comillas

Description:
Script for measuring the execution time of the IMAT-LAB program.

Usage:
Edit the lists of input and output files to use different
benchmarks.

The main loop contains code to run a timing measurement (benchmarking)
and/or profile the code using each of the provided files.
Comment out either of these lines if you do not want benchmarking or profiling.
"""

import timeit
import cProfile
import imatlab

#Number of repetitions of the timing measurement.
#Increasing it reduces random or incidental effects in the code, but increases the execution cost.
NITERS=100

def testRun(in_file:str, out_file:str):
    """ Wrapper for timeit and profile that opens the provided files
    and runs their commands using the imatlab module.

    Args:
        in_file (str): Name of the input file.
        out_file (str): Name of the output file.

    Returns: Void

    Raises:
        IOError: One of the files does not exist.
    """
    with open(in_file,"r") as fin:
        with open(out_file,"w",encoding="utf-8") as fout:
            imatlab.run_commands(fin,fout)

def measureTime(in_file:str, out_file:str)->float:
    """ Measures the mean execution time of imatlab reading the input from the file
    in_file and saving the output to the file out_file.

    Args:
        in_file (str): Name of the input file.
        out_file (str): Name of the output file.

    Returns:
        float: Measured mean execution time

    Raises:
        IOError: One of the files does not exist.
    """
    t=timeit.Timer("testRun('"+in_file+"','"+out_file+"')","from __main__ import testRun")
    return(t.timeit(number=NITERS)/NITERS)

def profile(in_file:str, out_file:str):
    """ Prints a profile of the execution of imatlab on the input read
    from the file in_file, saving the output to the file out_file.

    Args:
        in_file (str): Name of the input file.
        out_file (str): Name of the output file.

    Returns:
        None

    Raises:
        IOError: One of the files does not exist.
    """
    cProfile.run("testRun('"+in_file+"','"+out_file+"')")



if __name__ == "__main__":
    #Set up the list of input and output files to process
    #Comment out, add or remove files as needed.
    #in_files=["mcdTest.txt"]
    #out_files=["mcdTest_obtained.txt"]
    #in_files=["primosTest.txt","factorTest.txt","mcdTest.txt","potenciaTest.txt","invTest.txt","eulerTest.txt","sistemaTest.txt"]
    #out_files=["primosTest_obtained.txt","factorTest_obtained.txt","mcdTest_obtained.txt","potenciaTest_obtained.txt","invTest_obtained.txt","eulerTest_obtained.txt","sistemaTest_obtained.txt"]
    in_files=["primosTest.txt","factorTest.txt","mcdTest.txt","potenciaTest.txt",
               "invTest.txt","eulerTest.txt","sistemaTest.txt",]
    out_files=["primosTest_obtained.txt","factorTest_obtained.txt","mcdTest_obtained.txt","potenciaTest_obtained.txt",
              "invTest_obtained.txt","eulerTest_obtained.txt", "sistemaTest_obtained.txt"]
    #in_files=["primosTest.txt","factorTest.txt","mcdTest.txt","potenciaTest.txt",
    #            "invTest.txt","eulerTest.txt","cuadraticaTest.txt"]
    #out_files=["primosTest_out.txt","factorTest_out.txt","mcdTest_out.txt","potenciaTest_out.txt",
    #            "invTest_out.txt","eulerTest_out.txt","cuadraticaTest_out.txt"]
    #in_files=["ejemplosComandos.txt"]
    #out_files=["ejemplosSalida.txt"]
    # in_files=["sistemaTest.txt"]
    # out_files=["sistemaTest_out.txt"]
    
    #List of measured times
    runtime=[]
    for i in range(0,len(in_files)):
        #Comment out one line or the other to switch between benchmarking/profiling
        try:
            runtime.append(measureTime(in_files[i],out_files[i]))
            profile(in_files[i],out_files[i])
        except IOError:
            runtime.append(0)
            print("The file "+in_files[i]+" does not exist.\n")

    print(runtime)