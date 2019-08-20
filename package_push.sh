#!/bin/sh
python3 main.py $1/$1.json
adb push $1/$1_packed.bin /sdcard/Android/data/com.huami.watch.hmwatchmanager/files/watch_skin_local/138f43a91f311581895aef673ea1c199/138f43a91f311581895aef673ea1c199.bin