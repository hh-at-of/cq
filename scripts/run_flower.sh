#!/bin/bash

SCRIPT="start_flower"
CELERY_CONFIG_MODULE="cq.conf.default"

# Use -gt 0 to consume one or more arguments per pass in the loop (e.g.
# some arguments don't have a corresponding value to go with it
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
        echo "usage: ${{SCRIPT}} [-h --help] [-d,--daemon]"
        echo ""
        echo "Start a flower as a web based tool for monitoring and administration of cq cluster"
        echo ""
        echo "optional arguments:"
        echo "  -c, --config        set celery config module."
        echo "  -d, --daemon        start worker as daemon by current user."
        echo "  -h, --help          show this help message and exit."
        echo ""
        echo "Written by Hendrik."
        
        exit
    ;;
    -d|--daemon)
        echo "option -d|--daemon is not implemented yet."

        exit
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

CELERY_CONFIG_MODULE=$CELERY_CONFIG_MODULE flower -A cq worker

