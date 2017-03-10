#!/usr/bin/env python3
# vim: set noexpandtab:

import zlib
import tarfile
import io
import sys
import subprocess
import argparse
from xml.etree import ElementTree
import json
import struct
from base64 import b32encode
from urllib.parse import urlencode, quote
from collections import OrderedDict

def main():
	p = argparse.ArgumentParser(
			description="Extracts OTP configurations (including secrets) "
			"from an Android backup of FreeOTP")
	p.add_argument('backupfile', nargs='?', type=argparse.FileType('rb'),
			help="Backup file to extract configurations from "
			"(default: call adb and dump from a connected phone directly)")

	args = p.parse_args()
	input_file = args.backupfile

	if not input_file:
		# Push the backup data through stderr because adb prints text to stdout
		cp = subprocess.run(
				['adb', 'backup', '-f', '/dev/stderr', 'org.fedorahosted.freeotp'],
				stderr=subprocess.PIPE, stdout=sys.stderr)
		input_file = io.BytesIO(cp.stderr)

	# Skip android backup header
	input_file.seek(24)

	# Open zlib-compressed tar file
	uncompressed_data = zlib.decompress(input_file.read())
	tar = tarfile.open(fileobj=io.BytesIO(uncompressed_data))

	xmlf = tar.extractfile("apps/org.fedorahosted.freeotp/sp/tokens.xml")
	et = ElementTree.parse(xmlf)
	tokens = {}
	for item in et.findall("./string"):
		name = item.get('name')
		content = json.loads(item.text)
		if name == "tokenOrder":
			token_order = content
			continue
		tokens[name] = build_uri(content)
	
	assert len(tokens) == len(token_order)
	
	for name in token_order:
		print(tokens[name])

def build_uri(j):
	params = OrderedDict()

	type = j['type'].lower()
	if type == 'totp':
		if j['period'] != 30:
			params['period'] = j['period']
	elif type == 'hotp':
		params['counter'] = j['counter']
	else:
		raise ValueError("Invalid OTP type {}".format(type))

	secret = j['secret']
	secret = struct.pack("{}b".format(len(secret)), *secret)
	params['secret'] = b32encode(secret).strip(b'=').decode('ascii')

	if len(j.get('issuerInt', '')) > 0:
		params['issuer'] = j['issuerInt']

	label = j['label']
	if len(j.get('issuerAlt', '')) > 0:
		# Use customized label, if specified
		label = "{}:{}".format(j['issuerAlt'], label)
	elif len(j.get('issuerExt', '')) > 0:
		label = "{}:{}".format(j['issuerExt'], label)
	
	if j['algo'] != 'SHA1':
		params['algorithm'] = j['algo']
	
	if j['digits'] != 6:
		params['digits'] = j['digits']
	
	if 'image' in j:
		params['image'] = j['image']
	
	uri = "otpauth://{type}/{label}?{params}".format(
			type=type,
			label=quote(label),
			params=urlencode(params)
		)

	return uri

if __name__ == "__main__":
	main()
