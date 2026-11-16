import tempfile
import unittest
from pathlib import Path
from lanhu_unity import Prefab, plan, apply, verify, rollback, write_json, project_path, expand_nested


def node(k, name, parent=0, amin=(.5,.5), amax=(.5,.5), size=(100,100), pos=(0,0), scale=(1,1,1)):
    go=k+100
    return f'''--- !u!1 &{go}
GameObject:
  m_Name: {name}
  m_IsActive: 1
--- !u!224 &{k}
RectTransform:
  m_GameObject: {{fileID: {go}}}
  m_Father: {{fileID: {parent}}}
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalScale: {{x: {scale[0]}, y: {scale[1]}, z: {scale[2]}}}
  m_AnchorMin: {{x: {amin[0]}, y: {amin[1]}}}
  m_AnchorMax: {{x: {amax[0]}, y: {amax[1]}}}
  m_AnchoredPosition: {{x: {pos[0]}, y: {pos[1]}}}
  m_SizeDelta: {{x: {size[0]}, y: {size[1]}}}
  m_Pivot: {{x: 0.5, y: 0.5}}
'''


class ImportChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve()
        self.asset=self.root/'panel.prefab'
        self.asset.write_text(node(1,'Panel')+node(2,'Parent',1,scale=(2,2,1))+node(3,'Child',2))
        self.manifest=self.root/'mapping.json';self.report=self.root/'report'
        self.spec={'version':1,'prefabs':[{'path':'panel.prefab','referenceSize':[1080,2340],'mappings':[{'target':'Panel/Parent/Child','rect':[100,200,300,400],'reason':'test'}]}]}
        write_json(self.manifest,self.spec)

    def tearDown(self):self.tmp.cleanup()

    def test_scaled_parent_projection(self):
        f=Prefab(self.asset.read_text(),[1080,2340]);f.set_rect(3,[100,200,300,400])
        self.assertEqual(f.geometry(3),([100,1740],[150,200],[2,2]))

    def test_stretched_parent_projection(self):
        f=Prefab(node(1,'Panel')+node(2,'Child',1,amin=(0,0),amax=(1,1),size=(0,0)),[1080,2340])
        f.set_rect(2,[90,132,898,282]);self.assertEqual(f.geometry(2),([90,1926],[898,282],[1,1]))

    def test_bottom_fixed_content_on_short_screen(self):
        self.asset.write_text(node(1,'Panel')+node(2,'Content',1,amin=(0,0),amax=(1,1),size=(0,0)))
        self.spec['prefabs'][0]['mappings']=[{'target':'Panel/Content','rect':[0,0,1080,2340],'layout':{'m_AnchorMin':[0,0],'m_AnchorMax':[1,0],'m_Pivot':[.5,0]},'reason':'Bottom-aligned fixed-height scene'}]
        write_json(self.manifest,self.spec);plan(self.manifest,self.root,self.report);apply(self.root,self.report)
        f=Prefab(self.asset.read_text(),[1080,1920])
        self.assertEqual(f.geometry(2),([0,0],[1080,2340],[1,1]))

    def test_apply_verify_rollback_and_idempotence(self):
        before=self.asset.read_bytes();plan(self.manifest,self.root,self.report);apply(self.root,self.report)
        verify(self.root,self.report)
        p2=plan(self.manifest,self.root,self.root/'second')
        self.assertEqual(p2['audits'][0]['beforeSHA256'],p2['audits'][0]['afterSHA256'])
        rollback(self.root,self.report);self.assertEqual(before,self.asset.read_bytes())

    def test_changed_baseline_refused(self):
        plan(self.manifest,self.root,self.report);self.asset.write_text(self.asset.read_text()+'\n')
        with self.assertRaisesRegex(ValueError,'Input changed'):apply(self.root,self.report)

    def test_later_edits_block_rollback(self):
        plan(self.manifest,self.root,self.report);apply(self.root,self.report);self.asset.write_text(self.asset.read_text()+'\n')
        with self.assertRaisesRegex(ValueError,'later work'):rollback(self.root,self.report)

    def test_nonvisual_field_refused(self):
        self.spec['prefabs'][0]['mappings'][0]['style']={'m_text':'100/100'};write_json(self.manifest,self.spec)
        with self.assertRaisesRegex(ValueError,'Unsupported style'):plan(self.manifest,self.root,self.report)

    def test_path_escape_refused(self):
        with self.assertRaises(ValueError):project_path(self.root,'../outside')

    def test_nested_override_roundtrip(self):
        guid='f'*32
        source=self.root/'nested.prefab';source.write_text(node(10,'Nested')+node(11,'Child',10))
        Path(str(source)+'.meta').write_text('guid: '+guid)
        instance=f'''--- !u!1001 &999
PrefabInstance:
  m_Modification:
    m_TransformParent: {{fileID: 2}}
    m_Modifications:
    m_RemovedComponents: []
    m_RemovedGameObjects: []
    m_AddedGameObjects: []
    m_AddedComponents: []
  m_SourcePrefab: {{fileID: 100100000, guid: {guid}, type: 3}}
'''
        self.asset.write_text(self.asset.read_text()+instance)
        self.spec['prefabs'][0]['nestedPrefabs']=[{'instance':999,'source':'nested.prefab'}]
        self.spec['prefabs'][0]['mappings'][0]['target']='Panel/Parent/Nested/Child'
        write_json(self.manifest,self.spec);plan(self.manifest,self.root,self.report);apply(self.root,self.report)
        f=Prefab(self.asset.read_text(),[1080,2340]);expand_nested(f,self.spec['prefabs'][0]['nestedPrefabs'][0],self.root,{})
        self.assertEqual(f.geometry(f.transform('Panel/Parent/Nested/Child')),([100,1740],[150,200],[2,2]))
        self.assertEqual(source.read_text(),node(10,'Nested')+node(11,'Child',10))


if __name__=='__main__':unittest.main()
