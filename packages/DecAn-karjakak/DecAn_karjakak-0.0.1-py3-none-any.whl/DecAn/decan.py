# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

import time
import os
import argparse
import json
import functools

def timer(func):
    """
    Print the runtime of the decorated function
    https://realpython.com/primer-on-python-decorators/#timing-functions
    """
    
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        if value:
            print(value[:-1])
        print(f"\nFinished {func.__name__!r} in {run_time:.4f} secs")
    return wrapper_timer

def lookwd(alp: str, text: str):
    # Looking for an alphabet or a words positions.
    
    if alp in text:
        pos = ()
        np = 0
        c = text.count(alp)
        if len(alp) == 1:
            while c:
                np = np + text.find(alp)
                pos = pos + (np,)
                np += 1
                c -= 1
                text = text[text.find(alp)+1:]
            del np, text, c, alp
            return pos
        else:
            while c:
                np = np + text.find(alp)
                pos = pos + ((np, np + len(alp)),)
                np += 1
                c -= 1
                text = text[text.find(alp)+1:]
            del np, text, c, alp
            return pos

@timer
def deconstruct(text: str, filename: str, path: str):
    # To deconstruct a text file or sentences to json.
    
    if os.path.isfile(text):
        if text.rpartition('.')[2] == 'txt':
            with open(text) as rd:
                text = rd.read()
        else:
            raise Exception('Cannot read non-.txt file!!!')
    dics = {}
    alph = sorted(tuple(set(text)))
    for i in alph:
        if i != " ":
            gtp = lookwd(i, text)
            dics = dics | {i: gtp} 
            del gtp
    dics = dics | {'alphs': alph, 'total': len(text)}
    if os.path.isdir(path):
        with open(os.path.join(path, fi := f'{filename}.json' if '.json' not in filename else filename), 'w') as dc:
            json.dump(dics, dc)
    del dics, alph, text, filename, path, fi

@timer
def construct(filejson: str):
    # To construct back the deconstruct text that saved in json file.
    
    if os.path.isfile(filejson):
        with open(filejson) as rjs:
            rd = json.load(rjs)
        crtx = ''.join(' ' for i in range(rd['total']))
        for i in rd['alphs']:
            if i != " ":
                for j in rd[i]:
                    crtx = f'{crtx[:j]}{i}{crtx[j+1:]}'
        return crtx

@timer
def textsortchrs(txts: str, alph: list = None):
    # Doing analysis of finding each char or words for their position in text. 
    
    if os.path.isfile(txts):
        if txts.rpartition('.')[2] == 'txt':
            with open(txts) as rd:
                txts = rd.read()
        else:
            raise Exception('Cannot read non-.txt file!!!')
        
    dics = {}
    if isinstance(alph, list):
        for i in alph:
            gtp = lookwd(i, txts)
            if gtp:
                dics = dics | {i: {len(gtp): gtp}} 
                del gtp
                if len(i) > 1:
                    print(f'"{i}": {dics[i]}')
                    print(f'"{i}" is {len(dics[i][list(dics[i])[0]])} out of total {len(txts.split(" "))} words!\n')
                    del dics[i]
                else:
                    print(f'{repr(i)}: {dics[i]}')
                    print(f'{repr(i)} is {len(dics[i][list(dics[i])[0]])} out of total {len(txts)} chars!\n')
                    del dics[i]
            else:
                print(f'No such word {repr(i)} in text!!!')
    else:
        alph = sorted(tuple(set(txts)))
        for i in alph:
            gtp = lookwd(i, txts)
            dics = dics | {i: {len(gtp): gtp}} 
            del gtp
            print(f'{repr(i)}: {dics[i]}\n')
            del dics[i]
        print(f'Total of {len(txts)} chars!\n')

def main():
    parser = argparse.ArgumentParser(prog = 'DecAn',description = 'Analyze and Deconstruct words')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--deconstruct', type = str, nargs = 3, help = 'Save deconstruct as json file')
    group.add_argument('-c', '--construct', type = str, help = 'Construct back the deconstruct in json file')
    parser.add_argument('-a', '--analyze', type = str, help = 'Analyzing chars in a text')
    parser.add_argument('-s', '--search', type = str, action = 'extend', nargs = '+', help = 'Search list [only use after "-r"]')
    args = parser.parse_args()
    if args.analyze:
        if args.search:
            textsortchrs(args.analyze, args.search)
        else:
            textsortchrs(args.analyze)
    elif args.deconstruct:
        deconstruct(args.deconstruct[0], args.deconstruct[1], args.deconstruct[2])
    elif args.construct:
        construct(args.construct)

if __name__ == '__main__':
    main()