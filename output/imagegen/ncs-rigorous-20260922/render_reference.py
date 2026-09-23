"""Strict source-data figure layouts. No new experiment or image retouching."""
from pathlib import Path
from collections import defaultdict
from statistics import fmean
import csv, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, FancyArrowPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
REF = OUT / "reference"
REF.mkdir(parents=True, exist_ok=True)
ARMS = ("Opaque", "Aligned", "MisIndexed")
COLORS = dict(zip(ARMS, ("#3d5268", "#397a75", "#956448")))
MARKERS = ("o", "s", "^", "D", "v")
INK = "#202c37"
SOURCE = ROOT / "paper/figures/integrated-results"
analysis = json.loads((SOURCE / "analysis.json").read_text(encoding="utf-8"))
metrics = list(csv.DictReader((SOURCE / "campaign_metrics.csv").open(encoding="utf-8")))
story = json.loads((ROOT / "workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/STORY_WORLD_ANALYSIS.json").read_text(encoding="utf-8"))
baseline = json.loads((ROOT / "workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json").read_text(encoding="utf-8"))["rows"]
manifest = []

def rc():
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,
        "axes.titlesize":10,"axes.labelsize":9,"xtick.labelsize":8,"ytick.labelsize":8,
        "text.color":INK,"axes.labelcolor":INK,"axes.edgecolor":INK,"axes.linewidth":.7,
        "axes.spines.top":False,"axes.spines.right":False,"figure.facecolor":"white",
        "axes.facecolor":"white","svg.fonttype":"none","savefig.facecolor":"white"})

def arm_handles():
    return [Line2D([],[],color=COLORS[a],marker="o",ls="",label=a,ms=5) for a in ARMS]

def common_axes(ax, grid=False):
    ax.tick_params(width=.6,length=3)
    if grid: ax.grid(axis="y",color="#e7e9eb",lw=.5); ax.set_axisbelow(True)

def save(fig, number, variant, counts):
    stem = f"fig{number:02d}-{variant}"
    fig.savefig(REF / (stem+".png"),dpi=190,bbox_inches="tight",pad_inches=.12)
    fig.savefig(REF / (stem+".svg"),bbox_inches="tight",pad_inches=.12)
    plt.close(fig)
    manifest.append({"id":stem,"figure":number,"variant":variant,"reference_png":"reference/"+stem+".png",
                     "reference_svg":"reference/"+stem+".svg","counts":counts})
    print(f"REFERENCE {len(manifest)}/20 {stem}",flush=True)

def box(ax, x,y,w,h,title,body,fill="#f5f7f8",fs=9):
    ax.add_patch(Rectangle((x,y),w,h,facecolor=fill,edgecolor="#86939c",lw=.7))
    ax.text(x+.015,y+h-.028,title,ha="left",va="top",fontsize=fs+1,weight="bold")
    ax.text(x+.015,y+h-.088,body,ha="left",va="top",fontsize=fs,linespacing=1.55)

def arrow(ax,start,end,color=INK):
    ax.add_patch(FancyArrowPatch(start,end,arrowstyle="-|>",mutation_scale=10,lw=.85,color=color))

