#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os, sys
import re
import binascii
import argparse
import fileinput

__author__ = "Tim Gray"
__version__ = "1.0"

fixed = {"CLX": "77",
    "ENTER": "83",
    "X<>Y": "71",
    "R↓": "75",
    "+/-": "54",
    "±": "54",
    "/": "43",
    "÷": "43",
    # "x": "42",
    "×": "42",
    "-": "41",
    "+": "40",
    "LASTX": "76",
    "SIN": "59",
    "COS": "5A",
    "TAN": "5B",
    "ASIN": "5C",
    "ACOS": "5D",
    "ATAN": "5E",
    "LOG": "56",
    "10^X": "57",
    "10↑X": "57",
    "LN": "50",
    "E^X": "55",
    "E↑X": "55",
    "SQRT": "52",
    "X^2": "51",
    "X↑2": "51",
    "1/X": "60",
    "1÷X": "60",
    # "Y^X": "53",
    "Y↑X": "53",
    "%": "4C",
    "PI": "72",
    "COMPLEX": "A0 72",
    "ALL": "A2 5D",
    "NULL": "00",
    "CLA": "87",
    "DEG": "80",
    "RAD": "81",
    "GRAD": "82",
    "RECT": "A2 5A",
    "POLAR": "A2 59",
    "CPXRES": "A2 6A",
    "REALRES": "A2 6B",
    "KEYASN": "A2 63",
    "LCLBL": "A2 64",
    "RDX.": "A2 5B",
    "RDX,": "A2 5C",
    "CLΣ": "70",
    "CLST": "73",
    "CLRG": "8A",
    "CLKEYS": "A2 62",
    "CLLCD": "A7 63",
    "CLMENU": "A2 6D",
    # "->DEG": "6B",
    # "->RAD": "6A",
    # "->HR": "6D",
    # "->HMS": "6C",
    # "->REC": "4E",
    # "->POL": "4F",
    "→DEG": "6B",
    "→RAD": "6A",
    "→HR": "6D",
    "→HMS": "6C",
    "→REC": "4E",
    "→POL": "4F",
    "IP": "68",
    "FP": "69",
    "RND": "6E",
    "ABS": "61",
    "SIGN": "7A",
    "MOD": "4B",
    "COMB": "A0 6F",
    "PERM": "A0 70",
    "N!" : "62",
    "GAMMA": "A0 74",
    "RAN": "A0 71",
    "SEED": "A0 73",
    "RTN": "85",
    "AVIEW": "7E",
    "PROMPT": "8E",
    "PSE": "89",
    "AIP": "A6 31",
    "XTOA": "A6 6F",
    "AGRAPH": "A7 64",
    "PIXEL": "A7 65",
    "BEEP": "86",
    "GETKEY": "A2 6E",
    "MENU": "A2 5E",
    "X=0?": "67",
    "X≠0?": "63",
    "X<0?": "66",
    "X>0?": "64",
    "X≤0?": "7B",
    "X≥0?": "A2 5F",
    "X=Y?": "78",
    "X≠Y?": "79",
    "X<Y?": "44",
    "X>Y?": "45",
    "X≤Y?": "46",
    "X≥Y?": "A2 60",
    "PRΣ": "A7 52",
    "PRSTK": "A7 53",
    "PRA": "A7 48",
    "PRX": "A7 54",
    "PRUSR": "A7 61",
    "ADV": "8F",
    "PRLCD": "A7 62",
    "DELAY": "A7 60",
    "PRON": "A7 5E",
    "PROFF": "A7 5F",
    "MAN": "A7 5B",
    "NORM": "A7 5C",
    "TRACE": "A7 5D",
    "Σ+": "47",
    "Σ-": "48",
    "END": "C0 00 0D",
    ".END.": "C0 00 0D",
    "STOP": "84",
    "NEWMAT": "A6 DA",
    "R↑": "74",
    "REAL?": "A2 65",
    "CPX?": "A2 67",
    "STR?": "A2 68",
    "MAT?": "A2 66",
    "DIM?": "A6 E7",
    "ON": "A2 70",
    "OFF": "8D",
    "ΣREG?": "A6 78",
    "CLD": "7F",
    "ACOSH": "A0 66",
    "ALENG": "A6 41",
    "ALLΣ": "A0 AE",
    "AND": "A5 88",
    "AOFF": "8B",
    "AON": "8C",
    "AROT": "A6 46",
    "ASHF": "88",
    "ASINH": "A0 64",
    "ATANH": "A0 65",
    "ATOX": "A6 47",
    "BASE+": "A0 E6",
    "BASE-": "A0 E7",
    # "BASEx": "A0 E8",
    "BASE×": "A0 E8",
    "BASE÷": "A0 E9",
    "BASE±": "A0 EA",
    "BEST": "A0 9F",
    "BINM": "A0 E5",
    "BIT?": "A5 8C",
    "CORR": "A0 A7",
    "COSH": "A0 62",
    "CROSS": "A6 CA",
    "CUSTOM": "A2 6F",
    "DECM": "A0 E3",
    "DELR": "A0 AB",
    "DET": "A6 CC",
    "DOT": "A6 CB",
    "EDIT": "A6 E1",
    "EXITALL": "A2 6C",
    "EXPF": "A0 A0",
    "E^X-1": "58",
    "E↑X-1": "58",
    "FCSTX": "A0 A8",
    "FCSTY": "A0 A9",
    "FNRM": "A6 CF",
    "GETM": "A6 E8",
    "GROW": "A6 E3",
    "HEXM": "A0 E2",
    "HMS+": "49",
    "HMS-": "4A",
    "I+": "A6 D2",
    "I-": "A6 D3",
    "INSR": "A0 AA",
    "INVRT": "A6 CE",
    "J+": "A6 D4",
    "J-": "A6 D5",
    "LINF": "A0 A1",
    "LINΣ": "A0 AD",
    "LN1+X": "65",
    "LOGF": "A0 A2",
    "MEAN": "7C",
    "NOT": "A5 87",
    "OCTM": "A0 E4",
    "OLD": "A6 DB",
    "OR": "A5 89",
    "POSA": "A6 5C",
    "PUTM": "A6 E9",
    "PWRF": "A0 A3",
    "RCLEL": "A6 D7",
    "RCLIJ": "A6 D9",
    "RNRM": "A6 ED",
    "ROTXY": "A5 8B",
    "RSUM": "A6 D0",
    "R<>R": "A6 D1",
    "SDEV": "7D",
    "SINH": "A0 61",
    "SLOPE": "A0 A4",
    "STOEL": "A6 D6",
    "STOIJ": "A6 D8",
    "SUM": "A0 A5",
    "TANH": "A0 63",
    "TRANS": "A6 C9",
    "UVEC": "A6 CD",
    "WMEAN": "A0 AC",
    "WRAP": "A6 E2",
    "XOR": "A5 8A",
    "YINT": "A0 A6",
    "->DEC": "5F",
    "->OCT": "6F",
    "→DEC": "5F",
    "→OCT": "6F",
    "<-": "A6 DC",
    "^": "A6 DE",
    "v": "A6 DF",
    "->": "A6 DD",
    "←": "A6 DC",
    "↑": "A6 DE",
    "↓": "A6 DF",
    "→": "A6 DD",
    "%CH": "4D",
    # "`str`" : "Fn",
    "[MIN]": "A6 EA",
    "[MAX]": "A6 EB",
    "[FIND]": "A6 EC",
    "ADATE": "A6 81",
    "ATIME": "A6 84",
    "ATIME24": "A6 85",
    "CLK12": "A6 86",
    "CLK24": "A6 87",
    "DATE": "A6 8C",
    "DATE+": "A6 8D",
    "DDAYS": "A6 8E",
    "DMY": "A6 8F",
    "DOW": "A6 90",
    "MDY": "A6 91",
    "TIME": "A6 9C"
}

