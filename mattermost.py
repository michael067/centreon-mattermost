#!/usr/bin/env python3

# License : See LICENSE

import argparse
import requests
#import json
#import urllib3
import pprint


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
    template_host = "__{notificationtype}__ {hostalias} is {hoststate}\n{hostoutput}"
    template_service = "__{notificationtype}__ {hostalias} at {hostaddress}/{servicedesc} is {servicestate}\n{serviceoutput}"
    template = template_service if args.servicestate else template_host

    text = emoji(args.notificationtype) + template.format(**vars(args))

    return encode_special_characters(text)


def payload(args):
    payload = {
        "username": args.username,
        "icon_url": args.iconurl,
        "text": text(args)
    }

    if args.channel:
        payload["channel"] = args.channel
        
    if args.username:
        payload["username"] = args.username

    data = "payload=" + json.dumps(payload)
    return data


def request(url, data):
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response.read()


if __name__ == "__main__":
    args = parse()
    response = request(args.url, payload(args))
    print (response)