def framework(v):
    fig,ax=plt.subplots(figsize=(12,8) if v in "AC" else (10,9.6))
    ax.set(xlim=(0,1),ylim=(0,1)); ax.axis("off")
    if v in "AC":
        box(ax,.01,.70,.28,.27,"a  Programmable world",
            "Private process laws\nPersistent materials and samples\nOperations, instruments, resources\nDeclared public observations")
        box(ax,.34,.70,.31,.27,"b  Autonomous research",
            "Opaque / Aligned / MisIndexed\nSame world; different supplied information\nTask-specific research commission\n12 or 24 batches + matching measurements",fs=8.5)
        box(ax,.70,.70,.29,.27,"c  Experimental feedback",
            "Select an operation\nObserve the declared result\nRevise the next experiment\nFull action-observation history",fs=8.5)
        arrow(ax,(.29,.83),(.34,.83)); arrow(ax,(.65,.83),(.70,.83))
        ax.text(.01,.655,"d  Recommendation and post-experiment assessment",weight="bold",fontsize=10)
        boxes=[(.01,"Seal recommendation"),(.27,"K1: Mechanism"),(.51,"Q: Prediction"),(.76,"K2: Retrospective")]
        for x,t in boxes:
            ax.add_patch(Rectangle((x,.52),.22,.095,facecolor="#f5f7f8",edgecolor="#86939c",lw=.7))
            ax.text(x+.11,.567,t,ha="center",va="center",fontsize=9,weight="bold")
        for a,b in zip(boxes,boxes[1:]): arrow(ax,(a[0]+.22,.567),(b[0],.567))
        box(ax,.01,.305,.22,.12,"Independent retest","Sealed operating recommendation",fs=7.5)
        arrow(ax,(.12,.52),(.12,.425))
        ax.text(.30,.43,"K1: free-form account; no fixed equation template\nQ: 12 new conditions, point and interval predictions\nK2: reflection after Q; cannot revise sealed predictions",va="top",fontsize=9,linespacing=1.65)
        ax.text(.30,.305,"Q retains the full source history; retest outcomes are not supplied to Q.",fontsize=8.5)
        box(ax,.01,.01,.48,.24,"e  Controlled scope",
            "Change process laws under matched interfaces, or\nchange supplied information within the same world.\nPlatform: nine task families; study: EC, PA, RX, EQ, C, P.",fs=8.5)
        box(ax,.52,.01,.47,.24,"f  Readouts and retained outcomes",
            "Prediction MAE; interval coverage and width; task retests\n240 campaigns; 238 conforming research chains\n3,597 / 3,600 final assays; 720 / 720 K1, Q, K2 stages",fs=8.5)
    else:
        box(ax,.02,.76,.46,.22,"a  Private process model",
            "Process laws and parameters\nPersistent material state\nDeclared resources and legal operations")
        box(ax,.53,.76,.45,.22,"b  Public research interface",
            "Opaque / Aligned / MisIndexed\nSame world; different supplied information\nTask-specific goals and observations",fs=8.5)
        arrow(ax,(.48,.86),(.53,.86))
        ax.text(.02,.713,"c  Autonomous research and sealed assessment",weight="bold",fontsize=10)
        ys=[.62,.51,.40,.29,.18]
        titles=["Research: select → observe → revise","Seal operating recommendation",
                "K1: Free-form mechanism","Q: Predict 12 new conditions","K2: Retrospective reflection"]
        for y,t in zip(ys,titles):
            ax.add_patch(Rectangle((.06,y),.55,.072,facecolor="#f5f7f8",edgecolor="#86939c",lw=.7))
            ax.text(.335,y+.036,t,ha="center",va="center",fontsize=9)
        for y1,y2 in zip(ys,ys[1:]): arrow(ax,(.335,y1),(.335,y2+.072))
        box(ax,.68,.485,.29,.115,"Independent retest","Sealed recommendation",fs=8)
        arrow(ax,(.61,.546),(.68,.546))
        ax.text(.67,.40,"12 or 24 batches\nMatching measurement allowance\nFull source history retained for Q\nRetest outcomes withheld from Q\nK2 cannot revise Q",va="top",fontsize=8.5,linespacing=1.65)
        ax.text(.02,.105,"d  Scope and readouts",fontsize=10,weight="bold")
        ax.text(.02,.078,"Nine supported task families; six studied: EC, PA, RX, EQ, C, P.\n240 campaigns; 238 conforming chains; 3,597 / 3,600 assays; 720 / 720 posttest stages.\nSeparate readouts: prediction error, intervals and independent task retests.",
                va="top",fontsize=8,linespacing=1.55)
    save(fig,1,v,{"campaigns":240,"conforming":238,"posttest_stages":720})

