import csv
import numpy as np
import pandas as pd

if __name__ == "__main__":
	f = open("RUNS.csv", "w")
	for l in range(2010,2022):
		f.write("--export=ALL,YEAR={:d}\n".format(l))
	f.close()
