"""Package source-guided imagegen previews without modifying raster images."""
from pathlib import Path
from html import escape
import json
import re
import zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parent
initial = json.loads((ROOT / 'prompts.json').read_text(encoding='utf-8'))['initial_calls']
revisions = json.loads((ROOT / 'revision-records.json').read_text(encoding='utf-8'))
rev = {r['id']: r for r in revisions}
figures = [
    ('研究框架与评估顺序', 'Programmable research and sealed assessment',
     '私有过程模型、三臂信息条件、自主研究，以及封存推荐 → K1 → Q → K2。独立复测结果不反馈给 Q。',
     '九个底座任务家族；本研究六个体系。240 场，238 条符合执行合同的研究链，3,597 / 3,600 次最终测定，720 / 720 个后测阶段。三臂是信息条件；实体、参数、结构是信息作用位置，二者不同。',
     ['横向分区流程', '纵向主流程', '宽留白分区', '分隔线纵向流程']),
    ('目标表现与预测能力', 'Task performance and predictive accuracy',
     'EC、RX 各 30 个匹配比较。横轴是推荐复测得分变化，纵轴是预测 MAE 变化，均为优化目标减去探索目标。',
     '颜色区分三臂，形状区分五个复用世界。EC 空心 / 实心为 12 / 24 次预算；RX 为参数 / 结构先验。改善复测 / 改善预测 / 复测改善而预测变差：EC 26 / 14 / 13，RX 9 / 8 / 5。',
     ['双栏散点', '上下排列', '双栏宽留白', '纵排与轻网格']),
    ('增加预算后的预测变化', 'Prediction under 12- and 24-batch budgets',
     'EC 探索、EC 优化、PA 有机相分数、C 细粉率；每面板 15 条配对线，粗线表示均值，叉号标记源实验未足额执行。',
     '均值分别为 0.17378 → 0.11222、0.17811 → 0.10818、0.08291 → 0.02379、0.30999 → 0.27000。12 与 24 为独立会话；24 次也有更大操作和计算额度，不能解释为单独增加观测次数的因果效应。',
     ['标准 2 × 2', '横向四联', '纵向四联', '轻网格 2 × 2']),
    ('条件变化与响应权衡', 'Query regimes and response tradeoffs',
     'EQ 的预测误差和区间覆盖率，加上 C 在 12 次预算下相对 Opaque 的回收率—纯度 MAE 变化。',
     'EQ 是“其余九题”与“三道最稀释题”的分组，不是世界数量；五个世界均保留。80% 为名义覆盖率。C 有 10 个配对点，其中 2 个带未足额源实验标记。该分组属于探索性回顾分析。',
     ['横向三联', '纵向三联', '上二下一', '左侧双图与右侧整栏']),
    ('同数据公共基线', 'Agent forecasts versus a same-data public baseline',
     '回收率、纯度、粒径和细粉率各 30 场。横轴公共均值基线 MAE，纵轴 Agent MAE；对角线下方为 Agent 更好。',
     'Agent 胜出分别为 26 / 30、0 / 30、4 / 30、21 / 30。基线使用同场公开测定值的均值。纯度的低变异使均值基线很强；不能据此认定基线完成了机理发现。',
     ['标准 2 × 2', '横向四联', '纵向四联', '轻网格 2 × 2']),
]

records = []
for item in initial:
    ident = item['id']
    filename = ident + '.png'
    with Image.open(ROOT / filename) as im:
        im.verify()
    with Image.open(ROOT / filename) as im:
        dims = list(im.size)
    for suffix in ('.png', '.svg'):
        assert (ROOT / 'reference' / (ident + suffix)).is_file()
    if ident in rev:
        item = dict(item, source=rev[ident]['source'], prompt=rev[ident]['prompt'], reference=rev[ident]['reference'], revised=True)
    records.append(dict(item, dimensions=dims, output=filename, reference_png='reference/'+filename, reference_svg='reference/'+ident+'.svg'))
