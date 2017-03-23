#-*- coding:utf-8 -*-

import os
import argparse

def replaceName(src, dst):
	count = 0

	for f in os.listdir("."):
		if src in f:
			count += 1
			os.rename(f, f.replace(src, dst))

	if count > 0:
		print "%d files renamed " % count
	else:
		print "Nothing to rename !"

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Python renaming tool')
	parser.add_argument('--src', default='', type=str)
	parser.add_argument('--dst', default='', type=str)
	args = parser.parse_args()

	if not args.src:
		print "[Err] Arguments error, must specify what to rename !"
	else:
		print "Rename files that contain '%s' to '%s'" % (args.src, args.dst)
		replaceName(args.src, args.dst)
