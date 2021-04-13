#!/bin/bash

until python tangotwitterspy.py -k isil_keywords_2.txt -kq uscc0-node02.uncharted.software -kt isis -a RobH2; do
    python sendalert.py "API ERROR: [Amazon Linux EC2] ISIS 2 ERROR"
    echo "Crashed with exit code $?. Restarting..." >&0
    sleep 30
done

echo "API ERROR DETECTED.  Restarting in 30 Seconds."

python sendalert.py "API ERROR: [Amazon Linux EC2] ISIS 2 ERROR"

sleep 30

bash isis2.sh

#n.b. the exit code portion doesn't seem to work...
