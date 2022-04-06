import subprocess, time, psutil

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

proc = subprocess.Popen("./stream.sh", stdout=subprocess.PIPE, shell=True)
print("Start")



try:
    proc.wait(timeout=10)
except subprocess.TimeoutExpired:
    kill(proc.pid)
    print("kill")
