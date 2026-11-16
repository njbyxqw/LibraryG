#!/usr/bin/env python3
"""Explicit Lanhu-to-existing-UGUI mappings, with preview and guarded application."""
import argparse
import difflib
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import sys
from nested import expand_nested, flush_nested


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def project_path(root, relative):
    value = (root / relative).resolve()
    if Path(relative).is_absolute() or not value.is_relative_to(root):
        raise ValueError('Expected path inside project: ' + relative)
    return value


def scalar(block, field):
    matches = re.findall(r'^  ' + re.escape(field) + r': ?(.*)$', block, re.M)
    if len(matches) != 1:
        raise ValueError('Expected one field ' + field)
    return matches[0]


def vector(block, field):
    return [float(v) for v in re.findall(r'[xyzw]: ([^,}]+)', scalar(block, field))]


def fmt(values):
    return '{' + ', '.join(f'{k}: {v:.9g}' for k, v in zip('xyzw', values)) + '}'


def replace_field(block, field, value):
    scalar(block, field)
    return re.sub(r'^  ' + re.escape(field) + r':.*$', lambda _: '  ' + field + ': ' + str(value), block, flags=re.M)


def layers(document):
    result = {}
    def walk(items, visible=True, inside_slice=False):
        for layer in items:
            item = dict(layer)
            item['effectiveVisible'] = visible and layer.get('visible', True)
            item['insideSlice'] = inside_slice
            key = str(layer['id'])
            if key in result:
                raise ValueError('Duplicate layer ID: ' + key)
            result[key] = item
            walk(layer.get('layers', []), item['effectiveVisible'], inside_slice or layer.get('isSlice', False))
    walk(document['board']['layers'])
    return result


