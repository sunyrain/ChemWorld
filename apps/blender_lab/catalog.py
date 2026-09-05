"""Single source of truth for ChemLab assets. Coordinates in metres, Z up."""

from copy import deepcopy

VERSION = "1.1.0"
API_PORT = 8877


def number(lo, hi, default, unit):
    return {"type": "number", "minimum": lo, "maximum": hi, "default": default, "unit": unit}


PROFILES = {
    "mobile_manipulator": {
        "fields": {"speed_m_s": number(0.05, 0.35, 0.25, "m/s")},
        "actions": ["navigate", "pick", "place", "home", "estop", "reset_estop", "inspect"],
    },
    "bench": {"fields": {}, "actions": ["inspect"]},
    "hood": {
        "fields": {
            "fan_on": {"type": "boolean", "default": True},
            "sash_open_pct": number(0, 100, 35, "%"),
        },
        "actions": ["inspect"],
    },
    "reactor": {
        "fields": {
            "target_temperature_c": number(20, 100, 25, "degC"),
            "stir_rpm": number(0, 1200, 0, "rpm"),
        },
        "actions": ["start", "stop", "sample"],
    },
    "vessel": {"fields": {}, "actions": ["sample", "inspect"]},
    "hotplate": {
        "fields": {
            "target_temperature_c": number(20, 200, 25, "degC"),
            "stir_rpm": number(0, 1500, 0, "rpm"),
        },
        "actions": ["start", "stop"],
    },
    "bath": {
        "fields": {"target_temperature_c": number(20, 95, 25, "degC")},
        "actions": ["start", "stop"],
    },
    "oven": {
        "fields": {
            "target_temperature_c": number(20, 200, 25, "degC"),
            "door_open": {"type": "boolean", "default": False},
        },
        "actions": ["start", "stop"],
    },
    "chiller": {
        "fields": {"target_temperature_c": number(5, 30, 20, "degC")},
        "actions": ["start", "stop"],
    },
    "balance": {"fields": {}, "actions": ["tare", "weigh"]},
    "ph_meter": {"fields": {}, "actions": ["measure"]},
    "uvvis": {"fields": {"path_length_cm": number(0.1, 5, 1, "cm")}, "actions": ["measure"]},
    "ftir": {"fields": {}, "actions": ["measure"]},
    "centrifuge": {
        "fields": {
            "speed_rpm": number(0, 6000, 2000, "rpm"),
            "duration_s": number(1, 3600, 60, "s"),
            "lid_open": {"type": "boolean", "default": False},
        },
        "actions": ["start", "stop"],
    },
    "reagent": {
        "fields": {"cap_open": {"type": "boolean", "default": False}},
        "actions": ["dispense", "inspect"],
    },
    "cabinet": {
        "fields": {"door_open": {"type": "boolean", "default": False}},
        "actions": ["inspect"],
    },
    "sink": {"fields": {"water_on": {"type": "boolean", "default": False}}, "actions": ["inspect"]},
    "eyewash": {
        "fields": {"water_on": {"type": "boolean", "default": False}},
        "actions": ["inspect"],
    },
    "waste": {"fields": {}, "actions": ["inspect"]},
    "extinguisher": {"fields": {}, "actions": ["inspect"]},
    "rack": {"fields": {}, "actions": ["inspect"]},
}

ASSETS = []


def asset(id, name, label, kind, zone, location, size, **meta):
    p = deepcopy(PROFILES[kind])
    fields = p["fields"]
    state = {k: v["default"] for k, v in fields.items()}
    state.update(status="idle", visible=True)
    if kind in {"reactor", "hotplate", "bath", "oven", "chiller"}:
        state.update(temperature_c=25.0, running=False)
    if kind in {"vessel", "reactor", "waste"}:
        state.update(volume_ml=0.0, contents=[], mass_g=0.0)
    if kind == "reagent":
        state.update(remaining=meta["quantity"], unit=meta["unit"])
    if kind == "centrifuge":
        state.update(running=False, remaining_s=0.0)
    if kind in {"balance", "ph_meter", "uvvis", "ftir"}:
        state.update(last_result_id="", reading="READY")
    if kind == "mobile_manipulator":
        state.update(
            base_yaw_deg=0.0,
            wheel_angle_deg=0.0,
            battery_pct=100.0,
            estopped=False,
            held_asset_id="",
            arm_extension=0.0,
            arm_target_m=[0, 0, 1],
            gripper_open=True,
            active_command_id="",
        )
    ASSETS.append(
        dict(
            id=id,
            name=name,
            label=label,
            kind=kind,
            zone=zone,
            location=list(location),
            size=list(size),
            fields=fields,
            actions=p["actions"] + ["select", "set_visible", "move"],
            initial_state=state,
            **meta,
        )
    )


