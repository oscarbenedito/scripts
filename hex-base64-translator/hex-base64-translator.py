#!/usr/bin/env python3
# Copyright (C) 2020 Oscar Benedito
#
# This file is part of Utilities.
#
# Utilities is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Utilities is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Utilities.  If not, see <https://www.gnu.org/licenses/>.

import sys
from getpass import getpass

def char_to_bits(c):
    n = ord(c)
    if n >= 65 and n <= 90:
        return bin(n - 65)[2:].zfill(6)
    elif n >= 97 and n <= 122:
        return bin(n - 71)[2:].zfill(6)
    elif n >= 48 and n <= 57:
        return bin(n + 4)[2:].zfill(6)
    elif (c == '+'):
        return bin(62)[2:].zfill(6)
    elif (c == '/'):
        return bin(63)[2:].zfill(6)
    else:
        sys.exit('Error, ' + c + ' is not a Base64 character.', file=sys.stderr)

def bits_to_char(s):
    n = int(s, 2)
    if n < 26:
        return chr(n + 65)
    elif n < 52:
        return chr(n + 71)
    elif n < 62:
        return chr(n - 4)
    elif n == 62:
        return '+'
    elif n == 63:
        return '/'
    else:
        sys.exit('Error, ' + s + ' (' + str(n) + ') is not a binary number lower than 64.', file=sys.stderr)

def base64_to_hex(s):
    if len(s) % 2:
        print('WARNING: Number of Base64 characters is not multiple of 2. Adding zeros to string.', file=sys.stderr)
        s = 'A' + s

    ret = ''
    carry = ''
    while len(s) > 0:
        cs = s[:2]
        bs = char_to_bits(s[0]) + char_to_bits(s[1])
        ret += hex(int(bs, 2))[2:].zfill(3)
        s = s[2:]

    return ret

def hex_to_base64(s):
    if len(s) % 3:
        print('WARNING: Number of hexadecimal values is not a multiple of 3. Adding zeros to string.', file=sys.stderr)
        s = '0'*(3 - (len(s) % 3)) + s

    ret = ''
    while len(s) > 0:
        bs = bin(int(s[:3], 16))[2:].zfill(12)
        ret += bits_to_char(bs[:6])
        ret += bits_to_char(bs[6:])
        s = s[3:]

    return ret


if len(sys.argv) != 2 or (sys.argv[1] != 'base64-to-hex' and sys.argv[1] != 'hex-to-base64'):
    sys.exit('Usage: ' + sys.argv[0] + ' base64-to-hex | hex-to-base64.')

if sys.argv[1] == 'base64-to-hex':
    inp = getpass(prompt = 'Base64 secret: ')
    print('')
    out = base64_to_hex(inp)
    print('-'*80)
    print('Secret in hexadecimal:', out)
    print('-'*80)

elif sys.argv[1] == 'hex-to-base64':
    inp = getpass(prompt = 'Hexadecimal secret: ')
    print('')
    out = hex_to_base64(inp)
    print('-'*80)
    print('Secret in Base64:', out)
    print('-'*80)
    if inp[0] == '0' and len(inp) % 2 == 0:
        out = hex_to_base64(inp[1:])
        print('-'*80)
        print('Due to SSSS having an output with an even number of characters, your secret could be:', out)
        print('-'*80)