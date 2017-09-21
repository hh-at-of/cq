#!/bin/bash

SCRIPT="start_worker"
CELERY_CONFIG_MODULE="cq.conf.default"
CONCURRENCY=`nproc`

# Use -gt 0 to consume one or more arguments per pass in the loop (e.g.
# some arguments don't have a corresponding value to go with it
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
        echo "usage: ${SCRIPT} [OPTIONS]"
        echo ""
        echo "Start a cq worker on current host $HOST or on hosts given with option -H|--host."
        echo ""
        echo "optional arguments:"
        echo "  -c, --config        set celery config module."
        echo "  -C, --concurrence   set number of worker processes/threads. default: number of CPUs."
        echo "  -d, --daemon        start worker as daemon by current user."
        echo "  -h, --help          show this help message and exit."
        echo "  -H, --hosts HOST,..."
        echo "                      specify hosts as comma separated list where a worker"
        echo "                      should be started. It is needed that current user is"
        echo "                      able to log in the hosts via ssh."
        echo ""
        echo "Written by Hendrik."
        
        exit
    ;;
    -c|--config)
        CELERY_CONFIG_MODULE="$2"
        shift # past argument
    ;;
    -C|--concurrence)
        CONCURRENCY="$2"
        shift # past argument
    ;;
    -d|--daemon)
        echo "option -d|--daemon is not implemented yet."

        exit
    ;;
    -H|--hosts)
        HOSTS="$2"
        shift # past argument
    ;;
    *)
        # unknown option
        echo "unknown option!"
        
        exit
    ;;
esac
shift # past argument or value
done

source {activate_cq_ve_path}

CELERY_CONFIG_MODULE=$CELERY_CONFIG_MODULE celery -A cq worker -c$CONCURRENCY -E --loglevel=info

