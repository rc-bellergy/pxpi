#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Echo the information of the Huawei HiLink modems
# Tested on E3372

from __future__ import print_function
import sys
import xmltodict
import requests
import time
import math

def to_size(size):
   if (size == 0):
       return '0 Bytes'
   size_name = ('Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   return '%s %s' % (s,size_name[i])


def is_hilink(device_ip):
    try:
        r = requests.get(url='http://' + device_ip + '/api/device/information', allow_redirects=False, timeout=(2.0,2.0))
    except requests.exceptions.RequestException as e:
        return False;

    if r.status_code != 200:
        return False
    return True

def get_token(device_ip):
    token = None
    try:
        r = requests.get(url='http://' + device_ip + '/api/webserver/SesTokInfo', allow_redirects=False, timeout=(2.0,2.0))
    except requests.exceptions.RequestException as e:
        return token
    try:        
        d = xmltodict.parse(r.text, xml_attribs=True)
        if 'response' in d and 'TokInfo' in d['response']:
            token = d['response']['TokInfo']
            cookie = d['response']['SesInfo']
    except:
        pass
    return (token, cookie)
    

def call_api(device_ip, token, cookie, resource, xml_attribs=True):
    headers = {}
    if token is not None and cookie is not None:
        headers = {'__RequestVerificationToken': token, 'Cookie': cookie}
    try:
        r = requests.get(url='http://' + device_ip + resource, headers=headers, allow_redirects=False, timeout=(2.0,2.0))
    except requests.exceptions.RequestException as e:
        print ("Error: "+str(e))
        return False;

    if r.status_code == 200:
        d = xmltodict.parse(r.text, xml_attribs=xml_attribs)
        if 'error' in d:
            raise Exception('Received error code ' + d['error']['code'] + ' for URL ' + r.url)
        return d            
    else:
      raise Exception('Received status code ' + str(r.status_code) + ' for URL ' + r.url)

def get_connection_status(status):
    result = 'n/a'
    if status == '2' or status == '3' or status == '5' or status == '8' or status == '20' or status == '21' or status == '23' or status == '27' or status == '28' or status == '29' or status == '30' or status == '31' or status == '32' or status == '33':
        result = 'Connection failed, the profile is invalid'
    elif status == '7' or status == '11' or status == '14' or status == '37':
        result = 'Network access not allowed'
    elif status == '12' or status == '13':
        result = 'Connection failed, roaming not allowed'
    elif status == '201':
        result = 'Connection failed, bandwidth exceeded'
    elif status == '900':
        result = 'Connecting'
    elif status == '901':
        result = 'Connected'
    elif status == '902':
        result = 'Disconnected'
    elif status == '903':
        result = 'Disconnecting'
    elif status == '904':
        result = 'Connection failed or disabled'
    return result

def get_network_type(type):
    result = 'n/a'
    if type == '0':
        result = 'No Service'
    elif type == '1':
        result = 'GSM'
    elif type == '2':
        result = 'GPRS (2.5G)'
    elif type == '3':
        result = 'EDGE (2.75G)'
    elif type == '4':
        result = 'WCDMA (3G)'
    elif type == '5':
        result = 'HSDPA (3G)'
    elif type == '6':
        result = 'HSUPA (3G)'
    elif type == '7':
        result = 'HSPA (3G)'
    elif type == '8':
        result = 'TD-SCDMA (3G)'
    elif type == '9':
        result = 'HSPA+ (4G)'
    elif type == '10':
        result = 'EV-DO rev. 0'
    elif type == '11':
        result = 'EV-DO rev. A'
    elif type == '12':
        result = 'EV-DO rev. B'
    elif type == '13':
        result = '1xRTT'
    elif type == '14':
        result = 'UMB'
    elif type == '15':
        result = '1xEVDV'
    elif type == '16':
        result = '3xRTT'
    elif type == '17':
        result = 'HSPA+ 64QAM'
    elif type == '18':
        result = 'HSPA+ MIMO'
    elif type == '19':
        result = 'LTE (4G)'
    elif type == '41':
        result = 'UMTS (3G)'
    elif type == '44':
        result = 'HSPA (3G)'
    elif type == '45':
        result = 'HSPA+ (3G)'
    elif type == '46':
        result = 'DC-HSPA+ (3G)'
    elif type == '64':
        result = 'HSPA (3G)'
    elif type == '65':
        result = 'HSPA+ (3G)'
    elif type == '101':
        result = 'LTE (4G)'
    return result

def get_roaming_status(status):
    result = 'n/a'
    if status == '0':
        result = 'Disabled'
    elif status == '1':
        result = 'Enabled'
    return result

def get_signal_level(level):
    result = '-'
    if level == '1':
        result = u'\u2581'
    if level == '2':
        result = u'\u2581' + u'\u2583'
    if level == '3':
        result = u'\u2581' + u'\u2583' + u'\u2584'
    if level == '4':
        result = u'\u2581' + u'\u2583' + u'\u2584' + u'\u2586'
    if level == '5':
        result = u'\u2581' + u'\u2583' + u'\u2584' + u'\u2586' + u'\u2588'
    return result

def print_traffic_statistics(device_ip, token, cookie, connection_status):
    d = call_api(device_ip, token, cookie, '/api/monitoring/traffic-statistics')
    current_connect_time = d['response']['CurrentConnectTime']
    current_upload = d['response']['CurrentUpload']
    current_download = d['response']['CurrentDownload']
    total_upload = d['response']['TotalUpload']
    total_download = d['response']['TotalDownload']

    if connection_status == '901':
        print('    Connected for: ' + time.strftime('%H:%M:%S', time.gmtime(float(current_connect_time))) + ' (hh:mm:ss)')
        print('    Downloaded: ' + to_size(float(current_download)))
        print('    Uploaded: ' + to_size(float(current_upload)))
    print('  Total downloaded: ' + to_size(float(total_download)))
    print('  Total uploaded: ' + to_size(float(total_upload)))

def print_connection_status(device_ip, token, cookie):
    d = call_api(device_ip, token, cookie, '/api/monitoring/status')
    # print(d['response'])
    connection_status = d['response']['ConnectionStatus']
    signal_strength = d['response']['SignalStrength']
    signal_level = d['response']['SignalIcon']
    network_type = d['response']['CurrentNetworkType']
    roaming_status = d['response']['RoamingStatus']
    # wan_ip = d['response']['WanIPAddress']
    primary_dns_ip = d['response']['PrimaryDns']
    secondary_dns_ip = d['response']['SecondaryDns']
    wifi_status = d['response']['WifiStatus']
    wifi_users_current = d['response']['CurrentWifiUser']
    wifi_users_max = d['response']['TotalWifiUser']

    print('  Connection status: ' + get_connection_status(connection_status))
    public_ip = None
    if connection_status == '901':
        r = requests.get('http://ip.o11.net', timeout=(2.0,2.0))
        if r.status_code == 200:
            public_ip = r.text.rstrip()

        print('    Network type: ' + get_network_type(network_type))
        print('    Signal level: ' + get_signal_level(signal_level).encode('utf-8'), end="")
        if signal_strength is not None:
            print(' (' + signal_strength + '%)')
        else:
            print('')
        print('    Roaming: ' + get_roaming_status(roaming_status))
        # if wan_ip is not None:
        #     print('    Modem WAN IP address: ' +  wan_ip)
        if public_ip is not None:
            print('    Public IP address: ' + public_ip)
        print('    DNS IP addresses: ' + primary_dns_ip + ', ' + secondary_dns_ip)
    if wifi_status == '1':
        print('    WIFI users\t\t' + wifi_users_current + ' (of ' + wifi_users_max + ')')

    return connection_status

def print_device_info(device_ip, token, cookie):
    d = call_api(device_ip, token, cookie, '/api/device/information')
    device_name = d['response']['DeviceName']
    serial_number = d['response']['SerialNumber']
    imei = d['response']['Imei']
    hardware_version = d['response']['HardwareVersion']
    software_version = d['response']['SoftwareVersion']
    webui_version = d['response']['WebUIVersion']
    mac_address1 = d['response']['MacAddress1']
    mac_address2 = d['response']['MacAddress2']
    product_family = d['response']['ProductFamily']
 
    print('Huawei ' + device_name + ' ' + product_family + ' Modem (IMEI: ' + imei + ')')
    print('  Hardware version: ' + hardware_version)
    print('  Software version: ' + software_version)
    print('  Web UI version: ' + webui_version)
    print('  Serial: ' + serial_number)
    print('  MAC address (modem): ' + mac_address1, end='')
    if mac_address2 is not None:
        print('\tMAC address (WiFi): ' + mac_address2)
    else:
        print('')

def print_provider(device_ip, token, cookie, connection_status):
    if connection_status == '901':
        d = call_api(device_ip, token, cookie, '/api/net/current-plmn')
        state = d['response']['State']
        provider_name = d['response']['FullName']
        print('    Network operator: ' + provider_name)

def print_unread(device_ip, token, cookie):
    d = call_api(device_ip, token, cookie, '/api/monitoring/check-notifications')
    unread_messages = d['response']['UnreadMessage']
    if unread_messages is not None and int(unread_messages) > 0:
        print('  Unread SMS: ' + unread_messages)

device_ip = '192.168.1.1'
if len(sys.argv) == 2:
    device_ip = sys.argv[1]
    if not is_hilink(device_ip):
        print("Can't find a Huawei HiLink device on " + device_ip)
        print('')
        sys.exit(-1)
else:
    if not is_hilink(device_ip):
        if not is_hilink('192.168.8.1'):
            print("Can't find a Huawei HiLink device on the default IP addresses, please try again and pass the device's IP address as a parameter")
            print('')
            sys.exit(-1)
        else:
            device_ip = '192.168.8.1'

token, cookie = get_token(device_ip)
print('Token:', token)
print('Cookie:', cookie)
print_device_info(device_ip, token, cookie)
connection_status = print_connection_status(device_ip, token, cookie)
print_provider(device_ip, token, cookie, connection_status)
print_traffic_statistics(device_ip, token, cookie, connection_status)
print_unread(device_ip, token, cookie)
print('')