class Prefab:
    def __init__(self, text, reference_size):
        self.prefix = text.split('--- !u!')[0]
        self.blocks = {}
        self.types = {}
        self.order = []
        for block in re.split(r'(?=^--- !u!)', text, flags=re.M)[1:]:
            match = re.match(r'--- !u!(\d+) &(-?\d+)(.*)', block)
            if not match or match[3].strip() not in ('', 'stripped'):
                raise ValueError('Unsupported YAML block header')
            kind, key = int(match[1]), int(match[2])
            if key in self.blocks:
                raise ValueError('Duplicate local fileID')
            self.blocks[key] = block
            self.types[key] = kind
            self.order.append(key)
        self.nested_origins = {}
        self.reference_size = list(reference_size)
        self.transforms = {k: int(re.search(r'fileID: (-?\d+)', scalar(v, 'm_GameObject'))[1]) for k, v in self.blocks.items() if self.types[k] == 224 and '\n  m_Father:' in v}
        self.parents = {k: int(re.search(r'fileID: (-?\d+)', scalar(self.blocks[k], 'm_Father'))[1]) for k in self.transforms}
        self.paths = {}
        def path(key, seen):
            if key in seen:
                raise ValueError('Transform cycle')
            name = scalar(self.blocks[self.transforms[key]], 'm_Name').strip('"')
            parent = self.parents[key]
            return (path(parent, seen | {key}) + '/' if parent in self.transforms else '') + name
        for key in self.transforms:
            name = path(key, set())
            if name in self.paths:
                raise ValueError('Ambiguous hierarchy path: ' + name)
            self.paths[name] = key
        self.components = {}
        for key, block in self.blocks.items():
            if self.types[key] in (1, 224):
                continue
            match = re.search(r'^  m_GameObject: \{fileID: (-?\d+)\}', block, re.M)
            if match:
                self.components.setdefault(int(match[1]), []).append(key)

    def text(self):
        return self.prefix + ''.join(self.blocks[k] for k in self.order)

    def transform(self, path):
        if path not in self.paths:
            raise ValueError('Hierarchy path not found: ' + path)
        return self.paths[path]

    def geometry(self, key):
        block = self.blocks[key]
        parent = self.parents[key]
        if parent not in self.transforms:
            if parent != 0:
                raise ValueError('Unresolved parent transform: '+str(parent))
            return [0., 0.], self.reference_size, [1., 1.]
        rot = vector(block, 'm_LocalRotation')
        if abs(rot[0]) + abs(rot[1]) + abs(rot[2]) > 1e-6 or abs(abs(rot[3])-1) > 1e-6:
            raise ValueError('Rotated RectTransform requires explicit Unity corner projection: ' + str(key))
        origin, parent_size, parent_scale = self.geometry(parent)
        amin, amax = vector(block, 'm_AnchorMin'), vector(block, 'm_AnchorMax')
        size_delta, pivot = vector(block, 'm_SizeDelta'), vector(block, 'm_Pivot')
        pos, local_scale = vector(block, 'm_AnchoredPosition'), vector(block, 'm_LocalScale')
        scale = [parent_scale[i] * local_scale[i] for i in range(2)]
        if min(scale) <= 0:
            raise ValueError('Nonpositive transform scale')
        size = [(amax[i]-amin[i])*parent_size[i]+size_delta[i] for i in range(2)]
        lower = [origin[i]+parent_scale[i]*(parent_size[i]*(amin[i]+(amax[i]-amin[i])*pivot[i])+pos[i])-size[i]*pivot[i]*scale[i] for i in range(2)]
        return lower, size, scale

    def set_rect(self, key, desired):
        parent = self.parents[key]
        if parent not in self.transforms:
            raise ValueError('Cannot remap the root')
        self.geometry(key)  # Reject unsupported transforms before mutation.
        origin, parent_size, parent_scale = self.geometry(parent)
        block = self.blocks[key]
        amin, amax = vector(block, 'm_AnchorMin'), vector(block, 'm_AnchorMax')
        pivot, local_scale = vector(block, 'm_Pivot'), vector(block, 'm_LocalScale')
        x, y, w, h = desired
        lower = [x, self.reference_size[1]-y-h]
        extent = [w, h]
        size = [extent[i]/(parent_scale[i]*local_scale[i]) for i in range(2)]
        pos = [(lower[i]+extent[i]*pivot[i]-origin[i])/parent_scale[i]-parent_size[i]*(amin[i]+(amax[i]-amin[i])*pivot[i]) for i in range(2)]
        delta = [size[i]-(amax[i]-amin[i])*parent_size[i] for i in range(2)]
        block = replace_field(block, 'm_AnchoredPosition', fmt(pos))
        block = replace_field(block, 'm_SizeDelta', fmt(delta))
        self.blocks[key] = block

    def component(self, transform, predicate):
        hits = [k for k in self.components.get(self.transforms[transform], []) if predicate(self.blocks[k])]
        if len(hits) != 1:
            raise ValueError('Expected one matching component on ' + str(transform))
        return hits[0]

    def inventory(self):
        result = []
        for path, key in self.paths.items():
            block = self.blocks[key]
            row = {'path': path, 'rectTransform': key, 'anchorMin': vector(block, 'm_AnchorMin'), 'anchorMax': vector(block, 'm_AnchorMax'), 'sizeDelta': vector(block, 'm_SizeDelta'), 'scale': vector(block, 'm_LocalScale')}
            try:
                origin, size, scale = self.geometry(key)
                row['rect'] = [origin[0], self.reference_size[1]-origin[1]-size[1]*scale[1], size[0]*scale[0], size[1]*scale[1]]
            except ValueError as e:
                row['geometryError'] = str(e)
            row['components'] = []
            for c in self.components.get(self.transforms[key], []):
                b = self.blocks[c]
                row['components'].append({'id': c, 'type': self.types[c], **{k: scalar(b,k) for k in ('m_Script','m_Sprite','m_text','localeKey') if re.search(r'^  '+k+':',b,re.M)}})
            result.append(row)
        return result


