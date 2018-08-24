#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import argparse
import subprocess

n = dict()
n[0] = '$#'
n[1] = '${##}'
n[2] = '$(({n1}<<{n1}))'.format(n1=n[1])
n[3] = '$(({n2}#{n1}{n1}))'.format(n2=n[2], n1=n[1])
n[4] = '$(({n1}<<{n2}))'.format(n2=n[2], n1=n[1])
n[5] = '$(({n2}#{n1}{n0}{n1}))'.format(n2=n[2], n1=n[1], n0=n[0])
n[6] = '$(({n2}#{n1}{n1}{n0}))'.format(n2=n[2], n1=n[1], n0=n[0])
n[7] = '$(({n2}#{n1}{n1}{n1}))'.format(n2=n[2], n1=n[1])

def str_to_oct(cmd):
    """
    Converts a string to its octal representation, enclosed in: $\'STR\'
    """
    s = "$\\'"
    for _ in cmd:
        o = ('%s' % (oct(ord(_)).lstrip('0'))).rjust(3, '0')
        e = '\\\\' + ''.join(n[int(d)] for d in o)
        s += e
    s += "\\'"
    return s

def arg_to_cmd(arg):
    """
    Given an array of strings returns the octal representation of every single string, wrapped in '{}' and separated by ','
    """
    cmd = '{'
    cmd += ','.join(str_to_oct(_) for _ in arg)
    cmd += '}'
    return cmd

def encode(cmd):
    """
    Given a command returns the bashfuck'd version of it
    """
    print('cmd: `{}`'.format(cmd))
    bash = '${!#}'
    tmp = ['bash','-c',cmd]
    payload = "{bash}<<<{cmd}".format(bash=bash,cmd=arg_to_cmd(tmp))
    print('result ({} byte): {}'.format(len(payload), payload))
    return payload

def execute(bashfuck):
    """
    Runs a bashfuck'd command
    """
    p = subprocess.Popen(['/bin/bash','-c',bashfuck])
    p.communicate()    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0],
            description="encode a bash command with charset $,(,),#,!,{,},<,\\,'")
    parser.add_argument('cmd')
    parser.add_argument('-t', '--test', action='store_true', help='test bashfuck and output result')
    args = parser.parse_args()

    if args.test:
        execute(encode(args.cmd))
    else:
        encode(args.cmd)