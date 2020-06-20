import sys

format_dict = {
    "bucket" : "date,D,K,t,e,buckets,eps,run",
    "noisy_bucket" : "date,D,K,t,e,buckets,eps,run",
    "noisy" : "date,D,K,t,e,eps,run",
    "minhash" : "date,D,K,t,e,run",
    "onebit" : "date,D,K,t,e,run",
    "rr": "date,D,K,t,e,eps,run"
    }

fds = {}

mode = "w"
prefix = ""

if len(sys.argv) > 1: 
   for i, arg in enumerate(sys.argv[1:]):
        if arg == "--append":
            mode = "a"
        if arg == "--prefix":
            prefix = sys.argv[i + 2]


for k in format_dict.keys():
    fds[k] = open(prefix + k + ".csv", mode)
    if mode == "w":
        fds[k].write(format_dict[k] + "\n")

with open(sys.argv[-1]) as f:
    for line in f:
        identifier = line.split(",")[0]
        remainder = ",".join(line.split(",")[1:])
        fds[identifier].write(remainder)

for k in fds.keys():
    fds[k].close()

