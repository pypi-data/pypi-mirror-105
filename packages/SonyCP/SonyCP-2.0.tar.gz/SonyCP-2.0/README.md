# SonyCP
 
Sony SDCP / PJ Talk projector control 

Python **3** library to query and control Sony Projectors using SDCP (PJ Talk) protocol  over IP.

## Origin
This is a derivative work taken from Guy Shapira. It adds support for changing the lens position and the aspect ratio of the projector. I wish to publicly thank him for this code.

## Features:
* Autodiscover projector using SDAP (Simple Display Advertisement Protocol)
* Query and change power status
* Toggle input between HDMI-1 and HDMI-2
* Change the aspect ratio
* Change the lens position (1.85.1, 2.35.1, custom1, custom2, custom3)

## More features
The SDCP protocol allow to control practically everything in projector, i.e. resolution, brightness, 3d format...
If you need to use more commands, just add to _protocol.py_, and send with _my_projector._send_command__

### Protocol Documnetation:
* [VPL-VW1000ES Protocol Manual](https://www.digis.ru/upload/iblock/eac/VPL-VW1000ES,%20VW1100ES_ProtocolManual.pdf)
* [VW100 Protocol Manual](https://docs.sony.com/release//VW100_protocol.pdf)


### Supported Projectors
Supported Sony projectors should include:
* VPL-VW515
* VPL-VW520
* VPL-VW528
* VPL-VW665
* VPL-VW315
* VPL-VW320
* VPL-VW328
* VPL-VW365
* VPL-VW100
* VPL-VW760ES
* VPL-VW885ES
* VPL-HW65ES

## Installation 
```pip install SonyCP```

## Examples


Sending any command will initiate autodiscovery of projector if none is known and will cary on the command. so just go for it and maybe you get lucky:
```
import SonyCP

my_projector = SonyCP.Projector()

my_projector.get_power()
my_projector.set_power(True)

my_projector.get_picture_position()
my_projector.set_picture_position('2.35.1')
```

get_picture_position() will return a string of where the lens is currently positioned. This is different
than the aspect ratio. Aspect ratio will only change the picture within the current lens setup. So, if
the lens is set to display an image with 1.85.1, then changing the aspect ratio to 2.35.1 will NOT change
the lens, but rather display the image using 2.35.1 within a 1.85.1 lens position. You need to change the
lens to 2.35.1 in order to fill the entire screen.

Skip discovery to save time or if you know the IP of the projector
```
my_known_projector = SonyCP.Projector('10.1.2.3')
my_known_projector.set_HDMI_input(2)
```

# Credits
This modified library is based upon work done by Guy Shapira (pySDCP).
The original code is based on [sony-sdcp-com](https://github.com/vokkim/sony-sdcp-com) NodeJS library by [vokkim](https://github.com/vokkim).


 