# ACCEL|LOCAT|HEADING
chars = {
    '÷': 0,
    '×': 1,
    '√': 2,
    '∫': 3,
    '░': 4,
    'Σ': 5,
    '▶': 6,
    'π': 7,
    '¿': 8,
    '≤': 9,
    '\\\[LF\\\]': 10, # for [LF]
    '≥': 11,
    '≠': 12,
    '↵': 13,
    '↓': 14,
    '→': 15,
    '←': 16,
    'µ': 17,
    'μ': 17,
    '£': 18,
    '₤': 18,
    '°': 19,
    'Å': 20,
    'Ñ': 21,
    'Ä': 22,
    '∡': 23,
    'ᴇ': 24,
    'Æ': 25,
    '…': 26,
    '␛': 27,
    'Ö': 28,
    'Ü': 29,
    '▒': 30,
    '■': 31,
    '•': 31,
    " ": 32,
    "!": 33,
    '"': 34,
    "#": 35,
    "$": 36,
    "%": 37,
    "&": 38,
    "'": 39,
    "(": 40,
    ")": 41,
    "*": 42,
    "+": 43,
    ",": 44,
    "-": 45,
    ".": 46,
    "/": 47,
    "0": 48,
    "1": 49,
    "2": 50,
    "3": 51,
    "4": 52,
    "5": 53,
    "6": 54,
    "7": 55,
    "8": 56,
    "9": 57,
    ":": 58,
    ";": 59,
    "<": 60,
    "=": 61,
    ">": 62,
    "?": 63,
    "@": 64,
    "A": 65,
    "B": 66,
    "C": 67,
    "D": 68,
    "E": 69,
    "F": 70,
    "G": 71,
    "H": 72,
    "I": 73,
    "J": 74,
    "K": 75,
    "L": 76,
    "M": 77,
    "N": 78,
    "O": 79,
    "P": 80,
    "Q": 81,
    "R": 82,
    "S": 83,
    "T": 84,
    "U": 85,
    "V": 86,
    "W": 87,
    "X": 88,
    "Y": 89,
    "Z": 90,
    "[": 91,
    '\\\\': 92, # for \
    "]": 93,
    '↑': 94,
    "_": 95,
    "`": 96,
    "a": 97,
    "b": 98,
    "c": 99,
    "d": 100,
    "e": 101,
    "f": 102,
    "g": 103,
    "h": 104,
    "i": 105,
    "j": 106,
    "k": 107,
    "l": 108,
    "m": 109,
    "n": 110,
    "o": 111,
    "p": 112,
    "q": 113,
    "r": 114,
    "s": 115,
    "t": 116,
    "u": 117,
    "v": 118,
    "w": 119,
    "x": 120,
    "y": 121,
    "z": 122,
    "{": 123,
    "|": 124,
    "}": 125,
    "~": 126,
    "⊦": 127
}

