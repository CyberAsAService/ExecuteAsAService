import subprocess
import os
from typing import Any, Dict

from dataclasses import dataclass

os.environ["COMSPEC"] = 'powershell'

@dataclass
class Endpoint:
    """Class representing endpoint."""
    ip_address: str
    username: str
    password: str


# WMI_FORMAT = 'wmic /user:{user} /password:{password} /node:{remote_host} process call create '
# PsExec.exe \\192.168.182.129 -u 192.168.182.129\Witcher -p Switcher -accepteula -h -d powershell "echo falafel>c:\\thishmulik2.png.exe"
# PsExec.exe \\192.168.182.129 -u 192.168.182.129\Witcher -p Switcher -accepteula -h -d powershell "echo falafel > c:\hishmulik2.png.exe "
PSEXEC_FORMAT = './PsExec.exe \\\\{remote_host} -u {remote_host}\\{user} -p {password} -accepteula -h -d cmd /c \'powershell -noninteractive \"[regex]::Escape("&{{command}}") | iex\"\''

#TODO -> GET FROM VARIABLES
def _run_subprocess(remote_host: Endpoint, hash: str, **kwargs) -> subprocess.Popen:
    """
    :param remote_host:
    :param command:
    :return:
    """
    # process_command = "PSEXEC_FORMAT.format(user=remote_host.username,
    #                                        password=remote_host.password,
    #                                        remote_host=remote_host.ip_address,
    #                                        command=command)"
    #print(process_command)

    #$downloadUrl = ''''' + $downloadUrl + ''''';

    command = ["powershell.exe",  '-ExecutionPolicy', 'Unrestricted', "./runner.ps1", "-address",  remote_host.ip_address ,"-username", remote_host.username ,"-password", remote_host.password,"-hash", hash]
    command += ['-arguments', '"' +''.join([f"`${arg} = ''{value}'';" for arg,value in kwargs.items()])+'"']
    print(' '.join(command))
    #print(' '.join(["powershell.exe",  '-ExecutionPolicy', 'Unrestricted', "./runner.ps1", "-address", remote_host.ip_address ,"-username", remote_host.username ,"-password", remote_host.password,"-hash", hash ,"-downloadUrl",  'https://static.toiimg.com/thumb/msid-67586673,width-800,height-600,resizemode-75,imgsize-3918697,pt-32,y_pad-40/67586673.jpg' ,"-output" ,'C:\\this.png']))
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def run_command(remote_host: Endpoint, hash: str, **kwargs) -> Dict[str, str]:
    """
    :param remote_host:
    :param command:
    :return:
    """

    process = _run_subprocess(remote_host, hash, **kwargs)
    res = dict(rc=process.wait(), out=str(process.stdout.read()), err=str(process.stderr.read()), status= "Sent", msg="Sent")
    return res
