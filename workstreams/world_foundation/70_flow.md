# WF-70 连续流

范围：geometry-resolved PFR、residence time、heat boundary、pressure drop 和 solver diagnostics。

Owned paths：`pfr_reactors.py` 与 flow 专属 cards/fixtures/tests。reaction/property 通过 WF-00 protocol
注入，不直接改其它团队实现。

不修改：runtime flow service、task action space、reaction core internals。

交付：等温/绝热、零反应、短/长管、层流/湍流边界和压降失败 reference cases；新版 reaction
provider adapter proposal。详细要求见主清单 WF-08。
