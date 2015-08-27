import subprocess, os, sys, signal, time

def usage():
    print 'python launch_trace.py scripts logs app'
    print 'e.g. python launch_trace.py /usr/bin ls -l'

def trace():
    # Get command line arguments
    script_dir = sys.argv[1]
    log_dir = sys.argv[2]
    command_application = sys.argv[3]

    # Start timing
    start_time = time.strftime("%Y-%m-%d_%H:%M:%S")

    # Open log files
    cpu_logfile = '%s/%s_cpu.log' % (log_dir, str(start_time))
    app_logfile = '%s/%s_app.log' % (log_dir, str(start_time))
    h_app_logfile = open(app_logfile, 'w')

    # Start application
    print "Starting application: \"", command_application, "\""
    sp_application = subprocess.Popen(command_application, stdout = h_app_logfile, stderr = h_app_logfile)

    # Start tracing
    command_tracing = 'python %s/trace_cpu_mem.py -o %s -p %d' % (script_dir, cpu_logfile, sp_application.pid)
    print "Starting tracing: \"", command_tracing, "\""
    command_tracing = command_tracing.split()
    sp_tracing = subprocess.Popen(command_tracing)

    # Wait for application to finish
    print "Waiting for application to finish..."
    return_code_application = sp_application.wait()
    print "Application return code: ", return_code_application

    # End tracing
    sp_tracing.send_signal(signal.SIGTERM)
    return_code_tracing = sp_tracing.wait()
    print "Tracing return code: ", return_code_tracing

if __name__ == '__main__':
    if (len(sys.argv) < 4):
        usage()
        sys.exit(1)
    trace()
