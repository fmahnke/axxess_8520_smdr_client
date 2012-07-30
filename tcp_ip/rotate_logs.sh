#!/bin/bash

# Log file
today=$(date +%F)
log_path=/home/fritz/cgs_phones
log_file_name=phone_log_$today

# pid file
pid_file=/tmp/axxess_client.pid

# Client program
program_path=/home/fritz/axxess_8520_smdr_client/tcp_ip

# Kill old process if it exists
if [ -e $pid_file ]
then
    pid=$(cat $pid_file)
    kill $pid
fi

# Launch new process
cd $program_path
$program_path/axxess_8520_smdr_client.py $log_path/$log_file_name &

# Write pid file
pid=$!
echo $pid > $pid_file

