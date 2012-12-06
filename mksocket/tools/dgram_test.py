import logging
import logging.handlers
import sys

handler = "local6"

if(len(sys.argv) != 2):
	print "Usage: %s SOCKET - Where SOCKET is full path to a socket" % (sys.argv[0])
	sys.exit(1)

sock = sys.argv[1]

# Temporary workaround or else lighttpd will die when rotating logs..
#syslog = logging.handlers.SysLogHandler(address='/home/holm/code/rsyslog/log2', facility=handler)
try:
	syslog = logging.handlers.SysLogHandler(address=sock, facility=handler)
	formatter = logging.Formatter('%(asctime)s %(filename)s: %(message)s', '%b %e %H:%M:%S')
	syslog.setFormatter(formatter)

	root = logging.getLogger("")
	root.setLevel(logging.INFO)

	root.addHandler(syslog)

	logging.info("Testing the DGRAM socket!")
except Exception as e:
	print "Error with socket '%s': %s" % (sock, e)
