# split up the log file produced by exp_artificial.py
import sys

format_dict = {
    "bucket" : "date,D,K,t,e,bf,buckets,sparsity,eps,run",
    "noisy" : "date,D,K,t,e,scale,run",
    "minhash" : "date,D,K,t,e,run",
    "onebit" : "date,D,K,t,e,run"
    }

fds = {}

for k in format_dict.keys():
    fds[k] = open(k + ".csv", "w")
    fds[k].write(format_dict[k] + "\n")

with open(sys.argv[1]) as f:
    for line in f:
        identifier = line.split(",")[0]
        remainder = ",".join(line.split(",")[1:])
        fds[identifier].write(remainder + "\n")

for k in fds.keys():
    fds[k].close()

