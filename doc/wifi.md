- [Links for WiFi connection](#links-for-wifi-connection)
  - [Command line](#command-line)
  - [Via password file](#via-password-file)
- [For getting into ssh](#for-getting-into-ssh)
  - [Via Device Mode](#via-device-mode)
  - [Via Wifi connection](#via-wifi-connection)

# Links for WiFi connection

- https://unix.stackexchange.com/questions/420640/unable-to-connect-to-any-wifi-with-networkmanager-due-to-error-secrets-were-req
- https://learn.sparkfun.com/tutorials/adding-wifi-to-the-nvidia-jetson/all
- https://unix.stackexchange.com/questions/482207/cannot-connect-to-wifi-with-nmcli-although-secrets-are-provided

## Command line

```
sudo nmcli d wifi connect "YourDog'sTooLoud" password "Spartan$2019"
sudo nmcli d wifi connect "ItHurtsWhenIP" password "Spartan$2019" ifname wlan0
```

## Via password file

```
802-11-wireless-security.psk:secret12345
nmcli con up <connection name> passwd-file <filename>
```

# For getting into ssh

## Via Device Mode

- Micro USB connection
```
ssh user@hostname.local
ssh niket@ubuntu.local
```

## Via Wifi connection

```
ifconfig wlan0

ssh user@192.168.x.y
ssh niket@192.168.1.7
```
