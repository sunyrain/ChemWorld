# ChemLab-Assets 三仪器预览

独立的本地只读试接：IKA RCT digital 加热搅拌器、Metrohm 914 pH 仪、Hach DR6000
UV–Vis。旋转、缩放、点击部件、下拉选择、关节滑块、复位、线框、自动旋转。
使用已有 Three.js 0.169.0，无新增 Python/Node 依赖。

首次下载并启动：

```powershell
uv run --no-sync python -m apps.asset_preview --download
```

打开 **http://127.0.0.1:8895/**。此后直接运行 `uv run --no-sync python -m apps.asset_preview`，
浏览器与服务均无需外网。端口可用 `--port` 修改，缓存可用 `--cache` 指定。
`--download-only` 只下载；重复下载由用户显式请求，不在服务器启动时自动联网。

模型、完整原版部件摘要、许可和来源版本存放在 Git 已忽略的
`reference_repos/chemlab-assets-preview/`。下载器固定上游代码版本，解析数据集版本后
使用该版本下载三份 GLB，保留来源索引和原始许可证；不下载或执行第三方仪器运行时。
三个 GLB 合计 4,018,116 bytes。该缓存是可选第三方资产，不随 ChemWorld MIT 核心分发。

## 公开记录联动

“查看公开记录”按原顺序读取 `apps/blender_lab/static/demo.json` 中已有的八步开发示例。
加热映射到搅拌器类别，UV–Vis 测量映射到光度计类别；品牌与型号只是外观示意。
原记录没有 pH 测量，所以不为 pH 仪补造示例读数。终检不映射为 UV–Vis。
观测面板仅呈现所选快照中 `observed_mask=true` 的有限数值，并明确可能沿用先前观测。
初始缺测保持空白。关节滑块不触发实验，记录跳转不重新运行核心，也不调用模型。
屏幕纹理属于原始模型外观，实际 ChemWorld 观测始终在独立面板中显示。

## 来源与许可

- [ChemLab-Assets](https://github.com/mbzuai-nlp/ChemLab-Assets), release 1.0,
  Zirui Song, Jiadong Zhang, Jiahao Zhang, Xiaojun Chang, Xiaosong Ma, Xiuying Chen / MBZUAI (2026)。
- 模型、元数据等是 **CC BY-NC 4.0**；缓存保留 `LICENSE-ASSETS.md`、`NOTICE.md`、`CITATION.cff`。
  几何和元数据未修改；本预览增加独立呈现及公开记录映射，不声称该型号物理性能已验证。
- `app.mjs` 的关节枢轴及朝向适配参考其 MIT Explorer；署名与许可见 [THIRD_PARTY.md](THIRD_PARTY.md)。
- Three.js / GLTFLoader / OrbitControls 复用 `apps/blender_lab/static/vendor/` 的 MIT 版本。

## 定向检查

```powershell
uv run --no-sync pytest tests/test_asset_preview.py -q
uv run --no-sync ruff check apps/asset_preview tests/test_asset_preview.py
node --test apps/asset_preview/test_projection.mjs
node --check apps/asset_preview/static/app.mjs
```

这是展示功能验收，不产生科学实验数据，不更新冻结证据或论文。

2026-10-15 当前试用交付：三个 GLB 容器读取通过，56/56 部件具有匹配的模型节点，
18/18 页面、模型与许可 HTTP 资源可读；Python 8/8、JavaScript 3/3、Ruff、mypy 和
JavaScript 语法检查通过。浏览器连接不可用，Windows Computer Use 随后未获准控制 Edge。
用户选择自行打开预览，先交付当前版本；因此 **尚未完成实际渲染和鼠标/触摸交互验收**，
不能把资源/静态检查写成视觉验收通过。服务在本机 8895 运行，重启方式见上文。

适配说明：pH 仪的三枚按键在 GLB 中以按键网格命名、URDF 中则以另一组 link 名称命名；
本预览显式连接按键与字样网格。UV-Vis 舱盖使用原 GLB `lid_hinge` 父节点，连同把手一起转动。
这只修正呈现绑定，不修改下载的模型或赋予新的仪器能力。
