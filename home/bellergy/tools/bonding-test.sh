#! /bin/sh

echo "Slaves = $(cat /sys/class/net/bond0/bonding/slaves)"
echo "Primary = $(cat /sys/class/net/bond0/bonding/primary)"
echo "Active Slave = $(cat /sys/class/net/bond0/bonding/active_slave)"

r=$(pidof dhclient)
test -n "$r" && ps $r

r=$(pidof wpa_supplicant)
test -n "$r" && ps $r