stacks = {'T': 0,
    'Z': 1,
    'Y': 2,
    'X': 3,
    'L': 4}

modops = [
    'ARCL', 'ASSIGN', 'ASTO', 'CF', 'CLP', 'CLV', 'DIM', 'DSE', 'EDITN', 'ENG',
    'FC?', 'FC?C', 'FIX', 'FS?', 'FS?C', 'GTO', 'INDEX', 'INPUT', 'INTEG',
    'ISG', 'KEY', 'LBL', 'MVAR', 'PGMINT', 'PGMSLV', 'PRV', 'RCL', 'RCL+',
    'RCL-', 'RCL÷', 'RCL×', 'SCI', 'SF', 'SIZE', 'SOLVE', 'STO', 'STO+',
    'STO-', 'STO÷', 'STO×', 'TONE', 'VARMENU', 'VIEW', 'X<>', 'XEQ', 'ΣREG',
    '|-' ]

strops = {
 '├': '7F',
 'CLP': 'F0',
 'MVAR': '90',
 'CLV': 'B0',
 'DIM': 'C4',
 'EDITN': 'C6',
 'INDEX': '87',
 'ISG': '96',
 'DSE': '97',
 'ARCL': 'B3',
 'ASTO': 'B2',
#  'GTO': '1D', # fix
#  'LBL': 'C0 00 Fn 00', # fix
 'STO': '81',
 'STO+': '82',
 'STO-': '83',
 'STO×': '84',
 'STO÷': '85',
 'RCL': '91',
 'RCL+': '92',
 'RCL-': '93',
 'RCL×': '94',
 'RCL÷': '95',
 'X<>': '86',
 'INPUT': 'C5',
 'VIEW': '80',
 'PRV': 'B1',
 'VARMENU': 'C1',
 'PGMINT': 'B4',
 'PGMSLV': 'B5',
 'INTEG': 'B6',
 'SOLVE': 'B7'
}

regops = {
 'ASTO': '9A',
 'ARCL': '9B',
 'STO': '91',
 'STO+': '92',
 'STO-': '93',
 'STO×': '94',
 'STO÷': '95',
 'RCL': '90',
 'RCL+': 'F2 D1',
 'RCL-': 'F2 D2',
 'RCL×': 'F2 D3',
 'RCL÷': 'F2 D4',
 'ISG': '96',
 'DSE': '97',
 'X<>': 'CE',
 'INPUT': 'F2 D0',
 'VIEW': '98',
 'SF': 'A8',
 'CF': 'A9',
 'FS?C': 'AA',
 'FC?C': 'AB',
 'FS?': 'AC',
 'FC?': 'AD',
 'TONE': '9F',
 'ΣREG': '99',
 'SIZE': 'F3 F7'
}

