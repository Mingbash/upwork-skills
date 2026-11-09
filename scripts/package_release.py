#!/usr/bin/env python3
"""Build deterministic local candidate archives from an explicit audited allowlist."""
from pathlib import Path
import argparse, hashlib, json, zipfile
from check_release import check, ROOT
VERSION='0.1.0'

def build(out):
    errors=check()
    if errors:raise ValueError('\n'.join(errors))
    manifest=json.loads((ROOT/'release-files.json').read_text())
    files=[]
    for name in manifest:
        source=ROOT/name
        p=source.resolve()
        if not p.is_relative_to(ROOT) or not p.is_file() or source.is_symlink():raise ValueError('Invalid allowlisted path: '+name)
        files.append((name,p))
    out.mkdir(parents=True,exist_ok=True)
    results={}
    def archive(filename,entries):
        dest=out/filename
        with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for name,p in sorted(entries):
                info=zipfile.ZipInfo(name,(2026,11,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                z.writestr(info,p.read_bytes())
        results[filename]={'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'files':len(entries)}
    archive(f'{ROOT.name}-{VERSION}-source.zip',[(ROOT.name+'/'+n,p) for n,p in files])
    skills=sorted((ROOT/'skills').iterdir())
    for skill in skills:
        prefix='skills/'+skill.name+'/'
        archive(f'{skill.name}-{VERSION}.zip',[(n[len('skills/'):],p) for n,p in files if n.startswith(prefix)])
    if len(skills)>1:
        # Source archive doubles as the complete collection, including readable docs.
        results[f'{ROOT.name}-{VERSION}-source.zip']['kind']='complete collection and source repository'
    (out/(ROOT.name+'-checksums.json')).write_text(json.dumps(results,indent=2)+'\n')
    return results

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=ROOT/'build');args=parser.parse_args()
    print(json.dumps(build(args.out.resolve()),indent=2))

if __name__=='__main__':main()
