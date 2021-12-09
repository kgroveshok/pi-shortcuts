#!/bin/sh

# https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/

#echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
#echo "dwc2" | sudo tee -a /etc/modules
#echo "libcomposite" | sudo tee -a /etc/modules
#https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-setup-and-device-definition/

#

cat <<EOF >/home/pi/usbhid.sh
#!/bin/bash
#https://stackoverflow.com/questions/66393757/using-pi-zero-w-to-simulate-hid-keyboard-and-mouse
cd /sys/kernel/config/usb_gadget/
mkdir -p isticktoit
cd isticktoit
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
#echo 0x1d6b > idVendor # Linux Foundation
#echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x2341 > idVendor # pretend leonardo
echo 0x8036 > idProduct # pretend leonardo
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "pi zero w HID" > strings/0x409/manufacturer
echo "iSticktoit.net USB Device" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower
# Add functions here
# see gadget configurations below
# End functions

# Add functions here
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length

echo -ne \\x05\\x01\\x09\\x06\\xA1\\x01\\x85\\x01\\x05\\x07\\x19\\xE0\\x29\\xE7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xC0\\x05\\x01\\x09\\x02\\xA1\\x01\\x09\\x01\\xA1\\x00\\x85\\x02\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x81\\x25\\x7F\\x75\\x08\\x95\\x02\\x81\\x06\\xC0\\xC0 > functions/hid.usb0/report_desc


ln -s functions/hid.usb0 configs/c.1/
# End functions

echo 0x80 > configs/c.1/bmAttributes
echo 200 > configs/c.1/MaxPower # 200 mA


ls /sys/class/udc > UDC

chown pi /dev/hidg0
sleep 3
EOF

chmod +x /home/pi/usbhid.sh


