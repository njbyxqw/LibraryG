# -*- coding: utf-8 -*-
"""
TileV2 关卡可视化预览器 - 本地服务器
启动后访问 http://127.0.0.1:8790/
用法: python level_viz_server.py [端口]
"""
import http.server, json, os, re, subprocess, urllib.parse

CLIENT = r'D:/meatloaf_client01/client'
ROOTS = {
    'runtime': os.path.join(CLIENT, r'Assets/Game/TileV2/Config/LevelConfig'),
    'editor':  os.path.join(CLIENT, r'Assets/Game/TileV2/Editor/LevelConfig/Levels'),
}
HERE = os.path.dirname(os.path.abspath(__file__))


def git_show(rel_path):
    try:
        r = subprocess.run(['git', '-C', CLIENT, 'show', 'HEAD:' + rel_path.replace('\\', '/')],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def resolve(path):
    """将客户端路径解析为绝对路径，防目录穿越；仅返回真实存在的文件"""
    if os.path.isabs(path):
        full = os.path.normpath(path)
        return full if os.path.isfile(full) else None
    for root in ROOTS.values():
        full = os.path.normpath(os.path.join(root, path))
        try:
            if os.path.commonpath([full, os.path.normpath(root)]) == os.path.normpath(root) \
                    and os.path.isfile(full):
                return full
        except ValueError:
            continue
    return None


def _which_root(full):
    """返回 full 所属的 ROOTS 根；不在任何根内时返回 None"""
    full = os.path.normpath(full)
    for root in ROOTS.values():
        try:
            if os.path.commonpath([full, os.path.normpath(root)]) == os.path.normpath(root):
                return root
        except ValueError:
            continue
    return None


def _nat_key(s):
    """自然排序 key：把字符串拆成 数字/非数字 段，数字段按数值升序、字母段忽略大小写。
    支持任意位置的数字（如 20_TE.json、TS001.json），1 < 2 < 10"""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]


def _file_key(f):
    """按完整路径做自然排序（path 相同则回退到 name）"""
    return _nat_key(f['path']) + [_nat_key(f['name'])]


def scan_dir(path, recursive=True):
    """扫描关卡路径（目录或单个文件），返回 {'dir':显示名, 'files':[{name,path}]}
    path 可为空(默认运行时根)、相对 ROOTS 的子路径、或本地绝对路径"""
    if not path:
        full = os.path.normpath(ROOTS['runtime'])
        disp = 'Config/LevelConfig'
    elif os.path.isabs(path):
        full = os.path.normpath(path)
        disp = full
    else:
        full = None
        disp = path
        for root in ROOTS.values():
            cand = os.path.normpath(os.path.join(root, path))
            try:
                if os.path.commonpath([cand, os.path.normpath(root)]) != os.path.normpath(root):
                    continue
            except ValueError:
                continue
            if os.path.isdir(cand) or os.path.isfile(cand):
                full = cand
                disp = os.path.relpath(cand, root).replace('\\', '/') or '<根目录>'
                break
    if not full or not (os.path.isdir(full) or os.path.isfile(full)):
        return None
    files = []
    if os.path.isfile(full):
        base = _which_root(full)
        files.append({'name': os.path.basename(full),
                      'path': os.path.relpath(full, base).replace('\\', '/') if base else full})
    elif recursive:
        for dp, _, fns in os.walk(full):
            for fn in sorted(fns):
                if fn.endswith('.json'):
                    fp = os.path.join(dp, fn)
                    base = _which_root(fp)
                    files.append({'name': fn,
                                  'path': os.path.relpath(fp, base).replace('\\', '/') if base else fp})
    else:
        for fn in sorted(os.listdir(full)):
            if fn.endswith('.json'):
                fp = os.path.join(full, fn)
                base = _which_root(fp)
                files.append({'name': fn,
                              'path': os.path.relpath(fp, base).replace('\\', '/') if base else fp})
    files.sort(key=_file_key)
    return {'dir': disp, 'files': files}


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        try:
            if u.path == '/':
                html = open(os.path.join(HERE, 'level_viz.html'), 'rb').read()
                self._send(200, html, 'text/html; charset=utf-8')
            elif u.path == '/api/list':
                out = []
                for key, root in ROOTS.items():
                    files = []
                    if key == 'runtime':
                        for fn in sorted(os.listdir(root)):
                            if fn.endswith('.json'):
                                files.append({'name': fn, 'path': fn})
                    else:
                        for dp, _, fns in os.walk(root):
                            for fn in sorted(fns):
                                if fn.endswith('.json'):
                                    rel = os.path.relpath(os.path.join(dp, fn), root).replace('\\', '/')
                                    files.append({'name': rel, 'path': rel})
                    files.sort(key=_file_key)
                    out.append({
                        'key': key,
                        'name': '运行时配置 Config/LevelConfig' if key == 'runtime' else '编辑器关卡 Editor/Levels',
                        'files': files,
                    })
                self._send(200, json.dumps({'groups': out}).encode('utf-8'), 'application/json; charset=utf-8')
            elif u.path == '/api/scan':
                q = urllib.parse.parse_qs(u.query)
                dirp = (q.get('dir') or [''])[0]
                recursive = (q.get('recursive') or ['1'])[0] != '0'
                res = scan_dir(dirp, recursive)
                if res is None:
                    self._send(404, json.dumps({'error': '路径不存在: ' + dirp}).encode('utf-8'),
                               'application/json; charset=utf-8')
                else:
                    self._send(200, json.dumps(res).encode('utf-8'),
                               'application/json; charset=utf-8')
            elif u.path == '/api/load':
                q = urllib.parse.parse_qs(u.query)
                path = (q.get('path') or [''])[0]
                full = resolve(path)
                if not full or not os.path.isfile(full):
                    self._send(404, json.dumps({'error': '文件不存在: ' + path}).encode('utf-8'),
                               'application/json; charset=utf-8')
                    return
                data = json.load(open(full, encoding='utf-8'))
                base = None
                if 'base' in q:
                    # git 仓库根在 client 上一级，需带 client/ 前缀
                    rel = 'client/' + os.path.relpath(full, CLIENT).replace('\\', '/')
                    s = git_show(rel)
                    if s:
                        try:
                            base = json.loads(s)
                        except Exception:
                            base = None
                self._send(200, json.dumps({'data': data, 'base': base}).encode('utf-8'),
                           'application/json; charset=utf-8')
            elif u.path == '/favicon.ico':
                self._send(204, b'', 'image/x-icon')
            else:
                self._send(404, b'not found', 'text/plain')
        except Exception as e:
            self._send(500, json.dumps({'error': str(e)}).encode('utf-8'), 'application/json; charset=utf-8')


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8790
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print('TileV2 关卡可视化预览器: http://127.0.0.1:%d/' % port)
    srv.serve_forever()
