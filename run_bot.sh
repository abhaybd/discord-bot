#!/bin/sh
while true
do
	python3 ~/discord_bot/bot.py>&1
	if [ $? = 0 ]; then
		break
	else
		echo "Running again!">&2
		sleep 1
	fi
done