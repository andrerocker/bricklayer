#!/bin/bash
#
### BEGIN INIT INFO
# Provides:		bricklayer
# Required-Start:	$network $local_fs $remote_fs
# Required-Stop:	$network $local_fs $remote_fs
# Should-Start:		$network
# Should-Stop:		$network
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:	start and stop Bricklayer Package Builder
# Description:		The Bricklayer Package Builder builds packages to
# 			help you automate builds and upload packages to repositories.
### END INIT INFO

PATH=/usr/bin:/usr/sbin:/bin:/sbin
DAEMON=/usr/bin/twistd
RUNDIR=/var/run
PIDFILE=/var/run/bricklayer.pid
TACFILE=/etc/bricklayer/bricklayer.tac
LOGFILE=/var/log/bricklayer.log

CONSUMER=/usr/bin/build_consumer
CONSUMER_PIDFILE=/var/run/build_consumer.pid
CONSUMER_LOGFILE=/var/log/build_consumer.log

# Include bricklayer defaults if available
if [ -r /etc/default/bricklayer ]; then
	. /etc/default/bricklayer
fi

test -x ${DAEMON} || exit 0
test -r ${TACFILE} || exit 0

case "$1" in
  start)
	echo -n "Starting bricklayer"
	${DAEMON} -y ${TACFILE} --pidfile=${PIDFILE} -l /var/log/bricklayer.log 2>&1 > /dev/null &
	PYTHONPATH=/usr/share/pyshared/bricklayer/utils twistd -y /usr/share/pyshared/bricklayer/rest.py -l /var/log/bricklayer-rest.log
    	start-stop-daemon --start --quiet --exec ${CONSUMER} --pidfile ${CONSUMER_PIDFILE}.1 -b 
    	start-stop-daemon --start --quiet --exec ${CONSUMER} --pidfile ${CONSUMER_PIDFILE}.2 -b 
    	start-stop-daemon --start --quiet --exec ${CONSUMER} --pidfile ${CONSUMER_PIDFILE}.3 -b 
	echo "."	
	;;
  stop)
	echo -n "Stopping bricklayer"
	ps aux | grep twistd | grep -v grep | awk '{print $2}' | xargs kill -9
	ps aux | grep build_consumer | grep -v grep | awk '{print $2}' | xargs kill -9
	rm /var/run/bricklayer.sock
	echo "."
	;;
  restart)
	${0} stop
	sleep 1
	${0} start
	;;
  force-reload)
	${0} restart
	;;
  *)
	echo "Usage: ${0} {start|stop|restart|force-reload}" >&2
	exit 1
	;;
esac

exit 0

