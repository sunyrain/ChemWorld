// Presentation rules: a selected device never creates a measurement.
export function frameAsset(frame) {
  if (!['accepted', 'committed'].includes(frame.status)) return null;
  if (frame.operation === 'heat') return 'ika_plate_rctdigital';
  if (frame.operation === 'measure' && frame.instrument === 'uvvis') return 'hach_dr6000';
  if (frame.operation === 'measure' && frame.instrument === 'ph_meter') return 'metrohm_914';
  return null;
}

export function visibleMetrics(frame) {
  return Object.entries(frame.observations ?? {}).filter(([key, value]) =>
    frame.observed_mask?.[key] === true && typeof value === 'number' && Number.isFinite(value));
}

export const OPERATIONS = {add_solvent:'加入溶剂',add_reagent:'加入试剂',add_catalyst:'加入催化剂',heat:'加热',sample:'取样',measure:'仪器测量',terminate:'结束加工'};
export const METRICS = {yield:'产率',selectivity:'选择性',conversion:'转化率',purity:'纯度',recovery:'回收率',byproduct_signal:'副产物信号',degradation_warning:'降解信号',virtual_spectrum_summary:'虚拟谱图摘要',pH_normalized:'归一化 pH',acid_dissociation_fraction:'解离比例'};
