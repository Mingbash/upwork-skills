#!/usr/bin/env python3
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();drift=[]
    for source,target in {'workspace.md':'references/workspace.md','options.md':'references/options.md','options.json':'assets/options.json'}.items():
        data=(ROOT/'shared'/source).read_bytes()
        for skill in (ROOT/'skills').iterdir():
            dest=skill/target
            if dest.read_bytes()!=data:
                drift.append(skill.name+'/'+target)
                if not a.check:dest.write_bytes(data)
    print(('DRIFT' if a.check and drift else 'OK')+': '+str(len(drift))+' copies')
    return bool(a.check and drift)
if __name__=='__main__':raise SystemExit(main())
