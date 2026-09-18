import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { parseHandoff } from '../src/handoff.mjs';
import { renderWebMcpInboxPage } from '../src/webmcp-inbox-page.mjs';

test('裸 JSON、代码块、Windows 换行完整保留方案，拒绝损坏的包', () => {
  const text = JSON.stringify({title:'验收', conclusion:'第一行\n第二行'});
  for (const value of [text, '```json\n'+text+'\n```', '```JSON\r\n'+text+'\r\n```']) {
    assert.deepEqual(parseHandoff(value), JSON.parse(text));
  }
  for (const value of ['', '[]', 'null', '```json\n{}', '说明\n{}']) assert.throws(() => parseHandoff(value));
});

test('浏览器实际收到的脚本可编译，代码块解析没有模板转义损坏', () => {
  const script = renderWebMcpInboxPage().match(/<script type="module">([\s\S]*?)<\/script>/)[1];
  new vm.Script('(async()=>{'+script+'})');
  const context = vm.createContext({});
  vm.runInContext(script.slice(script.indexOf('function parseHandoff'), script.indexOf('async function createTask')), context);
  assert.equal(context.parseHandoff('```json\n{"title":"原样"}\n```').title, '原样');
});