asset(
    "bench_reaction",
    "通风反应装置台",
    "01 / REACTION",
    "bench",
    "reaction",
    (-2.7, 2.45, 0),
    (2.7, 1.1, 0.94),
)
asset(
    "bench_analysis",
    "独立表征仪器台",
    "03 / ANALYTICS",
    "bench",
    "analysis",
    (1.45, 2.65, 0),
    (4.65, 1.0, 0.94),
)
asset(
    "bench_preparation",
    "中央配液装置台",
    "02 / PREPARATION",
    "bench",
    "preparation",
    (0, -0.65, 0),
    (3.65, 1.35, 0.94),
)
asset(
    "bench_wet",
    "清洗与用水装置台",
    "04 / WET SERVICES",
    "bench",
    "utilities",
    (-3.55, 0.2, 0),
    (1.25, 1.4, 0.94),
)
asset(
    "hood_01",
    "通风橱",
    "FUME HOOD",
    "hood",
    "reaction",
    (-2.7, 2.45, 0.94),
    (2.5, 1.0, 1.65),
    support="bench_reaction",
)
asset(
    "reactor_01",
    "1 L 夹套玻璃反应器",
    "R-01 / JACKETED REACTOR",
    "reactor",
    "reaction",
    (-2.9, 2.25, 0.97),
    (0.7, 0.65, 1.24),
    capacity_ml=1000,
    support="bench_reaction",
    hood="hood_01",
)
asset(
    "condenser_01",
    "回流冷凝器与接收瓶",
    "R-02 / REFLUX",
    "vessel",
    "reaction",
    (-1.95, 2.3, 0.97),
    (0.45, 0.48, 1.05),
    capacity_ml=250,
    model="condenser",
    support="bench_reaction",
)
asset(
    "chiller_01",
    "循环冷却器",
    "C-01 / RECIRCULATOR",
    "chiller",
    "reaction",
    (-1.1125, 2.45, 0.06),
    (0.43, 0.58, 0.67),
)
asset(
    "hotplate_01",
    "磁力加热搅拌器",
    "H-01 / HOTPLATE",
    "hotplate",
    "preparation",
    (-1.05, -0.55, 0.94),
    (0.58, 0.5, 0.17),
    support="bench_preparation",
    vessel="beaker_01",
)
asset(
    "beaker_01",
    "500 mL 混合烧杯",
    "V-01 / MIXING",
    "vessel",
    "preparation",
    (-1.05, -0.55, 1.15),
    (0.3, 0.3, 0.4),
    capacity_ml=500,
    support="hotplate_01",
)
asset(
    "flask_01",
    "250 mL 锥形瓶",
    "V-02 / SAMPLE",
    "vessel",
    "preparation",
    (-0.23, -0.42, 0.94),
    (0.27, 0.27, 0.4),
    capacity_ml=250,
    model="flask",
    support="bench_preparation",
)
asset(
    "bath_01",
    "恒温水浴",
    "H-02 / WATER BATH",
    "bath",
    "preparation",
    (1.03, -0.4, 0.94),
    (0.86, 0.66, 0.42),
    support="bench_preparation",
)
asset(
    "oven_01",
    "鼓风干燥箱",
    "H-03 / DRYING OVEN",
    "oven",
    "heating",
    (3.48, 0.65, 0.08),
    (1.0, 0.85, 1.5),
)
asset(
    "balance_01",
    "分析天平",
    "A-01 / BALANCE",
    "balance",
    "analysis",
    (-0.32, 2.56, 0.94),
    (0.58, 0.5, 0.6),
    support="bench_analysis",
)
asset(
    "ph_01",
    "pH 测定仪",
    "A-02 / pH",
    "ph_meter",
    "analysis",
    (0.6, 2.55, 0.94),
    (0.48, 0.5, 0.6),
    support="bench_analysis",
)
asset(
    "uvvis_01",
    "紫外可见分光光度计",
    "A-03 / UV-VIS",
    "uvvis",
    "analysis",
    (1.57, 2.6, 0.94),
    (0.82, 0.65, 0.45),
    support="bench_analysis",
)
asset(
    "ftir_01",
    "ATR 傅里叶红外光谱仪",
    "A-04 / FTIR",
    "ftir",
    "analysis",
    (2.75, 2.6, 0.94),
    (0.88, 0.65, 0.47),
    support="bench_analysis",
)
asset(
    "centrifuge_01",
    "台式离心机",
    "P-01 / CENTRIFUGE",
    "centrifuge",
    "preparation",
    (1.2, -1.0, 0.94),
    (0.63, 0.56, 0.48),
    support="bench_preparation",
)
asset(
    "rack_01",
    "试管架与移液器架",
    "P-02 / SAMPLE RACK",
    "rack",
    "preparation",
    (0.22, -0.95, 0.94),
    (0.66, 0.32, 0.5),
    support="bench_preparation",
)
asset(
    "cabinet_salts",
    "固体试剂柜",
    "DRY REAGENTS",
    "cabinet",
    "storage",
    (-3.62, -1.88, 0.06),
    (1.35, 0.58, 1.7),
    model="shelf",
)
asset(
    "cabinet_solvents",
    "溶剂储存柜",
    "SOLVENT STORAGE",
    "cabinet",
    "storage",
    (3.5, -1.45, 0.06),
    (0.92, 0.65, 1.08),
    model="solvents",
)
asset(
    "water_01",
    "去离子水",
    "DI WATER",
    "reagent",
    "storage",
    (-3.95, -1.86, 1.26),
    (0.23, 0.23, 0.34),
    quantity=1000,
    unit="ml",
    density=1.0,
    color=[0.18, 0.66, 0.85],
    support="cabinet_salts",
)
asset(
    "salt_01",
    "氯化钠",
    "NaCl",
    "reagent",
    "storage",
    (-3.58, -1.86, 1.26),
    (0.23, 0.23, 0.34),
    quantity=500,
    unit="g",
    density=2.16,
    color=[0.84, 0.88, 0.91],
    support="cabinet_salts",
)
asset(
    "citrate_01",
    "柠檬酸",
    "CITRIC ACID",
    "reagent",
    "storage",
    (-3.23, -1.86, 1.26),
    (0.23, 0.23, 0.34),
    quantity=250,
    unit="g",
    density=1.66,
    color=[0.91, 0.85, 0.62],
    support="cabinet_salts",
)
asset(
    "bicarbonate_01",
    "碳酸氢钠",
    "NaHCO3",
    "reagent",
    "storage",
    (-3.95, -1.86, 0.72),
    (0.23, 0.23, 0.34),
    quantity=250,
    unit="g",
    density=2.2,
    color=[0.86, 0.87, 0.9],
    support="cabinet_salts",
)
asset(
    "cuso4_01",
    "硫酸铜示例溶液",
    "CuSO4 (aq)",
    "reagent",
    "storage",
    (-3.58, -1.86, 0.72),
    (0.23, 0.23, 0.34),
    quantity=500,
    unit="ml",
    density=1.02,
    color=[0.05, 0.38, 0.92],
    support="cabinet_salts",
)
asset(
    "buffer_01",
    "pH 7 缓冲液",
    "BUFFER pH 7",
    "reagent",
    "storage",
    (-3.23, -1.86, 0.72),
    (0.23, 0.23, 0.34),
    quantity=500,
    unit="ml",
    density=1.0,
    color=[0.21, 0.7, 0.39],
    support="cabinet_salts",
)
asset(
    "ethanol_01",
    "乙醇",
    "ETHANOL",
    "reagent",
    "storage",
    (3.32, -1.44, 0.59),
    (0.23, 0.23, 0.34),
    quantity=500,
    unit="ml",
    density=0.789,
    color=[0.82, 0.7, 0.36],
    support="cabinet_solvents",
)
asset(
    "indicator_01",
    "指示剂示例溶液",
    "INDICATOR",
    "reagent",
    "storage",
    (3.65, -1.44, 0.59),
    (0.2, 0.2, 0.28),
    quantity=100,
    unit="ml",
    density=0.9,
    color=[0.7, 0.12, 0.48],
    support="cabinet_solvents",
)
asset(
    "sink_01",
    "清洗水槽与水龙头",
    "SINK / DI TAP",
    "sink",
    "utilities",
    (-3.55, 0.22, 0.94),
    (1.04, 0.8, 0.5),
    support="bench_wet",
)
asset(
    "eyewash_01",
    "紧急洗眼器",
    "EYEWASH",
    "eyewash",
    "utilities",
    (-3.95, 1.34, 0.06),
    (0.48, 0.48, 1.2),
)
asset(
    "waste_aqueous",
    "水相废液收集桶",
    "AQUEOUS WASTE",
    "waste",
    "utilities",
    (-2.6, -2.5, 0.06),
    (0.38, 0.4, 0.62),
    capacity_ml=10000,
)
asset(
    "waste_solvent",
    "有机溶剂废液收集桶",
    "SOLVENT WASTE",
    "waste",
    "utilities",
    (3.47, -2.58, 0.06),
    (0.38, 0.4, 0.62),
    capacity_ml=10000,
)
asset(
    "extinguisher_01",
    "灭火器",
    "FIRE",
    "extinguisher",
    "utilities",
    (-4.02, -3.08, 0.06),
    (0.28, 0.28, 0.8),
)

asset(
    "robot_01",
    "移动机械臂实验室助手",
    "LAB ASSIST / M-01",
    "mobile_manipulator",
    "automation",
    (0.45, -2.25, 0.08),
    (0.64, 0.64, 1.4),
    footprint_radius_m=0.38,
    payload_kg=1.0,
    reach_m=0.86,
)
ASSETS[-1]["actions"].remove("move")
asset(
    "sample_tube_01",
    "封闭样品转运管",
    "SAMPLE / S-01",
    "vessel",
    "automation",
    (-0.5, -1.12, 0.94),
    (0.075, 0.075, 0.22),
    capacity_ml=50,
    model="transport_tube",
    portable=True,
    support="bench_preparation",
    grasp_offset_m=[0, 0, 0.17],
)
ASSETS[-1]["fields"] = {"sealed": {"type": "boolean", "default": True}}
ASSETS[-1]["initial_state"]["sealed"] = True

CATALOG = {a["id"]: a for a in ASSETS}


def public_asset(a):
    result = deepcopy(a)
    result["api"] = f"/api/v1/assets/{a['id']}"
    return result