def resolve_rect(mapping, boards):
    source = mapping.get('source')
    expected = None
    if source:
        board = boards[source['board']]
        layer = board['layers'][str(source['layer'])]
        if not layer['effectiveVisible'] and not mapping.get('allowHiddenReason'):
            raise ValueError('Hidden source layer: '+str(source))
        expected = [layer[k] for k in ('left','top','width','height')]
    if 'rect' in mapping:
        if not mapping.get('reason'):
            raise ValueError('Explicit rectangle needs a reason')
        expected = mapping['rect']
    if expected is None or len(expected)!=4 or any(not math.isfinite(float(v)) for v in expected) or min(expected[2:])<=0:
        raise ValueError('Invalid rectangle')
    scale = mapping.get('sourceScale', 1)
    offset = mapping.get('sourceOffset', [0,0])
    return [expected[0]*scale+offset[0],expected[1]*scale+offset[1],expected[2]*scale,expected[3]*scale]


def plan(manifest, root, report_dir):
    spec = read_json(manifest)
    if spec.get('version') != 1 or not spec.get('prefabs'):
        raise ValueError('Expected nonempty version 1 manifest')
    boards = {}
    inputs = {}
    for name, filename in spec.get('boards', {}).items():
        path = project_path(root, filename)
        raw = path.read_bytes()
        document = json.loads(raw)
        boards[name] = {'document':document, 'layers':layers(document)}
        inputs[filename] = sha(raw)
    changes = []
    proposed = {}
    audits = []
    for item in spec['prefabs']:
        filename = item['path']
        if filename in proposed:
            raise ValueError('Duplicate prefab entry')
        path = project_path(root, filename)
        raw = path.read_bytes()
        inputs[filename] = sha(raw)
        prefab = Prefab(raw.decode('utf-8'), item['referenceSize'])
        for nested in item.get('nestedPrefabs', []):
            expand_nested(prefab, nested, root, inputs)
        original = dict(prefab.blocks)
        original_paths = dict(prefab.paths)
        allowed = {}
        expected_rects = []
        for mapping in item['mappings']:
            key = prefab.transform(mapping['target'])
            if 'layout' in mapping:
                if not mapping.get('reason') or not ('rect' in mapping or 'source' in mapping):
                    raise ValueError('Layout changes require reason and explicit target rectangle')
                for field, value in mapping['layout'].items():
                    if field not in ('m_AnchorMin', 'm_AnchorMax', 'm_Pivot') or len(value) != 2 or any(not math.isfinite(float(v)) or not 0 <= v <= 1 for v in value):
                        raise ValueError('Invalid layout field: '+field)
                    prefab.blocks[key] = replace_field(prefab.blocks[key], field, fmt(value))
                    allowed.setdefault(key,set()).add(field)
            if mapping.get('source') or 'rect' in mapping:
                rect = resolve_rect(mapping, boards)
                prefab.set_rect(key, rect)
                allowed.setdefault(key, set()).update(('m_AnchoredPosition','m_SizeDelta'))
                expected_rects.append((key,rect,mapping['target']))
            if 'sprite' in mapping:
                sprite_path = project_path(root,mapping['sprite'])
                meta_path = Path(str(sprite_path)+'.meta')
                meta = meta_path.read_text()
                if not re.search(r'^  spriteMode: 1$',meta,re.M):
                    raise ValueError('Only single-sprite assets supported: '+mapping['sprite'])
                guid = re.search(r'^guid: (\w+)',meta,re.M)[1]
                inputs[mapping['sprite']] = sha(sprite_path.read_bytes())
                inputs[mapping['sprite']+'.meta'] = sha(meta_path.read_bytes())
                component = prefab.component(key,lambda b: '\n  m_Sprite:' in b)
                prefab.blocks[component] = replace_field(prefab.blocks[component],'m_Sprite',f'{{fileID: 21300000, guid: {guid}, type: 3}}')
                allowed.setdefault(component,set()).add('m_Sprite')
            if 'imageEnabled' in mapping:
                if not mapping.get('reason'):
                    raise ValueError('Image visibility change needs a reason')
                component = prefab.component(key,lambda b: '\n  m_Sprite:' in b)
                prefab.blocks[component] = replace_field(prefab.blocks[component], 'm_Enabled', int(mapping['imageEnabled']))
                allowed.setdefault(component,set()).add('m_Enabled')
            if 'graphicAlpha' in mapping:
                alpha = float(mapping['graphicAlpha'])
                if not mapping.get('reason') or not 0 <= alpha <= 1:
                    raise ValueError('Graphic alpha needs a reason and a value between 0 and 1')
                component = prefab.component(key,lambda b: '\n  m_Color:' in b and '\n  m_RaycastTarget:' in b)
                color = re.sub(r'a: [^,}]+', 'a: '+str(alpha), scalar(prefab.blocks[component], 'm_Color'))
                prefab.blocks[component] = replace_field(prefab.blocks[component], 'm_Color', color)
                allowed.setdefault(component,set()).add('m_Color')
            # Deliberately exclude locale keys, content, raycasts, events, scripts, hierarchy and active state.
            permitted = {'m_Type','m_PreserveAspect','m_FillMethod','m_FillOrigin','m_PixelsPerUnitMultiplier','m_fontSize','m_fontSizeBase','m_fontSizeMin','m_fontSizeMax','m_enableAutoSizing','m_HorizontalAlignment','m_VerticalAlignment','m_characterSpacing','m_TextWrappingMode'}
            for field,value in mapping.get('style',{}).items():
                if field not in permitted:
                    raise ValueError('Unsupported style field: '+field)
                component = prefab.component(key,lambda b: bool(re.search(r'^  '+re.escape(field)+':',b,re.M)))
                prefab.blocks[component] = replace_field(prefab.blocks[component],field,value)
                allowed.setdefault(component,set()).add(field)
            changes.append({'prefab':filename,**mapping})
        # A later parent change must not invalidate an earlier child rectangle.
        max_error = 0
        for key,rect,name in expected_rects:
            origin,size,scale=prefab.geometry(key)
            actual=[origin[0],item['referenceSize'][1]-origin[1]-size[1]*scale[1],size[0]*scale[0],size[1]*scale[1]]
            error=max(abs(a-b) for a,b in zip(actual,rect))
            if error>0.001:
                raise ValueError('Final rect mismatch (order parent mappings before children): '+name+' '+str(error))
            max_error=max(max_error,error)
        for key,before in original.items():
            after = prefab.blocks[key]
            for field in allowed.get(key,set()):
                before = replace_field(before,field,'<ALLOWED>')
                after = replace_field(after,field,'<ALLOWED>')
            if before != after:
                raise ValueError('Unexpected nonvisual mutation: '+str(key))
        if original_paths != prefab.paths or set(original)!=set(prefab.blocks):
            raise ValueError('Hierarchy or object identity changed')
        flush_nested(prefab, original, allowed)
        result = prefab.text().encode()
        proposed[filename]=result
        audits.append({'prefab':filename,'mappedNodes':len(item['mappings']),'maxRectErrorPixels':max_error,'objectIdsAndHierarchyPreserved':True,'allUnlistedFieldsByteIdentical':True,'beforeSHA256':sha(raw),'afterSHA256':sha(result)})
    # All validation before writing any proposed file.
    report_dir.mkdir(parents=True,exist_ok=True)
    if (report_dir/'plan.json').exists():
        raise ValueError('Use a fresh report directory to preserve audit history')
    for filename,data in proposed.items():
        dest=report_dir/'proposed'/filename;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        before=project_path(root,filename).read_text()
        diff=''.join(difflib.unified_diff(before.splitlines(True),data.decode().splitlines(True),fromfile=filename,tofile=filename))
        diffpath=report_dir/'diffs'/(filename+'.diff');diffpath.parent.mkdir(parents=True,exist_ok=True);diffpath.write_text(diff)
    report={'version':1,'manifest':str(Path(manifest).resolve().relative_to(root)),'manifestSHA256':sha(Path(manifest).read_bytes()),'inputs':inputs,'audits':audits,'changes':changes,'status':'planned','verificationBoundary':'Static YAML geometry and preservation only; Unity loading, dynamic writers, interactions and device adaptation require separate checks.'}
    write_json(report_dir/'plan.json',report)
    return report


