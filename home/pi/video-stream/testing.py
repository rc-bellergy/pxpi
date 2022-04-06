import subprocess, time, psutil

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

while True:
    proc = subprocess.Popen("./stream.sh", stdout=subprocess.PIPE, shell=True)
    print("Start")

    time.sleep(5)

    try:
        kill(proc.pid)
        print("kill")
    except:
        print("except")

    time.sleep(5)