def goals(v):
    vertical=v in "BD"
    fig,axs=plt.subplots(2 if vertical else 1,1 if vertical else 2,
        figsize=(7.5,10.5) if vertical else (12,6.2))
    fig.subplots_adjust(left=.12 if vertical else .08,right=.97,top=.94,bottom=.21 if vertical else .27,hspace=.40,wspace=.28)
    for ax,s,letter in zip(np.ravel(axs),("EC","RX"),"ab"):
        pairs=analysis["goal_contrasts"][s]
        assert len(pairs)==30
        for p in pairs:
            filled=p["budget"]==24 if s=="EC" else p["locus"]=="S"
            color=COLORS[p["arm"]]
            ax.scatter(p["delta_retest"],p["delta_mae"],s=34,marker=MARKERS[int(p["world"][-2:])-1],
                facecolors=color if filled else "white",edgecolors=color,linewidth=.9,zorder=3)
        ax.axhline(0,color="#a0a8ae",lw=.7); ax.axvline(0,color="#a0a8ae",lw=.7)
        ax.set_title(f"{letter}  {s}: optimization minus discovery",loc="left")
        ax.set_xlabel("Change in recommendation retest score")
        ax.set_ylabel("Change in score-prediction MAE")
        ax.text(.02,.98,"Open: 12 batches; filled: 24 batches" if s=="EC" else "Open: parameter prior; filled: structure prior",
                transform=ax.transAxes,va="top",fontsize=7.3)
        common_axes(ax,v=="D")
    handles=arm_handles()+[Line2D([],[],color="#3e4246",marker=m,ls="",label=f"W{i+1:02d}",ms=5) for i,m in enumerate(MARKERS)]
    fig.legend(handles=handles,ncol=4,frameon=False,loc="lower center",bbox_to_anchor=(.5,.085),fontsize=8)
    fig.text(.08,.057,"Matched pairs: EC 30; RX 30. Better retest / better prediction / better retest + worse prediction:",fontsize=8)
    fig.text(.08,.035,"EC: 26 / 14 / 13.   RX: 9 / 8 / 5.   Five reused worlds per study; system-specific score scales.",fontsize=8)
    save(fig,2,v,{"EC_pairs":30,"RX_pairs":30,"worlds_per_study":5})

def axes4(v, equal=False):
    if v=="B":
        nr,nc,sz=1,4,(15,5.3)
    elif v=="C":
        nr,nc,sz=4,1,(7.2,14)
    else:
        nr,nc,sz=2,2,(10.5,9.5) if v=="A" else (12,8.8)
    fig,axs=plt.subplots(nr,nc,figsize=sz)
    fig.subplots_adjust(left=.12 if nc==1 else .08,right=.98,top=.95,bottom=.16 if nr==1 else .13,wspace=.35,hspace=.50)
    return fig,np.ravel(axs)

