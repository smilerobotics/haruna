# 2-CH CAN HAT

[Support site](https://www.waveshare.com/wiki/2-CH_CAN_HAT)

## Prepare

Add following line to /boot/firmware/usercfg.txt

```
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=23
```

Then reboot.

Add following liens to /etc/network/interfaces

```
auto can0
iface can0 inet manual
      pre-up /sbin/ip link set $IFACE type can bitrate 1000000
      up /sbin/ip link set $IFACE up
      down /sbin/ip link set $IFACE down
```

Then reboot.

Or, type following command

```
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up
```

### See also

https://www.waveshare.com/wiki/2-CH_CAN_HAT#Preparation

* You don't need to set up can1
* The line `dtparam=spi=on` is not needed in usercfg.txt as long as it is already in config.txt
* You can fix `txqueuelen` with the following command
  * `sudo ip link set can0 txqueuelen 65536`
  * But, it seems to work without this configuration
