#!/usr/bin/env python3

# License : See LICENSE
# Modify for Centreon and python3 by Michael067
# Version 1.0.0 - 29/04/2020

import argparse
import requests
import json

VERSION = "1.0.0"

def parse():
    parser = argparse.ArgumentParser(description='Sends alerts to Mattermost')
    parser.add_argument('--url', help='Incoming Webhook URL', required=True)
    parser.add_argument('--channel', help='Channel to notify')
    parser.add_argument('--username', help='Username to notify as')
    parser.add_argument('--iconurl', help='URL of icon to use for username',
                        default='https://marketplace.bluemind.net/marketplace/media/avatar/Centreon_Logo_144x144_YYm84WM.png')
    parser.add_argument('--notificationtype', help='Notification Type',
                        required=True)
    parser.add_argument('--hostalias', help='Host Alias', required=True)
    parser.add_argument('--hostaddress', help='Host Address', required=True)
    parser.add_argument('--hoststate', help='Host State')
    parser.add_argument('--hostoutput', help='Host Output')
    parser.add_argument('--servicedesc', help='Service Description')
    parser.add_argument('--servicestate', help='Service State')
    parser.add_argument('--serviceoutput', help='Service Output')
    parser.add_argument('--version', action='version',
                        version='% (prog)s {version}'.format(version=VERSION))
    args = parser.parse_args()
    return args

def encode_special_characters(text):
    text = text.replace("%", "%25")
    text = text.replace("&", "%26")
    return text

def emoji(notificationtype):
    return {
        "RECOVERY": ":white_check_mark: ",
        "PROBLEM": ":fire: ",
        "DOWNTIMESTART": ":clock10: ",
        "DOWNTIMEEND": ":sunny: "
    }.get(notificationtype, "")

def text(args):
    template_host = "__{notificationtype}__ {hostalias} at {hostaddress} is {hoststate}\n{hostoutput}"
    template_service = "__{notificationtype}__ {hostalias} at {hostaddress}/{servicedesc} is {servicestate}\n{serviceoutput}"
    template = template_service if args.servicestate else template_host

    text = emoji(args.notificationtype) + template.format(**vars(args))

    return encode_special_characters(text)

def payload(args):
    data = {
        "icon_url": args.iconurl,
        "text": text(args),
    }

    if args.channel:
        data.update({"channel": args.channel })
        
    if args.username:
        data.update({"username": args.username })

    data = json.dumps(payload)
    return data

if __name__ == "__main__":
    args = parse()
    response = requests.post(args.url, payload(args), {'Content-Type': 'application/json'})
    #print(response)