def budgets(v):
    fig,axs=axes4(v)
    conditions=[("EC","discovery","score","EC discovery"),("EC","optimization","score","EC optimization"),
        ("PA","discovery","product_in_organic","PA organic fraction"),("C","delivery","crystal_fines_fraction","C fines fraction")]
    paircounts=[]
    for ax,(s,g,m,title),letter in zip(axs,conditions,"abcd"):
        ss=[r for r in metrics if r["system"]==s and r["goal"]==g and r["metric"]==m]
        groups=defaultdict(dict)
        for r in ss: groups[r["world"],r["arm"]][int(r["budget"])]=r
        assert len(groups)==15 and all(set(p)=={12,24} for p in groups.values())
        for (w,a),pair in groups.items():
            vals=[float(pair[b]["mae"]) for b in (12,24)]
            ax.plot([12,24],vals,color=COLORS[a],lw=.7,alpha=.45,marker="o",ms=2.8)
            for b in (12,24):
                if pair[b]["conforming"]!="True": ax.scatter(b,float(pair[b]["mae"]),marker="x",color=INK,s=40,zorder=5)
        means=[fmean(float(r["mae"]) for r in ss if int(r["budget"])==b) for b in (12,24)]
        ax.plot([12,24],means,color=INK,lw=1.8,marker="D",ms=5,zorder=4)
        ax.set(title=f"{letter}  {title}",xticks=[12,24],xlim=(10,26),xlabel="Batch budget",ylabel="Prediction MAE",ylim=(0,None))
        ax.text(.03,.98,f"Mean: {means[0]:.5f} → {means[1]:.5f}",transform=ax.transAxes,va="top",fontsize=7.7)
        paircounts.append(len(groups)); common_axes(ax,v=="D")
    handles=arm_handles()+[Line2D([],[],color=INK,marker="D",lw=1.8,label="Mean"),Line2D([],[],color=INK,marker="x",ls="",label="Source shortfall")]
    fig.legend(handles=handles,ncol=5 if v=="B" else 3,frameon=False,loc="lower center",bbox_to_anchor=(.5,.025),fontsize=8)
    fig.text(.08,.015,"15 matched pairs per panel. Independent sessions; 24 batches include larger operational and computational allowances.",fontsize=7.5)
    save(fig,3,v,{"matched_pairs_per_panel":paircounts,"shortfall_campaigns":1})

def regimes(v):
    if v=="A":
        fig,axs=plt.subplots(1,3,figsize=(14,5.6))
        fig.subplots_adjust(left=.055,right=.98,top=.91,bottom=.24,wspace=.32)
    elif v=="B":
        fig,axs=plt.subplots(3,1,figsize=(7.5,13))
        fig.subplots_adjust(left=.16,right=.94,top=.95,bottom=.12,hspace=.43)
    else:
        fig=plt.figure(figsize=(11,10)); gs=fig.add_gridspec(2,2)
        if v=="C": axs=[fig.add_subplot(gs[0,0]),fig.add_subplot(gs[0,1]),fig.add_subplot(gs[1,:])]
        else: axs=[fig.add_subplot(gs[0,0]),fig.add_subplot(gs[1,0]),fig.add_subplot(gs[:,1])]
        fig.subplots_adjust(left=.09,right=.97,top=.94,bottom=.16,wspace=.35,hspace=.48)
    eq=story["eq_p_query_regimes"]["aggregate"]; cells=story["eq_p_query_regimes"]["cells"]
    groups=("other_nine","three_most_dilute")
    for ax,metric,scale,title in zip(axs[:2],("mae","coverage"),(1,100),("a  EQ: prediction error","b  EQ: interval coverage")):
        for i,a in enumerate(ARMS):
            xs=np.arange(2)+(i-1)*.23
            vals=[next(r[metric] for r in eq if r["arm"]==a and r["group"]==g)*scale for g in groups]
            ax.bar(xs,vals,width=.205,color=COLORS[a],alpha=.83)
            for j,g in enumerate(groups):
                values=[r["groups"][g][metric]*scale for r in cells if r["arm"]==a]
                assert len(values)==5
                ax.scatter(xs[j]+np.linspace(-.055,.055,5),values,s=20,facecolor="white",edgecolor=COLORS[a],lw=.9,zorder=3)
        ax.set_title(title,loc="left")
        ax.set_xticks([0,1],["Other nine\nqueries","Three most\ndilute queries"])
        ax.set_ylabel("Macro mean absolute error" if metric=="mae" else "Coverage (%)")
        if metric=="coverage": ax.axhline(80,color=INK,ls="--",lw=.9); ax.set_ylim(0,105)
        common_axes(ax,True)
    pair=[r for r in story["c_paired_response_tradeoffs"] if r["budget"]==12]
    ax=axs[2]
    for p in pair:
        ax.scatter(p["recovery_delta"],p["purity_delta"],color=COLORS[p["arm"]],s=36,marker="o" if p["arm"]=="Aligned" else "^",zorder=3)
        if not p["both_conforming"]: ax.scatter(p["recovery_delta"],p["purity_delta"],marker="x",color=INK,s=62,zorder=4)
    ax.axhline(0,color="#8a959d",lw=.7); ax.axvline(0,color="#8a959d",lw=.7)
    ax.set(title="c  C: response tradeoff, 12 batches",xlabel="Recovery MAE change vs Opaque",ylabel="Purity MAE change vs Opaque",
           xlim=(-.37,.01),ylim=(-.005,.13))
    ax.grid(color="#e7e9eb",lw=.5); ax.set_axisbelow(True)
    handles=arm_handles()+[Line2D([],[],color=INK,ls="--",label="Nominal 80%"),Line2D([],[],color=INK,marker="x",ls="",label="Source shortfall")]
    fig.legend(handles=handles,ncol=3,frameon=False,loc="lower center",bbox_to_anchor=(.5,.035),fontsize=8)
    fig.text(.06,.022,"Exploratory retained-data analysis; five reused worlds. Other nine queries include boundary conditions.",fontsize=7.5)
    fig.text(.06,.005,"EQ dots: world means. C: 5 Aligned and 5 MisIndexed pairs; crosses identify pairs containing the shortfall source.",fontsize=7.5)
    save(fig,4,v,{"EQ_world_points_per_panel":30,"C_paired_points":len(pair),"C_shortfall_pairs":sum(not p["both_conforming"] for p in pair)})

