#!/bin/bash

echo "Starting up all collectors"


# echo "---------------------------------------------------------"
# echo -e "Starting random collector"
# (exec sh collector.sh random)
# sleep 5
echo "---------------------------------------------------------"
echo -e "Starting Arabic random collector"
./arabicCollector.sh random &
echo "---------------------------------------------------------"
sleep 5
echo "Starting Arabic filter collector 0"
./arabicCollector.sh filter 0 &
echo "---------------------------------------------------------"
sleep 5
echo "Starting Arabic filter collector 1"
./arabicCollector.sh filter 1 &
echo "---------------------------------------------------------"
sleep 5
echo "Starting Arabic filter collector 2"
./arabicCollector.sh filter 2 &
echo "---------------------------------------------------------"
sleep 5
echo "Starting Arabic filter collector 3"
./arabicCollector.sh filter 3 &
echo "---------------------------------------------------------"
sleep 5

echo "Starting Ukraine random collector"
./ukraineCollector.sh random &
echo "---------------------------------------------------------"
sleep 5
echo "Starting Ukraine filter collector 0"
./ukraineCollector.sh filter 0 &
echo "---------------------------------------------------------"
sleep 5
echo "Starting Ukraine filter collector 1"
./ukraineCollector.sh filter 1 &
echo "---------------------------------------------------------"
sleep 5
echo "Starting Ukraine filter collector 2"
./ukraineCollector.sh filter 2 &
echo "---------------------------------------------------------"
sleep 5
echo "Starting Ukraine filter collector 3"
./ukraineCollector.sh filter 3 &
echo "---------------------------------------------------------"
echo

echo "All collectors started"



