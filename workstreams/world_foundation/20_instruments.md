# WF-20 仪器与谱图

范围：sample preparation → raw signal → calibration/processing → public estimate；HPLC、GC、UV–vis、
pH 以及正式任务实际启用的谱图通道。

Owned paths：`spectroscopy*.py`、`chromatography*.py`、`nmr*.py`、`mass_spectrometry*.py`、模块
专属 instrument schema/fixtures/tests。`world/spectra.py` 的替代方案由本模块提交，最终切换由 110
执行。

不修改：observation runtime、task instrument list、final scoring、golden trajectory。

交付：LOD/LOQ、校准、共峰、漂移、饱和、replicate 与 identifiability reference cases；final assay
和 evaluator truth 的分离方案。详细要求见主清单 WF-03。
