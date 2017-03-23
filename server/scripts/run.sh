#!/bin/sh

mkdir /tmp/edgetracetmp

python3.5 analyzelog.py 0
python3.5 plotlog.py
python3.5 mapplotlog.py

rm /tmp/edgetracetmp/*
rmdir /tmp/edgetracetmp
