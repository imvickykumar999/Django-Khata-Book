## Connect mobile via USB to laptop

```bash
C:\Users\surface>adb tcpip 5555
restarting in TCP mode port: 5555

C:\Users\surface>adb devices
List of devices attached
RZ8N60JN0EE     device
```

## Unplug USB

```bash
C:\Users\surface>adb connect 192.168.0.107
connected to 192.168.0.107:5555

C:\Users\surface>scrcpy
scrcpy 2.3.1 <https://github.com/Genymobile/scrcpy>
INFO: ADB device found:
INFO:     --> (tcpip)    192.168.0.107:5555            device  SM_A217F
C:\Users\surface\Documents\GitHub\scrcp...pped. 48.3 MB/s (66007 bytes in 0.001s)
[server] INFO: Device: [samsung] samsung SM-A217F (Android 12)
INFO: Renderer: direct3d
INFO: Texture: 720x1600
WARN: Killing the server...
```
