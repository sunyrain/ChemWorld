# WF-110 Runtime 接入与下一版冻结

本模块是共享文件的唯一所有者；在物理模块开发期间不与其它团队并行修改 shared files。

独占 paths：`tasks.py`、World Law、runtime registry/profile/domain services、world kernels、顶层 exports、
正式 docs、golden、benchmark validation 和 release artifacts。

集成顺序：

1. 验证模块 card、reference evidence 和 WF-00 protocol；
2. 接入一个模块并删除对应正式 fallback；
3. 运行 operation → model 可达性和守恒审计；
4. 每次接入保持测试可运行，所有模块完成后提升 World Law；
5. 重建任务 hash、golden、15-task consistency、serious baseline、response surface 和 replay；
6. 发布新 benchmark contract，不覆盖 v1。

验收：共享文件无跨团队冲突，正式 runtime 不存在隐式双路由，wheel 可复现新 World Law，所有
成熟度声明均由实际调用与证据自动生成。
