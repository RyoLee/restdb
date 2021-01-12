#!/bin/sh
mkdir -p /config
if [ ! -f "/config/restdb.cfg" ];then
    cp /restdb.cfg.sample /config/restdb.cfg
fi
python /restdb.py