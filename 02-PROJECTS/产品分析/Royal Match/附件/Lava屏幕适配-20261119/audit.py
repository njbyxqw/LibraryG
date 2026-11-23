from pathlib import Path
import bisect, hashlib, json, re, struct, importlib.metadata
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
from elftools.elf.elffile import ELFFile

out = Path(__file__).resolve().parent
source = out.parent / 'Period-Audit'
meta = json.loads((source / 'dump/dump/script.json').read_text('utf-8-sig'))
methods = {m['Address']: m for m in meta['ScriptMethod']}
metadata = {m['Address']: m['Name'] for key in ['ScriptMetadata', 'ScriptMetadataMethod', 'ScriptString'] for m in meta[key] if 'Name' in m}
addresses = sorted(methods)
binary = (source / 'libil2cpp.so').read_bytes()
digest = hashlib.sha256(binary).hexdigest()
assert digest == 'ea4eaf596b64ff255cc042d52d32e44078ed773d70be6c3368db9459a12b3a22'
with (source / 'libil2cpp.so').open('rb') as stream:
    elf = ELFFile(stream)
    segments = [(s['p_vaddr'], s['p_offset'], s['p_filesz']) for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD']
    relocated = {}
    for section in elf.iter_sections():
        if section['sh_type'] == 'SHT_RELA':
            for relocation in section.iter_relocations():
                target = relocation['r_addend']
                if target in metadata:
                    relocated[relocation['r_offset']] = metadata[target]
    metadata.update(relocated)

def read(address, count):
    for virtual, offset, size in segments:
        if virtual <= address and address + count <= virtual + size:
            return binary[offset + address - virtual:offset + address - virtual + count]
    return b''

classes = ['LavaQuestCompletedScene', 'LavaQuestCompetitionDialog', 'LavaQuestCompetitionSceneView', 'AncientAdventureRewardClaimPanel', 'AncientAdventureDialog', 'AncientAdventureSceneController', 'AncientAdventureSceneView', 'AncientAdventurePlayerView', 'LavaQuestStartDialog', 'AncientAdventureStartDialog']
records = []
for address, method in sorted(methods.items()):
    name = method['Name']
    selected = ('LavaQuestCompetitionDialog$$' in name and any(k in name for k in ['Init','PrepareHeader','PrepareTopPanel','ArrangeColliders','ArrangeTapToContinue','GetConfig','ShowDialogWithUiAnimation'])) or ('LavaQuestCompetitionSceneView$$' in name and any(k in name for k in ['ArrangeScene','AlignSceneBackground','OnOrientationChange','PrepareForDialog']))
    if not selected:
        continue
    end = addresses[bisect.bisect_right(addresses, address)]
    lines = [name, method.get('Signature', ''), f'0x{address:X}; next named boundary 0x{end:X}']
    registers = {}
    decoder = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    decoder.detail = True
    for ins in decoder.disasm(read(address, end - address), address):
        operand, note = ins.op_str, ''
        if ins.mnemonic in ('bl', 'b') and operand.startswith('#0x'):
            note = methods.get(int(operand[1:], 16), {}).get('Name', '')
        if ins.mnemonic == 'adrp':
            reg, value = operand.split(', ')
            registers[reg] = (int(value[1:], 16), ins.address)
        reference = re.fullmatch(r'x\d+, \[(x\d+), #0x([0-9a-f]+)\]', operand)
        if ins.mnemonic == 'ldr' and reference and reference[1] in registers:
            base, previous = registers[reference[1]]
            if ins.address - previous <= 24:
                note = metadata.get(base + int(reference[2], 16), '')
        match = re.fullmatch(r'(s\d+|d\d+), \[(x\d+), #0x([0-9a-f]+)\]', operand)
        if ins.mnemonic == 'ldr' and match and match[2] in registers:
            base, previous = registers[match[2]]
            if ins.address - previous <= 24:
                location = base + int(match[3], 16)
                size = 4 if match[1].startswith('s') else 8
                raw = read(location, size)
                if len(raw) == size:
                    value = struct.unpack('<f' if size == 4 else '<d', raw)[0]
                    note = f'literal {value:.9g} @ 0x{location:X}; confirm base register before use'
        lines.append(f'{ins.address:08X} {ins.mnemonic:8} {operand}' + (' ; ' + note if note else ''))
        if ins.mnemonic != 'adrp':
            for reg in ins.regs_access()[1]:
                registers.pop(ins.reg_name(reg), None)
    filename = re.sub(r'[^\w.-]', '_', name.split('.')[-1]) + f'_{address:x}.txt'
    (out / filename).write_text('\n'.join(lines), encoding='utf-8')
    records.append({'name': name, 'address': hex(address), 'file': filename, 'sha256': hashlib.sha256((out / filename).read_bytes()).hexdigest()})
(out / 'manifest.json').write_text(json.dumps({'binary_sha256': digest, 'script_json_sha256': hashlib.sha256((source/'dump/dump/script.json').read_bytes()).hexdigest(), 'audit_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'tools': {name: importlib.metadata.version(name) for name in ['capstone','pyelftools']}, 'methods': records, 'limits': ['Static; no frame capture', 'Adjacent named boundary approximation', 'Linear literal/metadata annotations require manual control-flow and register validation; not a decompiler']}, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'{len(records)} method extracts')
