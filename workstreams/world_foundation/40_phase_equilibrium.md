# WF-40 相平衡、萃取与洗涤

范围：LLE、activity、flash、phase stability、tie-line、entrainment 和多级 extraction/wash。

Owned paths：`extraction_*.py`、`flash_*.py`、相平衡专属实现/cards/tests。共享 property 只通过 WF-00
provider protocol 获取。

不修改：dry/concentrate/transfer、runtime phase services、partition task/scenario。

交付：单相/两相极限、极端 K、相反转、不收敛和物料闭合参考证据；匿名虚拟物系与真实语义
property profile 分离。详细要求见主清单 WF-05。
