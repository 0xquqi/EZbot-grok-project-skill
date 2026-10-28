#!/usr/bin/env python3
"""Build or check the self-contained prompt and the versioned delivery archive."""
import argparse
import hashlib
import json
import re
import string
import subprocess
import zipfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/ezbot-grok-scout'
ORDER = ['SKILL.md', 'assets/defaults.json', 'assets/messages.json',
         'references/grok-runtime.md', 'references/startup.md', 'references/discovery-state.md',
         'references/research-flow.md', 'references/mechanism-questions.md',
         'references/fees-contracts.md', 'references/output.md', 'references/sources.md']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError('Run without -O: validation assertions must remain enabled')
    docs = {name: (SKILL/name).read_text(encoding='utf-8') for name in ORDER}
    front = re.match(r'^---\n(.*?)\n---\n', docs['SKILL.md'], re.S)
    assert front, 'Missing YAML frontmatter'
    ruby = 'puts JSON.generate(YAML.safe_load(STDIN.read, permitted_classes: [], permitted_symbols: [], aliases: false))'
    meta = json.loads(subprocess.check_output(['ruby', '-ryaml', '-rjson', '-e', ruby], input=front[1], text=True))
    assert set(meta) <= {'name','description','license','allowed-tools','metadata'}
    assert meta['name'] == SKILL.name
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', meta['name']) and len(meta['name']) <= 64
    assert isinstance(meta['description'],str) and 0 < len(meta['description']) <= 1024
    assert '<' not in meta['description'] and '>' not in meta['description']
    assert not re.search(r'^\s*\[TODO:.*\]\s*$', docs['SKILL.md'], re.M)
    version = meta['metadata']['version']
    defaults = json.loads(docs['assets/defaults.json'])
    messages = json.loads(docs['assets/messages.json'])
    assert defaults['skill_version'] == version
    assert defaults['initial_lookback_minutes'] == 60
    assert defaults['accounts'] == [] and defaults['interval_minutes'] is None
    assert all(defaults[k] is False for k in ['schedule_enabled','export_files_by_default','external_notifications_enabled','public_publishing_enabled'])
    assert messages['card_attribution'] == 'Skill 作者：@0xquqi'
    values = dict(window_start='2026-10-28 14:00', window_end='2026-10-28 15:00', timezone='Asia/Shanghai',run_mode='本次单次搜索，未开启定时监测', **messages)
    fields = {name for _,name,_,_ in string.Formatter().parse(messages['startup_template']) if name}
    assert fields <= values.keys()
    rendered = messages['startup_template'].format(**values)
    assert '{' not in rendered and messages['disclaimer'] in rendered
    assert messages['customization_help'] in rendered
    assert all('**' not in v for v in messages.values() if isinstance(v, str))
    assert '**' not in rendered and '**' not in docs['references/output.md']
    assert messages['first_completion_title'] == '首轮试运行结束'
    assert messages['completion_title'] == '本轮运行结束'
    # Render success, empty, and incomplete variants with real-shaped values.
    # This validates template interpolation, not the Bot's delivery behavior.
    rendered_endings = []
    for title in [messages['first_completion_title'], messages['completion_title']]:
        for template in ['completion_template', 'completion_empty_template']:
            ending_values = dict(values, completion_title=title,
                result_summary='本轮介绍3个项目，另补充1条已结束活动动态。',
                followup_hint='你可以回复“展开第2个项目”，或调整搜索设置。',
                material_limitation='跨轮状态保存失败，已交付结果不受影响。')
            ending = messages[template].format(**ending_values)
            assert ending.startswith(f'{title}。') and '{' not in ending and '**' not in ending
            rendered_endings.append(ending)
    incomplete = messages['incomplete_template'].format(reason='公开搜索暂时不可用。',
        delivered_summary='已交付1条待核实线索。', next_step='恢复后可继续本轮。')
    assert incomplete.startswith('本轮未完成。') and '{' not in incomplete and '**' not in incomplete
    links = 0
    for rel, body in docs.items():
        if not rel.endswith('.md'): continue
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',body):
            if '://' in link or link.startswith('#'): continue
            dest = ((SKILL/rel).parent/link.split('#')[0]).resolve()
            assert dest.is_relative_to(SKILL.resolve()) and dest.is_file(), (rel,link)
            assert dest.relative_to(SKILL).as_posix() in docs, (rel,link,'not embedded')
            links += 1
    content_id = sha(json.dumps({k: sha(v.encode('utf-8')) for k, v in docs.items()}, sort_keys=True).encode())
    prompt = (f'EZbot 项目发现与研究 v{version}\nSkill 作者：@0xquqi\n内容标识：{content_id}\n\n'
              '以下是完整工作流，章节标题与Skill文件路径对应；所有必要引用均已展开，无需访问本地路径。'
              '按用户请求启动、研究或调整设置；仅阅读本附件不自动运行。方法以此版本为准，用户明确设置优先；'
              '涉及范围冲突先说明，不擅自改动既有定时计划。\n\n')
    prompt += '\n\n'.join(f'===== {rel} =====\n{docs[rel].rstrip()}' for rel in ORDER) + '\n'
    files = {str((SKILL/rel).relative_to(ROOT)): docs[rel].encode('utf-8') for rel in ORDER}
    files['GrokBot完整提示词.txt'] = prompt.encode('utf-8')
    for rel in ['开始使用.txt','给现有Grok对话的纠正指令.txt','LICENSE']:
        files[rel] = (ROOT/rel).read_bytes()
    for rel,data in files.items():
        body=data.decode('utf-8')
        assert '/Users/' not in body and '/private/' not in body, rel
        assert '声称发现的5个' not in body, rel
    provenance=json.loads((ROOT/'evaluation/source-provenance.json').read_text())
    review=json.loads((ROOT/'evaluation/review.json').read_text())
    assert review['version'] == version and review['method'] == 'manual-rule-review'
    manifest={'schema_version':3,'version':version,'skill_content_sha256':content_id,
      'files':{rel:sha(data) for rel,data in files.items()},'upstream':provenance,
      'validation':{'yaml_parser':'Ruby Psych safe_load','frontmatter_constraints':'passed',
        'local_links':{'status':'passed','count':links},'configuration':'passed',
        'startup_rendering':'passed',
        'visible_template_format':'plain text labels; no Markdown emphasis markers',
        'completion_rendering':{'status':'passed','success_and_empty_variants':len(rendered_endings),'incomplete_variant':True},
        'self_contained_prompt':'all skill source files embedded verbatim',
        'package_scope':'public instructions and configuration only; no runtime state or personal paths',
        'quick_validate_py':'not run in this build; Ruby Psych parses YAML; not claimed passed',
        'scenario_review':review,
        'grok_documentation_review':json.loads((ROOT/'evaluation/grok-capability-review.json').read_text()),
        'grok_bot_forward_test':'not_run'}}
    manifest_bytes=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    files['交付校验.json']=manifest_bytes
    archive=ROOT/f'EZbot-Grok-Scout-v{version}.zip'
    if args.check:
        for rel,data in files.items():
            assert (ROOT/rel).read_bytes() == data, f'Stale delivery file: {rel}'
    else:
        (ROOT/'GrokBot完整提示词.txt').write_bytes(files['GrokBot完整提示词.txt'])
        (ROOT/'交付校验.json').write_bytes(manifest_bytes)
        buffer=BytesIO()
        with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as z:
            for rel,data in files.items():
                info=zipfile.ZipInfo(f'EZbot-Grok-Scout-v{version}/{rel}',(2026,10,28,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o100644 << 16
                z.writestr(info,data)
        archive.write_bytes(buffer.getvalue())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        expected={f'EZbot-Grok-Scout-v{version}/{rel}':data for rel,data in files.items()}
        assert set(z.namelist()) == set(expected)
        assert all(z.read(name)==data for name,data in expected.items())
    print(json.dumps({'version':version,'mode':'check' if args.check else 'build','files':len(files),
        'prompt_characters':len(prompt),'zip_bytes':archive.stat().st_size,
        'zip_sha256':sha(archive.read_bytes()),'result':'passed','grok_bot_test':'not_run'},ensure_ascii=False))

if __name__=='__main__':
    main()
