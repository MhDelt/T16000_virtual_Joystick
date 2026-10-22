# T16000_virtual_Joystick
T16000 virtual joystick proxy for Proton

Made it for myself to play Microsoft Flight Simulator X under Linux using Thrustmaster T16000M HOTAS

Problem was that MFSX did not correctly assigned analog axies from joystick.

## How to use

Use `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x044F/0xB10A PROTON_ENABLE_HIDRAW=0` in a Launch Options to hide original T16000M controller from a game.
Then start a script with `python3 t16000m_proxy.py` from a terminal.
Dont close terminal while playing.
Virtual Joystick should appear in settings.

