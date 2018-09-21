#!/usr/bin/env bash
ssh xs.vc
cd ~/portfolio-django
git pull
cp portfolio/ ~/shaneleblancnet/
cp static/ ~/shaneleblancnet/
cp content/ ~/shaneleblancnet/
