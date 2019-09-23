# Copyright (C) 2013 by Aivars Kalvans <aivars.kalvans@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
import random
import base64
from scrapy import log

ip_list = '''http://66.35.162.175:8080
http://66.96.232.100:3128
http://67.148.156.107:8080
http://38.83.105.194:8118
http://24.205.244.90:7004
http://149.91.81.46:3128
http://15.194.22.136:8088
http://68.38.88.142:8080
http://98.198.18.194:3128
http://146.184.0.116:8080
http://173.234.216.81:8080
http://68.234.201.150:8080
http://50.254.4.194:3128
http://96.82.6.237:3128
http://167.114.195.242:3128
http://74.222.11.146:9000
http://137.135.166.225:8132
http://66.76.179.40:8080
http://12.207.13.21:3128
http://108.5.240.154:80
http://70.254.226.206:8080
http://68.87.73.164:80
http://72.47.105.199:80
http://209.190.64.156:3128
http://73.129.7.140:80
http://40.118.209.103:3128
http://199.48.160.69:3128
http://168.63.24.174:8128
http://108.59.10.135:55555
http://137.135.166.225:8146
http://209.173.8.221:8080
http://206.55.232.198:80
http://137.135.166.225:8137
http://13.91.111.179:3128
http://152.160.35.171:80
http://146.184.0.115:8080
http://168.63.24.174:8145
http://64.62.233.67:80
http://174.37.186.165:3128
http://137.135.166.225:8123
http://13.80.13.253:80
http://158.69.237.1:3128
http://64.30.135.58:56419
http://50.30.152.130:8086
http://67.222.45.31:8080
http://40.118.65.190:80
http://208.47.176.252:80
http://64.20.48.83:8080
http://159.203.80.26:3128
http://149.91.81.46:8080'''

class RandomProxy(object):
    def __init__(self, settings):
        #self.proxy_list = settings.get('PROXY_LIST')
        fin = ip_list

        self.proxies = {}
        for line in fin.split('\n'):
            parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line)

            # Cut trailing @
            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else:
                user_pass = ''

            self.proxies[parts.group(1) + parts.group(3)] = user_pass


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            return

        proxy_address = random.choice(self.proxies.keys())
        proxy_user_pass = self.proxies[proxy_address]

        request.meta['proxy'] = proxy_address
        if proxy_user_pass:
            basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = basic_auth

    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        log.msg('Removing failed proxy <%s>, %d proxies left' % (
                    proxy, len(self.proxies)))
        try:
            del self.proxies[proxy]
        except ValueError:
            pass
        except KeyError:
            pass