shortregops = {'RCL': '2', 'STO': '3'}

# FIX, SCI, ENG 10 or 11
# All use 'F1' command and then D5-7 or E5-7
# 10 = D
# 11 = E
# FIX = 5
# SCI = 6
# ENG = 7
# I'm putting this all in a dict so it is programmatically accessible
dispops = {
    'FIX': 5,
    'SCI': 6,
    'ENG': 7,
    'op': 'F1',
    10: 13,
    11: 14
}

indregops0 = {
 'FIX': '9C',
 'SCI': '9D',
 'ENG': '9E',
 'DIM': 'F2 EC',
 'EDITN': 'F2 EF',
 'INDEX': 'F2 DA',
 'INPUT': 'F2 EE',
 'CLV': 'F2 D8',
 'VARMENU': 'F2 F8',
 'PRV': 'F2 D9',
 'PGMINT': 'F2 E8',
 'PGMSLV': 'F2 E9',
 'INTEG': 'F2 EA',
 'SOLVE': 'F2 EB',
}
indregops = regops.copy()
indregops.update(indregops0)


indstrops = {
 'STO': '89',
 'STO+': '8A',
 'STO-': '8B',
 'STO×': '8C',
 'STO÷': '8D',
 'RCL': '99',
 'RCL+': '9A',
 'RCL-': '9B',
 'RCL×': '9C',
 'RCL÷': '9D',
 'GTO': 'AE',
 'XEQ': 'AF',
 'ASTO': 'BA',
 'ARCL': 'BB',
 'FIX': 'DC',
 'SCI': 'DD',
 'ENG': 'DE',
 'ISG': '9E',
 'DSE': '9F',
 'DIM': 'CC',
 'EDITN': 'CE',
 'INDEX': '8F',
 'X<>': '8E',
 'SF': 'A8',
 'CF': 'A9',
 'FS?C': 'AA',
 'FC?C': 'AB',
 'FS?': 'AC',
 'FC?': 'AD',
 'VIEW': '88',
 'INPUT': 'CD',
 'CLV': 'B8',
 'TONE': 'DF',
 'VARMENU': 'C9',
 'PRV': 'B9',
 'ΣREG': 'DB',
 'PGMINT': 'BC',
 'PGMSLV': 'BD',
 'INTEG': 'BE',
 'SOLVE': 'BF'
}

lblops = {
    'LBL': 'CF', 
    'GTO': 'D0 00', 
    'XEQ': 'E0 00', 
    'LBLstr': 'C0 00', 
    'GTOstr': '1D', 
    'XEQstr': '1E',
    'GTOXEQind': 'AE',
    'GTOind': 0, 
    'XEQind': 128,
    'GTOindST': 112, 
    'XEQindST': 240,
    'GTOindstr': 'AE', 
    'XEQindstr': 'AF'
    }

shortlblops = {
    'LBL': 1, # '0'
    'GTO': 177,  # 'B1'
    }

shortlblsuffix = {
    'GTO': '00', 
    }

toops = {
 'ASSIGN': 'C0',
 'KEY': 'F3',
 'KEYXEQ': 'E2',
 'KEYGTO': 'E3',
 'KEYXEQstr': 'C2',
 'KEYGTOstr': 'C3',
 'KEYXEQindstr': 'CA',
 'KEYGTOindstr': 'CB'
    }

