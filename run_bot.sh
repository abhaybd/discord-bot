#!/bin/sh
while true
do
	nohup python3 ~/discord_bot/bot.py
	echo 'Running again!'
	sleep 1
done