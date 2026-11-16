#!/usr/bin/env python3
"""Copy explicitly selected PNGs unchanged; create single-sprite metas from a project template."""
import argparse
import json
from pathlib import Path
import re
import struct
import uuid
from lanhu_unity import project_path, read_json, sha, write_json


def run(project, source_root, manifest, report):
    spec = read_json(manifest)
    template = project_path(project, spec['metaTemplate']).read_text()
    if not re.search(r'^  spriteMode: 1$', template, re.M) or not re.search(r'^  textureType: 8$', template, re.M):
        raise ValueError('Template must be a single-sprite TextureImporter')
    pending = {}
    records = []
    for item in spec['sprites']:
        source = project_path(source_root, item['source'])
        data = source.read_bytes()
        if data[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError('Not PNG: ' + item['source'])
        size = list(struct.unpack('>II', data[16:24]))
        if size != item['pixels']:
            raise ValueError('Source dimensions changed: ' + item['source'])
        dest = project_path(project, item['target'])
        guid = uuid.uuid5(uuid.NAMESPACE_URL, 'lanhu-unity/' + item['target']).hex
        meta = re.sub(r'^guid: .*$', 'guid: '+guid, template, flags=re.M)
        border = item.get('border', [0,0,0,0])
        if min(border) < 0 or border[0]+border[2]>size[0] or border[1]+border[3]>size[1]:
            raise ValueError('Invalid sprite border')
        meta = re.sub(r'^  spriteBorder:.*$', '  spriteBorder: {'+', '.join(f'{k}: {v}' for k,v in zip('xyzw',border))+'}', meta, flags=re.M)
        for path, content in ((dest,data), (Path(str(dest)+'.meta'),meta.encode())):
            if path.exists() and path.read_bytes() != content:
                raise ValueError('Refusing to replace existing asset: '+str(path))
            pending[path] = content
        records.append({**item,'guid':guid,'sha256':sha(data)})
    for path,content in pending.items():
        path.parent.mkdir(parents=True,exist_ok=True)
        if not path.exists():
            with path.open('xb') as stream:
                stream.write(content)
        parent=path.parent
        while parent != project/'Assets' and parent.is_relative_to(project/'Assets'):
            meta=Path(str(parent)+'.meta')
            if not meta.exists():
                guid=uuid.uuid5(uuid.NAMESPACE_URL,'lanhu-unity/'+parent.relative_to(project).as_posix()).hex
                with meta.open('x') as stream:
                    stream.write(f'fileFormatVersion: 2\nguid: {guid}\nfolderAsset: yes\nDefaultImporter:\n  externalObjects: {{}}\n  userData:\n  assetBundleName:\n  assetBundleVariant:\n')
            parent=parent.parent
    write_json(report, {'sprites':records,'sourceImagesUnmodified':True})
    return len(records)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',required=True)
    parser.add_argument('--source-root',required=True)
    parser.add_argument('--manifest',required=True)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    print(json.dumps({'imported':run(Path(args.project).resolve(),Path(args.source_root).resolve(),args.manifest,args.report)}))