def apply(root,report_dir):
    report=read_json(report_dir/'plan.json')
    manifest=project_path(root,report['manifest'])
    if sha(manifest.read_bytes())!=report['manifestSHA256']:
        raise ValueError('Manifest changed; replan')
    for path,digest in report['inputs'].items():
        if sha(project_path(root,path).read_bytes())!=digest:
            raise ValueError('Input changed; replan: '+path)
    for audit in report['audits']:
        proposed=report_dir/'proposed'/audit['prefab']
        if sha(proposed.read_bytes())!=audit['afterSHA256']:
            raise ValueError('Proposed output changed')
    for audit in report['audits']:
        name=audit['prefab'];path=project_path(root,name);backup=report_dir/'before'/name
        backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(path.read_bytes())
    for audit in report['audits']:
        name=audit['prefab'];dest=project_path(root,name)
        if sha(dest.read_bytes())!=audit['beforeSHA256']:
            raise ValueError('Concurrent modification detected before write: '+name)
        dest.write_bytes((report_dir/'proposed'/name).read_bytes())
    report['status']='applied';write_json(report_dir/'result.json',report)
    return {'applied':len(report['audits']),'report':str(report_dir/'result.json')}


def verify(root,report_dir):
    report=read_json(report_dir/'plan.json')
    result=[]
    for a in report['audits']:
        result.append({'prefab':a['prefab'],'matchesPlannedOutput':sha(project_path(root,a['prefab']).read_bytes())==a['afterSHA256']})
    if not all(x['matchesPlannedOutput'] for x in result):
        raise ValueError('Current assets differ from planned output: '+json.dumps(result))
    return result