commandtr = {
    # 41 commands
    'ST+' : 'STO+',
    'ST-' : 'STO-',
    'STx' : 'STOx',
    'ST÷' : 'STO÷',
    # prettify
    "R^": "R↑",
    r'R\v': "R↓",
    "Rv": "R↓",
    "RDN": "R↓",
    "\GS+": "Σ+",
    "\GS-": "Σ-",
    "CL\GS": "CLΣ",
    "\GSREG": "PRΣ",
    "\GSREG?": "ΣREG",
    "SUM+": "Σ+",
    "SUM-": "Σ-",
    "CLSUM": "CLΣ",
    "SUMREG": "PRΣ",
    "SUMREG?": "ΣREG",
    "X#0?": "X≠0?"	,
    "X<=0?": "X≤0?"	,
    "X>=0?": "X≥0?"	,
    "X#Y?": "X≠Y?"	,
    "X<=Y?": "X≤Y?"	,
    "X>=Y?": "X≥Y?"	,
    '|-': '├',
    "->POL": "→POL",
    "->REC": "→REC",
    "->DEG": "→DEG",
    "->RAD": "→RAD",
    "->OCT": "→OCT",
    "->DEC": "→DEC",
    "->HMS": "→HMS",
    "->HR": "→HR",
    "\->POL": "→POL",
    "\->REC": "→REC",
    "\->DEG": "→DEG",
    "\->RAD": "→RAD",
    "\->OCT": "→OCT",
    "\->DEC": "→DEC",
    "\->HMS": "→HMS",
    "\->HR": "→HR",
    "+/-": "±",
    "CHS": "±",
    "FACT": "N!",
    # "x": "×",
    # "*": "×",
    # "/": "÷",
    "RCLx": "RCL×",
    "RCL*": "RCL×",
    "RCL/": "RCL÷",
    "STOx": "STO×",
    "STO*": "STO×",
    "STO/": "STO÷",

    "10^X": "10↑X",
    "X^2": "X↑2",
    "Y^X": "Y↑X",
    "BASEx": "BASE×",
    "BASE+/-": "BASE±",
    "E^X-1": "E↑X-1",
    "ENTER^": "ENTER"
    }

chartr = {
    r'\:-': "÷",
    r'\x': "×",
    r'\v/': "√",
    r'\S': "∫",
    r'\FUZ': "▒",
    r'\GS': "Σ",
    r'\|>': "▸",
    r'\PI': "π",
    r'\?': "¿",
    r'\<=': "≤",
    r'[LF]': "line feed",
    r'\>=': "≥",
    r'\#': "≠",
    r'\</': "↵",
    r'\v': "↓",
    r'\->': "→",
    r'\<-': "←",
    r'\PND': "£",
    r'\m': "μ",
    r'\o': "°",
    r'\Ao': "Å",
    r'\N~': "Ñ",
    r'\A"': "Ä",
    r'\<\\': "∡",
    r'\E': "ᴇ",
    r'\AE': "Æ",
    r'\...': "…",
    r'\O"': "Ö",
    r'\U"': "Ü",
    r'^': "↑",
    r'\^': "↑",
    r'\.': "•"
    }

reverttr = {
    "1÷X": "1/X"
    }

# stackre = re.compile(r'(STO)')

# 'TONE', 'SIZE', 'ΣREG', 
# 'ENG', 'FIX', 'SCI',
# 'SF', 'CF', 'FC?', 'FC?C', 'FS?', 'FS?C',
# 'KEY', 'KEY',

bytere = re.compile(r'\d*\s*{\s*\d+-Byte Prgm\s}', re.I)
linenore = re.compile(r'^[0-9]*▸?\s*')
regre = re.compile(r'\d\d')
locallbl = list('ABCDEFGHIJabcde')
labelre = re.compile(r'^([0-9]*)\s(LBL)')

numberre = re.compile(r'-?\d+(\.\d+|)((ᴇ|e|E)-?\d+|)')
strre = re.compile('\".*\"')
concatre = re.compile('^\|-"')

ndigitre = re.compile(r'(\d)')
ndecimalre = re.compile(r'\.')
nere = re.compile(r'(ᴇ|e|E)')
nminusre = re.compile(r'-')

def locallblhex(lbl):
    if lbl.isupper():
        loc = hex(ord(lbl) + 37)[2:]
    else:
        loc = hex(ord(lbl) + 26)[2:]
    return loc

def numtoraw(number):
    n = ndigitre.sub(r' 1\1', number)
    n = n.replace('.', ' 1A')
    n = nere.sub(r' 1B', n)
    n = n.replace('-', ' 1C').strip()
    n = n + ' 00'
    return n

def strlen(word):
    return hex(240 + len(word))[2:] 

def strtoraw(st, f = True):
    l = len(st)
    if l > 15:
        st = st[:14]
    if f:
        # out = strlen(st) + binascii.hexlify(st.encode()).decode()
        out = strlen(st) + ''.join(['{:02x}'.format(chars[i]) for i in st])
    else:
        # out = binascii.hexlify(st.encode()).decode()
        out = ''.join(['{:02x}'.format(chars[i]) for i in st])
    return out