def evidence(v):
    fig,axs=axes4(v)
    ms=[("crystal_yield","Net crystal recovery"),("crystal_purity","Crystal purity"),("crystal_size","Particle-size index"),("crystal_fines_fraction","Fines fraction")]
    counts=[]
    for ax,(metric,title),letter in zip(axs,ms,"abcd"):
        limit=max(max(r["agent_mae"][metric],r["public_baselines"]["mae"]["public_mean"][metric]) for r in baseline)*1.08
        ax.plot([0,limit],[0,limit],color="#7e8b95",ls="--",lw=.8,zorder=0)
        wins=0
        for r in baseline:
            x=r["public_baselines"]["mae"]["public_mean"][metric]; y=r["agent_mae"][metric];wins+=y<x
            ax.scatter(x,y,c=COLORS[r["arm"]],s=29,alpha=.88,
                marker=("o" if r["budget"]==12 else "^") if r["conforming"] else "x")
        ax.set(xlim=(0,limit),ylim=(0,limit),aspect="equal",xlabel="Public-mean MAE",ylabel="Agent MAE")
        ax.set_title(f"{letter}  {title}\nAgent lower MAE: {wins}/30",loc="left",fontsize=9)
        ax.ticklabel_format(axis="both",style="plain",useOffset=False); counts.append(wins);common_axes(ax,v=="D")
    handles=arm_handles()+[Line2D([],[],color=INK,marker=m,ls="",label=t) for m,t in (("o","12 batches"),("^","24 batches"),("x","Source shortfall"))]
    fig.legend(handles=handles,ncol=3 if v!="B" else 6,frameon=False,loc="lower center",bbox_to_anchor=(.5,.027),fontsize=8)
    fig.text(.08,.012,"30 campaigns per response; same source observations. Below diagonal: agent better. Above: public mean better.",fontsize=7.5)
    assert counts==[26,0,4,21]
    save(fig,5,v,{"campaigns_per_response":30,"agent_wins":counts,"nonconforming_sources":1})

rc()
for n,fn in enumerate((framework,goals,budgets,regimes,evidence),1):
    for v in "ABCD": fn(v)
(OUT/"reference-manifest.json").write_text(json.dumps({"source_manuscript":"paper/venues/ncs/article.md",
    "sources":["paper/figures/integrated-results/analysis.json","paper/figures/integrated-results/campaign_metrics.csv",
    "workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/STORY_WORLD_ANALYSIS.json",
    "workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json"],
    "figures":manifest},indent=2),encoding="utf-8")

