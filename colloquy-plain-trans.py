#!/opt/local/bin/python2.7

try:
  from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree

from datetime import datetime
from urlparse import urlparse
from urlparse import parse_qs
import argparse
import sys
import locale
import re

if sys.stdout.isatty():
    default_encoding = sys.stdout.encoding
else:
    default_encoding = locale.getpreferredencoding()

def main(log_file_list):
    for log_file in log_file_list:
        tree = etree.parse(log_file)
        root = tree.getroot()
        source = root.get('source')
        url = urlparse(source)
        qs_dict = parse_qs('a=' + url.path[1:])
        channel = qs_dict['a'][0]
        envelope = root.findall('envelope')
        for e in envelope:
            sender = e.find('sender')
            messages = e.findall('message')
            for m in messages:
                received = m.get('received')
		received = re.sub(r"[+]([0-9])+", "", received)
                dt = datetime.strptime(received, "%Y-%m-%d %H:%M:%S ")
                dt_str = dt.strftime("%Y-%m-%d %H:%M")
                if m.text:
                    print "%s %s %s: %s" % (dt_str, channel, sender.text,
                            m.text.encode(default_encoding))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Display colloquy logs in plain text')
    #parser.add_argument('encoding', metavar='e', type=str, nargs='?',
    #        help='overide the default encoding for the plain text output')
    parser.add_argument('log_file', type=file, nargs='+',
            help='the name of xml based colloquy transcript file')
    args = parser.parse_args()
    main(args.log_file)

