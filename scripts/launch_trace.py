import subprocess, os, sys, signal
import calendar, time


def usage():
    print 'python launch_trace.py app'
    print 'e.g. python launch_trace.py ls -l'

def trace():
    cmdlist = sys.argv[1:]
    print "application command = {0}".format(cmdlist)
    start_time = calendar.timegm(time.gmtime())
    #print "CPU recording start_time: ", start_time
    cpu_logfile = '%s_cpu.log' % str(start_time)
    app_logfile = '%s_app.log' % str(start_time)
    h_app_logfile = open(app_logfile, 'w')

    sp = subprocess.Popen(cmdlist, stdout = h_app_logfile)
    cmd1 = 'python trace_cpu_mem.py -o %s -p %d' % (cpu_logfile, sp.pid)
    print cmd1
    cmdlist1 = cmd1.split()
    sp1 = subprocess.Popen(cmdlist1)

    print "Waiting...."
    print "Application return code:", sp.wait()

    sp1.send_signal(signal.SIGTERM)
    print "Tracing return code:", sp1.wait()

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        usage()
        sys.exit(1)
    trace()