def rollback(root, report_dir):
    report=read_json(report_dir/'plan.json')
    for a in report['audits']:
        if sha(project_path(root,a['prefab']).read_bytes()) not in (a['beforeSHA256'], a['afterSHA256']):
            raise ValueError('Rollback would overwrite later work: '+a['prefab'])
        if sha((report_dir/'before'/a['prefab']).read_bytes()) != a['beforeSHA256']:
            raise ValueError('Backup changed or missing')
    for a in report['audits']:
        dest = project_path(root,a['prefab'])
        if sha(dest.read_bytes()) not in (a['beforeSHA256'], a['afterSHA256']):
            raise ValueError('Concurrent modification during rollback: '+a['prefab'])
        if sha(dest.read_bytes()) == a['afterSHA256']:
            dest.write_bytes((report_dir/'before'/a['prefab']).read_bytes())
    return {'rolledBack':len(report['audits'])}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['inspect-board','inspect-prefab','plan','apply','verify','rollback'])
    parser.add_argument('--project',default='.')
    parser.add_argument('--input')
    parser.add_argument('--manifest')
    parser.add_argument('--report')
    parser.add_argument('--size',nargs=2,type=float,default=[1080,2340])
    args=parser.parse_args();root=Path(args.project).resolve()
    if args.command=='inspect-board':
        doc=read_json(args.input);result={'board':{k:v for k,v in doc['board'].items() if k!='layers'},'layers':[{k:l.get(k) for k in ('id','name','type','effectiveVisible','insideSlice','isSlice','left','top','width','height','textInfo')} for l in layers(doc).values()]}
    elif args.command=='inspect-prefab':
        result=Prefab(Path(args.input).read_text(),args.size).inventory()
    elif args.command=='plan':
        result=plan(args.manifest,root,Path(args.report).resolve());result={'prefabs':len(result['audits']),'mappedNodes':len(result['changes']),'report':args.report}
    else:
        result=globals()[args.command](root,Path(args.report).resolve())
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    try:
        main()
    except (ValueError,KeyError,OSError) as error:
        print('ERROR: '+str(error),file=sys.stderr);sys.exit(2)
