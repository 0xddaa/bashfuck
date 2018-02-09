#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from pwn import *
import argparse

n = dict()
n[0] = '$#'
n[1] = '${##}'
n[2] = '$(({n1}<<{n1}))'.format(n1=n[1])
n[3] = '$(({n2}#{n1}{n1}))'.format(n2=n[2], n1=n[1])
n[4] = '$(({n2}#{n1}{n0}{n0}))'.format(n2=n[2], n1=n[1], n0=n[0])
n[5] = '$(({n2}#{n1}{n0}{n1}))'.format(n2=n[2], n1=n[1], n0=n[0])
n[6] = '$(({n2}#{n1}{n1}{n0}))'.format(n2=n[2], n1=n[1], n0=n[0])
n[7] = '$(({n2}#{n1}{n1}{n1}))'.format(n2=n[2], n1=n[1])

def split(cmd):
    argv = []
    token = ''
    quote = False
    for c in cmd:
        if c == ' ' and not quote:
            argv.append(token)
            token = ''
        elif c == '\'':
            quote = not quote
        else:
            token += c
    argv.append(token)
    return argv

def str_to_oct(cmd):
    s = "$\\'"
    for _ in cmd:
        o = ('%s' % (oct(ord(_)).lstrip('0'))).rjust(3, '0')
        e = '\\\\' + ''.join(n[int(d)] for d in o)
        s += e
    s += "\\'"
    return s

def arg_to_cmd(arg):
    cmd = '{'
    cmd += ','.join(str_to_oct(_) for _ in arg)
    cmd += ',}'
    return cmd

def encode(cmd):
    log.info('cmd: `{}`'.format(cmd))
    bash = '${!#}'
    cmd = "bash -c '{}'".format(cmd)
    exp = "%s<<<%s" % (bash, arg_to_cmd(split(cmd)))
    log.info('result: ' + exp)
    return exp

def execute(bashfuck):
    with context.local(log_level='ERROR'):
        r = process('/bin/bash')
    r.sendline(bashfuck)
    r.sendline('echo GGGGGGGG; exit')
    log.info(r.recvuntil('GGGGGGGG', drop=True).strip())
    with context.local(log_level='ERROR'):
        r.close()


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
