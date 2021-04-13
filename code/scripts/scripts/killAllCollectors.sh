#!/bin/bash

echo "killing all Twitterator.py processes"

pkill -f Twitterator.py

# alternatively
#kill $(ps aux | grep '[p]ython3 Twitterator.py' | awk '{print $2}')

