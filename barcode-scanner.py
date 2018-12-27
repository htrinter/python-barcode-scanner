from evdev import InputDevice, categorize, ecodes
from datetime import datetime
import calendar

scancodes = {
	11:	u'0',
	2:	u'1',
	3:	u'2',
	4:	u'3',
	5:	u'4',
	6:	u'5',
	7:	u'6',
	8:	u'7',
	9:	u'8',
	10:	u'9'
}
NOT_RECOGNIZED_KEY = u'X'

device = InputDevice('/dev/input/event0') # Replace with your device

barcode = ''

def saveBarcode(bc):
	d = datetime.utcnow()
	unixtime = calendar.timegm(d.utctimetuple())
	
	entry = str(unixtime) + ' ' + bc +  '\n'
	print(entry)
	with open('barcodes.txt', 'a') as bc_file:
		bc_file.write(entry)

for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        eventdata = categorize(event)
	if eventdata.keystate == 1: # Keydown
		scancode = eventdata.scancode
		if scancode == 28: # Enter
			saveBarcode(barcode)
			barcode = ''
		else:
			key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
			barcode = barcode + key
			if key == NOT_RECOGNIZED_KEY:
				print('unknown key, scancode=' + str(scancode))