assert len(records) == 20
(ROOT / 'generation-records.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
(ROOT / 'prompts.json').write_text(json.dumps({'mode':'built-in image_gen, source-guided edits', 'initial_calls':initial, 'revision_calls':revisions}, ensure_ascii=False, indent=2), encoding='utf-8')

css = '''
:root{color-scheme:light;--ink:#202c37;--rule:#ced5da;--accent:#397a75}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:#f5f6f7;font:15px/1.6 system-ui,"Microsoft YaHei",sans-serif}a{color:#285c73}header,main,footer{max-width:1440px;margin:auto;padding:24px 36px}header{background:white;border-bottom:1px solid var(--rule)}h1{font-size:27px;margin:0 0 8px}h2{font-size:23px;margin:0 0 6px}h3{font-size:16px;margin:0}.intro{max-width:1050px}.minor{font-size:13px;color:#53616b}.toolbar{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin:18px 0 4px}.toolbar a,button{font:inherit;background:white;border:1px solid #9ba8b0;border-radius:3px;padding:7px 12px;cursor:pointer;color:var(--ink);text-decoration:none}button:hover,.toolbar a:hover{border-color:var(--accent);color:var(--accent)}.summary{position:sticky;top:0;z-index:2;background:#202c37;color:white;padding:10px 36px;display:flex;gap:20px;align-items:center;justify-content:center;flex-wrap:wrap}.summary button{font-size:13px;padding:3px 10px}.section{padding:30px 0 18px;border-bottom:1px solid var(--rule);scroll-margin-top:72px}.section>p{margin:4px 0 10px;max-width:1150px}.scope{border-left:3px solid #8797a1;padding:7px 12px;background:white;font-size:13px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:20px}.card{background:white;border:1px solid var(--rule);border-radius:3px;overflow:hidden}.card.selected{outline:3px solid var(--accent);outline-offset:1px}.cardhead{padding:12px 16px;display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:1px solid #e5e9ec}.cardhead label{white-space:nowrap;cursor:pointer}.frame{height:460px;padding:12px;display:flex;align-items:center;justify-content:center;background:white}.frame img{max-width:100%;max-height:100%;object-fit:contain}.links{padding:11px 16px;border-top:1px solid #e5e9ec;display:flex;align-items:center;gap:15px;flex-wrap:wrap;font-size:13px}.links button{font-size:13px;padding:4px 8px}.mode{color:#5b6871;font-size:12px;margin-left:auto}input{accent-color:var(--accent)}details{background:white;border:1px solid var(--rule);padding:12px 16px;margin:18px 0}summary{cursor:pointer}code{font-size:12px}footer{font-size:13px;padding-bottom:40px} @media(max-width:900px){.grid{grid-template-columns:1fr}header,main,footer{padding-left:18px;padding-right:18px}.frame{height:400px}.summary{padding:10px 18px}} @media print{.summary,.toolbar,.links{display:none}.grid{grid-template-columns:1fr 1fr}.frame{height:310px}.section{break-before:page}.card{break-inside:avoid}}
'''
parts = ['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ChemWorld NCS — 学术配图选版</title><style>'+css+'</style><header><h1>ChemWorld · NCS 学术配图选版</h1><p class="intro">5 个 Figure，每图 4 个 imagegen 预览。白底、平面图形、低饱和配色；按原文和现有数据组织，不加入写实物品或装饰插画。</p><p class="minor intro">生成预览用于挑选版式。精确底图由现有数据绘制，可切换核对并下载 SVG。Imagegen 的点位、刻度和线条不作为定量依据；投稿图应由原始数据按选定版式重绘。</p><div class="toolbar">']
parts += [f'<a href="#figure-{i}">Figure {i}</a>' for i in range(1,6)]
parts += ['<a href="chemworld-ncs-academic-previews.zip" download>下载完整包</a><a href="README.md">说明与来源</a></div></header><div class="summary"><span id="selection-summary">尚未选版</span><button id="export">导出选择</button><button id="reset">清空选择</button></div><main>']
for i,(title,en,desc,scope,layouts) in enumerate(figures,1):
    parts.append(f'<section class="section" id="figure-{i}"><h2>Figure {i} · {title}</h2><p class="minor">{en}</p><p>{desc}</p><p class="scope">{scope}</p><div class="grid">')
    for variant,layout in zip('ABCD',layouts):
        ident=f'fig{i:02d}-{variant}'
        parts.append(f'''<article class="card" data-id="{ident}"><div class="cardhead"><h3>{variant} · {layout}</h3><label><input type="radio" name="figure-{i}" value="{variant}"> 选择 {variant}</label></div><a class="frame" href="{ident}.png" target="_blank" rel="noopener"><img src="{ident}.png" loading="lazy" alt="Figure {i} variant {variant}"></a><div class="links"><button class="toggle" aria-pressed="false">切换精确底图</button><a href="{ident}.png" target="_blank" rel="noopener">打开预览</a><a href="reference/{ident}.svg" download>SVG</a><a href="reference/{ident}.png" download>底图 PNG</a><span class="mode">Imagegen 预览</span></div></article>''')
    parts.append('</div></section>')
parts.append('''<details><summary>使用说明与校对范围</summary><p>每个 Figure 独立选择 A–D；选择保存在当前浏览器，可导出 JSON 发送给合作者。点击图片可放大。切换底图可检查精确刻度、数据点和线条。</p><p>已完成版式与文字检查，修正世界图例、预算图例、填充说明和基线图脚注。生成图仍是概念预览，未做逐像素的数据忠实度认证。例如部分高密度散点和短缺叉号在生成图中不够清楚，应以 SVG 为准。Figure 5A 的 MisIndexed 图例有多余的装饰性圆点，选版时忽略，最终矢量图不包含该重复标记。</p><p>原论文图片和稿件没有被替换。初次生成的五张被修订图保留在本地 drafts 目录；压缩包只收录最终 20 个候选及对应底图。</p></details></main><footer>来源：当前 NCS Article 和既有结果分析。使用内置 image_gen 生成；源数据底图用 Matplotlib 绘制。完整提示词见 <a href="prompts.json">prompts.json</a>，生成记录见 <a href="generation-records.json">generation-records.json</a>。</footer>''')
script = '''
const storageKey='chemworld-ncs-rigorous-20260922';let selected={};try{selected=JSON.parse(localStorage.getItem(storageKey)||'{}')}catch(e){}
function refresh(){document.querySelectorAll('.card').forEach(c=>{const r=c.querySelector('input');r.checked=selected[r.name]===r.value;c.classList.toggle('selected',r.checked)});document.getElementById('selection-summary').textContent=Array.from({length:5},(_,i)=>`Fig ${i+1}: ${selected['figure-'+(i+1)]||'—'}`).join('   ·   ');try{localStorage.setItem(storageKey,JSON.stringify(selected))}catch(e){}}
document.querySelectorAll('.card input').forEach(r=>r.addEventListener('change',()=>{selected[r.name]=r.value;refresh()}));
document.querySelectorAll('.toggle').forEach(b=>b.addEventListener('click',()=>{const c=b.closest('.card'),on=b.getAttribute('aria-pressed')!=='true',p=(on?'reference/':'')+c.dataset.id+'.png';c.querySelector('img').src=p;c.querySelector('.frame').href=p;b.setAttribute('aria-pressed',String(on));b.textContent=on?'切换生成预览':'切换精确底图';c.querySelector('.mode').textContent=on?'源数据精确底图':'Imagegen 预览'}));
document.getElementById('export').addEventListener('click',()=>{const blob=new Blob([JSON.stringify({collection:'ChemWorld NCS rigorous previews',selection:selected,note:'Layout selection only. Re-render publication plots from source data.'},null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='chemworld-ncs-figure-selection.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),2000)});
document.getElementById('reset').addEventListener('click',()=>{selected={};refresh()});refresh();
'''
parts.append('<script>'+script+'</script></html>')
page=''.join(parts)
(ROOT / 'index.html').write_text(page, encoding='utf-8')
(ROOT / 'gallery.js').write_text(script, encoding='utf-8')

readme='''# ChemWorld NCS：严格学术风格配图预览

打开 `index.html`，每个 Figure 有 A–D 四版，共 20 张 imagegen 生成图。图中文字为英文。可选择每图一个版本，导出 JSON；可切换精确数据底图并下载 SVG。

## 交付内容

- `fig01-A.png` 至 `fig05-D.png`：最终 20 张生成预览。
- `reference/`：相同 20 个版式的 PNG 和可编辑 SVG，直接从既有分析数据绘制。
- `prompts.json`：内置 image_gen 的 20 次初始生成及 5 次修订提示词。
- `generation-records.json`：最终输出与来源对应关系。
- `render_reference.py`：底图绘图脚本；在本仓库内通过 `uv run --no-sync python output/imagegen/ncs-rigorous-20260922/render_reference.py` 运行。
- `build_gallery.py`：打包和文件验证脚本，不编辑生成图像。

## 使用界限

这些是选版预览，不是已经验证的投稿定量图。数据面板、逐场比较、配对线、图例和分母均以源数据底图为依据，imagegen 生成仍可能改变局部点位、刻度间距、重叠标记或字形。正式投稿应从数据生成最终矢量图，不能把生成位图直接作为数值证据。没有运行新实验，也没有替换任何稿件或论文原图。

已检查 20 张生成图的风格和整体构成；修正 Figure 2A 的 W01 图例、Figure 2D 的填充标签、Figure 5A 的 12 次预算图例、Figure 5B 横向排版、Figure 5D 脚注。Figure 5A 修订后 MisIndexed 图例仍有一个多余圆点，属于预览层排版瑕疵；SVG 中没有这个问题。高密度面板的单个标记不保证由 imagegen 完整复现。

## 图的组织

1. 平台、三臂、自主实验及封存后测的流程。
2. EC / RX 优化表现与预测能力的配对关系。
3. EC / PA / C 的 12 与 24 次预算比较。
4. EQ 查询条件变化及 C 响应间权衡。
5. C 四响应与同场公开观测均值基线的比较。

## 科学内容来源

- `paper/venues/ncs/article.md`
- `paper/figures/integrated-results/analysis.json`
- `paper/figures/integrated-results/campaign_metrics.csv`
- `workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/STORY_WORLD_ANALYSIS.json`
- `workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json`

底图脚本验证 EC / RX 各 30 个目标配对、每个预算面板 15 个配对、C 基线胜出数 26 / 0 / 4 / 21。所有展示均来自已有证据；没有新增因果结论或显著性标记。
'''
(ROOT / 'README.md').write_text(readme, encoding='utf-8')

files=[ROOT/r['output'] for r in records]+sorted((ROOT/'reference').glob('*'))
files += [ROOT/n for n in ('index.html','README.md','prompts.json','generation-records.json','revision-records.json','reference-manifest.json','render_reference.py','build_gallery.py','gallery.js')]
archive=ROOT/'chemworld-ncs-academic-previews.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files: z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z: assert z.testzip() is None
for link in re.findall(r'(?:href|src)="([^"]+)"',page):
    if not link.startswith(('#','http')): assert (ROOT/link).is_file(),link
report={'generated_previews':len(records),'reference_pngs':len(list((ROOT/'reference').glob('*.png'))),'reference_svgs':len(list((ROOT/'reference').glob('*.svg'))),'revision_calls':len(revisions),'archive_files':len(files),'archive_bytes':archive.stat().st_size,'png_readability':'all passed','gallery_local_links':'all passed','numeric_authority':'source-data SVG/PNG only'}
(ROOT/'VALIDATION.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
