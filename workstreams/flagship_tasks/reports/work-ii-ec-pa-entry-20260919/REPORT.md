# EC预测题与PA先验入口验证

development；固定参考，无模型来源。

完成15/15批、99/99操作；通过15/15单元，精确重放通过15/15；耗时27.59秒。

重放另计15计划批，已核对99/99操作；0 provider调用、0重试；失败和未执行保留分母。

| EC题 | 条件组 | 电位域 | 产率 | 综合分 | 通过 |
| --- | --- | --- | ---: | ---: | --- |
| Q01 | short | negative | 0.002021779539063573 | 0.03265897557139397 | True |
| Q02 | short | positive | 0.013318453915417194 | 0.3494912087917328 | True |
| Q03 | long | negative | 0.08089765906333923 | 0.35898518562316895 | True |
| Q04 | long | positive | 0.19362318515777588 | 0.5720124840736389 | True |
| Q05 | electrolyte_1 | negative | 0.07626529037952423 | 0.36235904693603516 | True |
| Q06 | electrolyte_1 | positive | 0.23458951711654663 | 0.6275988817214966 | True |
| Q07 | electrolyte_3 | negative | 0.06711229681968689 | 0.3478533923625946 | True |
| Q08 | electrolyte_3 | positive | 0.16522285342216492 | 0.5429551601409912 | True |
| Q09 | solvent_2 | negative | 0.044986847788095474 | 0.28822582960128784 | True |
| Q10 | solvent_2 | positive | 0.14248453080654144 | 0.49437618255615234 | True |
| Q11 | current_cap | negative | 0.1362166702747345 | 0.2764512300491333 | True |
| Q12 | current_cap | positive | 0.19715233147144318 | 0.3448810577392578 | True |

| 电位域 | 题数 | 产率范围 | 产率低于0.02 |
| --- | ---: | --- | ---: |
| negative | 6 | 0.00202–0.13622 | 1 |
| positive | 6 | 0.01332–0.23459 | 1 |

成对差为正电位减负电位，仅作描述；每种条件只有一次固定参考，不是显著性检验或完整机理辨识。

| 条件组 | 产率差 | 综合分差 |
| --- | ---: | ---: |
| short | 0.01130 | 0.31683 |
| long | 0.11273 | 0.21303 |
| electrolyte_1 | 0.15832 | 0.26524 |
| electrolyte_3 | 0.09811 | 0.19510 |
| solvent_2 | 0.09750 | 0.20615 |
| current_cap | 0.06094 | 0.06843 |

| PA条件 | 完成批数 | 操作数 | 匿名工具回复 | 通过 |
| --- | ---: | ---: | --- | --- |
| Opaque | 1 | 9 | True | True |
| Aligned | 1 | 9 | True | True |
| MisIndexed | 1 | 9 | True | True |

```json
{
  "pa_actions_and_observations_same_across_arms": true,
  "all_material_replies_delivered": true,
  "opaque_without_dossier": true,
  "solvent_dossier_unchanged": true,
  "extractant_properties_transposed": true,
  "public_catalog_same": true
}
```

参考合法性、匿名送达与物理不变性不代表Agent学会规律，亦不代表正式三臂已执行。EC题目在本次执行前固定，低响应或零差异也保留；没有按输出重新选题。
