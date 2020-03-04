import os
import subprocess

def check_root():
    return os.geteuid() == 0

is_root = check_root()

if is_root:
    proc1 = subprocess.Popen(['ipfs','daemon'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, )
    proc2 = subprocess.Popen(['ipfs-cluster-service', 'daemon'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
else:
    print("Please run script under root")