def remove_lineno(lines):
    if bytere.match(lines[0]):
        lines = lines[1:]
    if type(lines) == type(''):
        lines = lines.split("\n")
    return [linenore.sub('', line.strip()) for line in lines]

# sub('({})'.format('|'.join(map(re.escape, replacements.keys()))), lambda m: replacements[m.group()], s)


def translatechars(lines):
    out = []
    for line in lines:
        tmpline = []
        for word in line.split(" "):
            if word in chartr:
                tmpline.append(chartr[word])
            elif strre.match(word):
                tmpword = []
                for c in word.strip('"'):
                    tmpline.append(chartr[c])
                tmpline.append('"{}"'.format(tmpword))
            else:
                tmpline.append(word)
        out.append(tmpline)
    return out

chartrre = re.compile('({})'.format('|'.join(map(re.escape, chartr.keys()))))
revertre = re.compile('({})'.format('|'.join(map(re.escape, reverttr.keys()))))

def translatecmds(lines):
    out = []
    for line in lines:
        words = line.split(' ')
        if words[0] in commandtr:
            tmp = commandtr[words[0]] + ' ' + ' '.join(words[1:])
            # a few commands don't have extra words, so just strip out the
            # spaces added from the above line
            out.append(tmp.strip())
        elif concatre.match(line):
            out.append(concatre.sub('├"', line))
        else:
            out.append(line)
    return out


def translatechars2(lines):
    tlines = []
    for l in lines:
        tlines.append(chartrre.sub(lambda m: chartr[m.group()], l))
    # for l in tlines:
    #     tlines2.append(revertre.sub(lambda m: reverttr[m.group()], l))
    return tlines


