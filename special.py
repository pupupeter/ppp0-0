#!/usr/bin/env python3
import sys
import subprocess

def rstrip(s):
	while s and (s[-1] == '\r' or s[-1] == '\n'): s = s[:-1]
	return s


def run_command(command):
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	return stdout

def PSNR(fna,fnb):
	cmd = ['python', 'psnr.py',fna,fnb]

	psnr = float(run_command(cmd))
	return psnr

	
def SSIM(fna,fnb):
	cmd = ['python', 'ssim.py',fna,fnb]
	ssim = float(run_command(cmd))
	return ssim


if __name__=="__main__":
	fa, fb = open(sys.argv[2],encoding='utf-8'), open(sys.argv[3],encoding='utf-8')
	while True:
		la, lb = fa.readline(), fb.readline()
		if la:
			if not lb or rstrip(la) != rstrip(lb): quit(1)
		elif lb:
			quit(1)
		else:
			break


