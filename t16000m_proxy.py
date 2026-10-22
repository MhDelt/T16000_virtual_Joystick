#!/usr/bin/env python3
import evdev
from evdev import UInput, AbsInfo, ecodes as e

SRC_NAME = "T.16000M"
OUT_MIN, OUT_MAX = -32767, 32767
AXES = [e.ABS_X, e.ABS_Y, e.ABS_RZ, e.ABS_THROTTLE]  # Axes
HATS = [e.ABS_HAT0X, e.ABS_HAT0Y]


src = None
for path in evdev.list_devices():
    d = evdev.InputDevice(path)
    if SRC_NAME in d.name:
        src = d
        break
if src is None:
    raise SystemExit("Can't find T.16000M")

caps = src.capabilities()
src_abs = {code: info for code, info in caps.get(e.EV_ABS, [])}
buttons = caps.get(e.EV_KEY, [])

abs_caps = []
for code in AXES:
    if code in src_abs:
        abs_caps.append((code, AbsInfo(0, OUT_MIN, OUT_MAX, 0, 0, 0)))
for code in HATS:
    if code in src_abs:
        abs_caps.append((code, AbsInfo(0, -1, 1, 0, 0, 0)))

ui = UInput({e.EV_KEY: buttons, e.EV_ABS: abs_caps},
            name="Virtual Joystick", vendor=0x1234, product=0x5678)

def scale(code, v):
    i = src_abs[code]
    return (v - i.min) * (OUT_MAX - OUT_MIN) // (i.max - i.min) + OUT_MIN

src.grab()  # Original device is signalling here and not to other software
print("Running. Ctrl+C to stop.")
try:
    for ev in src.read_loop():
        if ev.type == e.EV_ABS and ev.code in AXES and ev.code in src_abs:
            ui.write(e.EV_ABS, ev.code, scale(ev.code, ev.value))
        elif ev.type == e.EV_ABS and ev.code in HATS:
            ui.write(e.EV_ABS, ev.code, ev.value)
        elif ev.type == e.EV_KEY:
            ui.write(e.EV_KEY, ev.code, ev.value)
        elif ev.type == e.EV_SYN:
            ui.syn()
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    src.ungrab()
    print("\nUngrabbed...")
    ui.close()
    print("\nStopped")
