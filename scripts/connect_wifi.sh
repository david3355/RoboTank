#!/bin/bash

# 1st parameter: Wifi SSID
# 2nd parameter: Wifi Password (8-63 character!)
# If Wifi SSID is not found in saved networks, it will be saved
# If Wifi SSID is found in saved networks and password is provided, saved network will be overridden, and new password will be saved
# Hint: check connected network: iwgetid

wifi_ssid=$1
wifi_pwd=$2

interface=wlan0
wifis=/home/pi/wifi_networks/
wpa_conf=/etc/wpa_supplicant/wpa_supplicant.conf
wpa_template=wpa_conf_template

found=0
for i in "$wifis"*
do
  f=$(basename "$i")
  if [ "$f" == "$wifi_ssid" ] ; then
    found=1
  fi
done

if [ $found -eq 0 ] && [ ${#wifi_pwd} -lt 8 ] ; then
  echo "New connection! Password must be at least 8 characters!"
  exit
fi

if [ $found -eq 0 ] || [ ${#wifi_pwd} -ge 8 ] ; then
  wpa_passphrase "$wifi_ssid" "$wifi_pwd" > "$wifis$wifi_ssid"
fi

cat $wpa_template > $wpa_conf
cat "$wifis$wifi_ssid" >> $wpa_conf


wpa_cli -i $interface reconfigure