def tohex(lines):
    out = []
    for lineno, line in enumerate(lines):
        if line in fixed.keys():
            out.append(fixed[line])
        elif strre.match(line):
            out.append(strtoraw(line.strip('"')))
        elif numberre.match(line):
            out.append(numtoraw(line))
        elif line[0] == "├":
            # concatenation string
            w = line[1:].strip('"')
            o = strtoraw(w, 0)
            l = strlen(w + ' ')
            i = strops[line[0]]
            out.append(l + i + o)
        else:
            outwords = []
            words = line.split(" ")
            if words[0] in modops:
                if words[0] in toops:
                    if words[0] == 'ASSIGN':
                        w = words[1].strip('"')
                        o = strtoraw(w, 0)
                        l = strlen(w + '  ')
                        i = toops[words[0]]
                        loc = '{:02x}'.format(int(words[3]) - 1)
                        out.append(l + i + o + loc)
                    else:
                        reg = words[3]
                        l = toops['KEY']
                        if strre.match(reg):
                            w = reg.strip('"')
                            loc = strtoraw(w, 0)
                            l = strlen(w + '  ')
                            inst = toops[words[0]+words[2]+'str']
                        elif regre.match(reg):
                            loc = '{:02x}'.format(int(reg))
                            inst = toops[words[0]+words[2]]
                        elif reg in locallbl:
                            inst = toops[words[0]+words[2]]
                            loc = locallblhex(reg)
                        elif reg == 'IND':
                            if words[4] == 'ST':
                                inst = toops[words[0]+words[2]]
                                loc = 'F{}'.format(stacks[words[5]])
                            elif regre.match(words[4]):
                                inst = toops[words[0]+words[2]]
                                loc = '{:02x}'.format(128 + int(words[4]))
                            elif strre.match(words[4]):
                                w = words[4].strip('"')
                                loc = strtoraw(w, 0)
                                l = strlen(w + '  ')
                                inst = toops[words[0]+words[2]+'indstr']
                        k = '{:02x}'.format(int(words[1]))
                        out.append(l + inst + k + loc)
                # first look for commands with a string as the argument
                elif words[0] in strops and strre.match(words[1]):
                    w = words[1].strip('"')
                    o = strtoraw(w, 0)
                    l = strlen(w + ' ')
                    i = strops[words[0]]
                    out.append(l + i + o)
                # look for numerical register operations
                elif words[0] in regops and regre.match(words[1]):
                    num = int(words[1])
                    numhex = '{:02x}'.format(num)
                    if words[0] == 'SIZE':
                        numhex = "{:02x}{:02x}".format(int(num/256), 
                            int(num % 256))
                        out.append(regops[words[0]] + numhex)
                    elif num < 16 and words[0] in ['STO', 'RCL']:
                        out.append(shortregops[words[0]] + numhex[1])
                    else:
                        out.append(regops[words[0]] + numhex)
                # look for stack register operations
                elif words[0] in regops and words[1] == 'ST':
                    out.append(regops[words[0]] +
                        '7{}'.format(stacks[words[2]]))
                # stack register operations without ST
                elif words[0] in regops and words[1] in stacks:
                    out.append(regops[words[0]] +
                        '7{}'.format(stacks[words[1]]))
                # look for IND indirect register operations
                elif words[0] in indregops and words[1] == 'IND':
                    # look for a register number
                    if regre.match(words[2]):
                        num = int(words[2])
                        numhex = hex(128 + num)[2:]
                        out.append(indregops[words[0]] + numhex)
                    # look for a stack
                    elif words[2] == 'ST':
                        out.append(indregops[words[0]] +
                            'F{}'.format(stacks[words[3]]))
                    # look for a string
                    elif strre.match(words[2]):
                        w = words[2].strip('"')
                        o = strtoraw(w, 0)
                        l = strlen(w + ' ')
                        i = indstrops[words[0]]
                        out.append(l + i + o)
                # labels ops - GTO, XEQ, LBL, KEY
                elif words[0] in lblops:
                    if regre.match(words[1]):
                        num = int(words[1])
                        # local short labels - < 16
                        if num < 15 and words[0] in shortlblops:
                            numhex = '{:02x}'.format(shortlblops[words[0]] +
                                num)
                            op = numhex
                            if words[0] in shortlblsuffix:
                                op += shortlblsuffix[words[0]]
                            out.append(op)
                        # local 'long' labels - > 15
                        else:
                            numhex = '{:02x}'.format(num)
                            out.append(lblops[words[0]] + numhex)
                    # local letter labels
                    # I don't like this but I'm not sure what the math was for
                    # local letter labels...
                    elif words[1] in locallbl:
                        numhex = locallblhex(words[1])
                        out.append(lblops[words[0]] + numhex)
                    # string labels
                    elif strre.match(words[1]):
                        w = words[1].strip('"')
                        o = strtoraw(w, 0)
                        l = strlen(w)
                        inst = lblops[words[0]+'str']
                        if words[0] == 'LBL':
                            l = strlen(w + ' ') + '00'
                        out.append(inst + l + o)
                    # INDirect labels
                    elif words[1] == 'IND':
                        # string labels
                        op = lblops['GTOXEQind']
                        if words[2] == 'ST':
                            num = int(lblops[words[0] + 'indST']) + stacks[words[3]]
                            out.append(op + '{:02x}'.format(num))
                        elif regre.match(words[2]):
                            num = int(lblops[words[0] + 'ind']) + int(words[2])
                            out.append(op + '{:02x}'.format(num))
                        elif strre.match(words[2]):
                            w = words[2].strip('"')
                            o = strtoraw(w, 0)
                            l = strlen(w + ' ')
                            inst = lblops[words[0]+'indstr']
                            out.append(l + inst + o)
                elif words[0] in ['FIX', 'SCI', 'ENG', 'TONE']:
                    if int(words[1]) < 10:
                        inst = indregops[words[0]]
                        o = '{:02x}'.format(int(words[1]))
                    elif int(words[1]) in [10, 11]:
                        inst = dispops['op']
                        o = '{:1x}{:1x}'.format(dispops[int(words[1])], 
                            dispops[words[0]])
                    out.append(inst + o)
            else:
                print("error - line no. {}: {}".format(lineno + 1,
                    ' '.join(words)))
    # out = [fixed[i] for i in words]

    return out

def process_file(lines):
    # strip empty elements
    lines = [x for x in lines if x != []]
    lines2 = remove_lineno(lines)
    lines3 = translatecmds(lines2)
    lines4 = translatechars2(lines3)
    if lines4[-1] != 'END':
        lines4.append('END')
    return lines4

def prettify_file(lines, numbytes):
    totallines = len(lines)
    numdigits = len(str(totallines))
    if numdigits < 2:
        numdigits = 2
    progstr = "{{ {:d}-Byte Prgm }}".format(numbytes)
    newlines = lines.copy()
    newlines.insert(0, progstr)
    fmtstr = "{{:0{}d}} ".format(numdigits)
    numlines = []
    for n,l in enumerate(newlines):
        tmpline = fmtstr.format(n) + l
        tmpline = labelre.sub(r'\1▸\2', tmpline)
        numlines.append(tmpline)
    return numlines

