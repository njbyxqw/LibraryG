"""Explicit single-level PrefabInstance overrides; source assets remain untouched."""
import re

MOD = re.compile(r'    - target: \{fileID: (-?\d+), guid: (\w+), type: 3\}\n      propertyPath: ([^\n]+)\n      value:([^\n]*)\n      objectReference: ([^\n]+)\n')


def override_block(block, source_id, guid, field, value, reference=False):
    matches = [m for m in MOD.finditer(block) if int(m[1]) == source_id and m[2] == guid and m[3] == field]
    if len(matches) > 1:
        raise ValueError('Duplicate nested override: ' + field)
    row = (f'    - target: {{fileID: {source_id}, guid: {guid}, type: 3}}\n'
           f'      propertyPath: {field}\n'
           f'      value:{"" if reference else " " + str(value)}\n'
           f'      objectReference: {value if reference else "{fileID: 0}"}\n')
    if matches:
        m = matches[0]
        return block[:m.start()] + row + block[m.end():]
    marker = '    m_RemovedComponents:'
    if block.count(marker) != 1:
        raise ValueError('Unsupported nested modification serialization')
    return block.replace(marker, row + marker)


def expand_nested(prefab, spec, root, inputs):
    from lanhu_unity import Prefab, project_path, sha, scalar, vector, fmt, replace_field
    instance = int(spec['instance'])
    block = prefab.blocks[instance]
    if prefab.types[instance] != 1001:
        raise ValueError('Expected PrefabInstance')
    source_path = project_path(root, spec['source'])
    meta_path = source_path.with_suffix(source_path.suffix + '.meta')
    guid = re.search(r'^guid: (\w+)', meta_path.read_text(), re.M)[1]
    if not re.search(r'm_SourcePrefab: \{fileID: 100100000, guid: ' + guid, block):
        raise ValueError('Source prefab GUID mismatch')
    inputs[spec['source']] = sha(source_path.read_bytes())
    inputs[spec['source'] + '.meta'] = sha(meta_path.read_bytes())
    source = Prefab(source_path.read_text(), prefab.reference_size)
    # Deeper instances remain opaque and cannot be targeted by this view.
    parent = int(re.search(r'm_TransformParent: \{fileID: (-?\d+)\}', block)[1])
    if parent not in prefab.transforms:
        raise ValueError('Unresolved nested parent')
    for m in MOD.finditer(block):
        key, field, value = int(m[1]), m[3], m[4].strip()
        if key not in source.blocks or m[2] != guid:
            # Stale or deeper-instance overrides remain byte-identical and untargetable.
            continue
        b = source.blocks[key]
        base, dot, axis = field.partition('.')
        if dot and axis in 'xyzw' and len(axis) == 1 and re.search(r'^  '+base+':', b, re.M):
            v = vector(b, base); v['xyzw'.index(axis)] = float(value)
            source.blocks[key] = replace_field(b, base, fmt(v))
        elif base == 'm_Color' and axis in ('r','g','b','a'):
            color = scalar(b, base)
            color = re.sub(r'\b'+axis+r': [^,}]+', axis+': '+str(float(value)), color)
            source.blocks[key] = replace_field(b, base, color)
        elif not dot and re.search(r'^  '+re.escape(field)+':', b, re.M):
            # Only geometric and identity/name fields are needed by the read model.
            if field == 'm_Name' or field in ('m_Sprite', 'm_Type', 'm_PreserveAspect', 'm_Enabled'):
                source.blocks[key] = replace_field(b, field, m[5] if value == '' else value)
    removed = set()
    removal = re.search(r'    m_RemovedGameObjects:(.*?)(?=    m_AddedGameObjects:)', block, re.S)
    if removal:
        removed = set(int(x) for x in re.findall(r'fileID: (-?\d+)', removal[1]))
    def removed_transform(k):
        while k in source.transforms:
            if source.transforms[k] in removed:
                return True
            k = source.parents[k]
        return False
    def connected(k):
        while k in source.transforms:
            k = source.parents[k]
        return k == 0
    kept = {k for k in source.transforms if connected(k) and not removed_transform(k)}
    def virtual(k):
        return f'{instance}:{k}'
    roots = [k for k in kept if source.parents[k] not in source.transforms]
    if len(roots) != 1:
        raise ValueError('Expected one nested RectTransform root')
    parent_path = next(p for p,k in prefab.paths.items() if k == parent)
    def path(k):
        name = scalar(source.blocks[source.transforms[k]], 'm_Name').strip('"')
        return (path(source.parents[k]) if source.parents[k] in kept else parent_path) + '/' + name
    for k in kept:
        v, go = virtual(k), virtual(source.transforms[k])
        name = path(k)
        if name in prefab.paths:
            raise ValueError('Duplicate expanded path: ' + name)
        prefab.paths[name] = v
        prefab.transforms[v] = go
        prefab.parents[v] = virtual(source.parents[k]) if source.parents[k] in kept else parent
        keys = [k, source.transforms[k]] + source.components.get(source.transforms[k], [])
        prefab.components[go] = [virtual(c) for c in source.components.get(source.transforms[k], [])]
        for c in keys:
            vc = virtual(c)
            prefab.blocks[vc] = source.blocks[c]
            prefab.types[vc] = source.types[c]
            prefab.nested_origins[vc] = (instance, c, guid)


def flush_nested(prefab, original, allowed):
    from lanhu_unity import scalar, vector
    edits = {}
    for key, fields in allowed.items():
        if key not in prefab.nested_origins:
            continue
        instance, source_id, guid = prefab.nested_origins[key]
        for field in fields:
            if scalar(original[key], field) == scalar(prefab.blocks[key], field):
                continue
            values = [(field, scalar(prefab.blocks[key], field))]
            if field in ('m_AnchoredPosition', 'm_SizeDelta', 'm_AnchorMin', 'm_AnchorMax', 'm_Pivot'):
                values = [(field+'.'+axis, f'{value:.9g}') for axis,value in zip('xy', vector(prefab.blocks[key], field))]
            elif field == 'm_Color':
                values = [(field+'.'+axis, value) for axis,value in re.findall(r'([rgba]): ([^,}]+)', scalar(prefab.blocks[key], field))]
            for prop,value in values:
                prefab.blocks[instance] = override_block(prefab.blocks[instance], source_id, guid, prop, value, field == 'm_Sprite')
                edits.setdefault(instance, set()).add((source_id, guid, prop))
    # Unlisted override rows and all instance topology must remain byte identical.
    for instance, changed in edits.items():
        def mask(b):
            return MOD.sub(lambda m: '' if (int(m[1]),m[2],m[3]) in changed else m[0], b)
        if mask(original[instance]) != mask(prefab.blocks[instance]):
            raise ValueError('Unexpected nested prefab mutation')
