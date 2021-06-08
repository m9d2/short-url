#!/bin/bash
pid=`ps -ef | grep uvicorn | grep -v grep | awk '{print $2}'`
if [ -n "$pid" ]
then
  echo "kill -9 pid:" $pid
  kill -9 $pid
fi
nohup /home/ubuntu/.local/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000 > log.log &