def write_raw(ofn, hexout):
    with open(ofn, 'wb') as outf:
        outf.write(binascii.unhexlify(hexout))

def print_raw(hexout, concat = False):
    if concat:
        delimiter = ''
    else:
        delimiter = '\n'
    print(delimiter.join([h.upper() for h in hexout]))


    hexout3 = ''.join(hexout2)
    bytelength = int(len(hexout3)/2 - 3)
    progstr = "{{ {}-Byte Prgm }}".format(bytelength)

def read_file(fn):
    # with open(fn) as f:
    #     lines = f.readlines()
    lines = [l for l in fileinput.input(fn)]
    lines = ''.join(lines).strip()
    lines = lines.split('\n')
    return lines

def main(argv=None):

    if argv is None:
        argv = sys.argv
    programName = os.path.basename(argv[0])

    description ="""Encodes programs for the DM42 calculator.
    
    The calculator uses a superset of HP42S program commands.  By default, if the encoded program is writen to a file with the [-w] option, the raw file is written to the same location as the input file."""
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument('--version', action='version',
        version='%(prog)s {}'.format(__version__))

    # parser.add_argument('-t', '--test', action="store_true", dest="test", help="Prints the file renaming without actually renaming the files.",
    #     default=False)

    group1 = parser.add_argument_group('printing',
        'commands that print the processed program.')
    group1.add_argument('-p', '--print', action="store_true", dest="print", help="Prints the file - prettified output", default=False)

    group1.add_argument('--hex', action="store_true",
        dest="hex", help="Prints encoded hex", default=False)

    group1.add_argument('-l', '--hexlines', action="store_true", 
        dest="hexlines",
        help="Prints encoded hex one command per line", default=False)

    group1.add_argument('-b', '--binary', action="store_true",
        dest="binary", help="Prints encoded hex in binary - suitable for piping", default=False)


    group2 = parser.add_argument_group('writing',
        'commands that write the raw output.')
    group2.add_argument('-o', '--out', dest="outfile", 
        help="Set the output raw filename")

    group2.add_argument('-w', '--write', dest="write", action='store_true',
        help="Write the output raw data to a file")

    parser.add_argument('infile')
    # parser.add_argument('outfile', nargs='?')
    args = parser.parse_args()

    # if not args.file:
    #     parser.print_usage()
    #     return 2	
    # print(args.infile)

    lines = read_file(args.infile)

    # set file names
    fn1, fn2 = os.path.split(args.infile)
    fn2a, fn2ext = os.path.splitext(fn2)

    # remove line numbers
    nonumlines = remove_lineno(lines)
    # translate inconsistent/HP41 commands
    lines2 = translatecmds(nonumlines)
    # translate special characters
    glines = translatechars2(lines2)

    # convert to hex values
    hexout = tohex(glines)
    # remove spaces in hex codes
    hexout2 = [h.replace(' ', '') for h in hexout]
    # remove line breaks
    comphex = ''.join(hexout2)
    numbytes = int(len(comphex)/2 - 3)
    
    # prettify output
    plines = prettify_file(glines, numbytes)
    if args.hex or args.hexlines:
        args.print = True
    if args.print:
        if args.hex:
            if args.hexlines:
                print('\n'.join(hexout2))
            else:
                print(comphex)
        else:
            print('\n'.join(plines))
    if args.binary:
        sys.stdout.buffer.write(binascii.unhexlify(comphex))

    ofn = os.path.join(fn1, fn2a + '.raw')
    if args.outfile:
        args.write = True
    if args.write:
        if not args.outfile:
            if args.infile == '-':
                ofn = 'out.raw'
            else:
                ofn = os.path.join(fn1, fn2a + '.raw')
            if os.path.exists(ofn):
                a, b = os.path.splitext(ofn)
                ofn = a + "-{}.raw"
                i = 1
                while os.path.exists(ofn.format(i)):
                    i += 1
                ofn = ofn.format(i)
        else:
            ofn = os.path.expanduser(args.outfile)
        write_raw(ofn, comphex)



if __name__ == "__main__":
    sys.exit(main())
