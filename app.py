from pathlib import Path
import os
from html import escape
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT=Path(__file__).resolve().parent
def find_data_file():
    configured=os.environ.get("PAISABAZAAR_DATA")
    candidates=[]
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.extend([ROOT/"dataset-2.csv",ROOT/"data"/"credit_health_demo.csv"])
    return next((path for path in candidates if path.exists()),None)

CSV=find_data_file()
USING_DEMO=CSV is not None and CSV.name=="credit_health_demo.csv"
SCORES=["Poor","Standard","Good"]
COLORS={"Poor":"#C96758","Standard":"#C58A2C","Good":"#25816F"}
MIX_COLORS={"Bad":"#C96758","Standard":"#7D91A3","Good":"#25816F"}
BEHAVIOUR_COLORS={"High_spent_Large_value_payments":"#285E86","High_spent_Medium_value_payments":"#4C88AF","High_spent_Small_value_payments":"#86B5D0","Low_spent_Large_value_payments":"#8DAA8C","Low_spent_Medium_value_payments":"#C7A66B","Low_spent_Small_value_payments":"#C77D63"}
MIN_PAYMENT_COLORS={"NM":"#718096","No":"#C58A2C","Yes":"#25816F"}
CATEGORY_LABELS={"NM":"Not mentioned","High_spent_Large_value_payments":"High · large payments","High_spent_Medium_value_payments":"High · medium payments","High_spent_Small_value_payments":"High · small payments","Low_spent_Large_value_payments":"Low · large payments","Low_spent_Medium_value_payments":"Low · medium payments","Low_spent_Small_value_payments":"Low · small payments"}
FALLBACK_COLORS=["#426B8C","#66A69D","#C58A2C","#8873A9","#C96758","#6A8D68"]
IDENTIFIERS={"ID","Name","SSN"}
st.set_page_config(page_title="Paisabazaar | Credit Portfolio Intelligence",page_icon="◈",layout="wide")
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:#F5F7FA}
[data-testid="stHeader"]{background:rgba(245,247,250,.92)}
[data-testid="stSidebar"]{background:#14263D;border-right:1px solid #263B54}
[data-testid="stSidebar"] *{color:#EAF1F7}
[data-testid="stSidebar"] [data-baseweb="select"] *{color:#1A2C41}
.block-container{max-width:1450px;padding:2rem 3rem 3rem}
h1,h2,h3{color:#152B45;font-family:system-ui,sans-serif;letter-spacing:-.03em}
h1{font-size:2.15rem!important;font-weight:800!important}
[data-testid="stMetric"]{background:white;padding:1rem;border:1px solid #E4EAF0;border-radius:16px;box-shadow:0 5px 18px #14263D0A}
div[data-testid="stPlotlyChart"]{background:white;border:1px solid #E4EAF0;border-radius:16px;padding:.35rem}
.hero{padding:2rem 2.2rem;border-radius:22px;background:linear-gradient(115deg,#14263D,#1A4860 57%,#177E89);margin:.2rem 0 1.2rem;box-shadow:0 14px 35px #14263D22}
.hero h1{color:white!important;margin:0 0 .45rem}.hero p{color:#D7E6EF;margin:0;font-size:1.03rem}
.eyebrow{color:#8DD7CC;font-size:.74rem;font-weight:700;letter-spacing:.14em;margin-bottom:.7rem}
.notice{background:#EAF2F4;border-left:4px solid #3D9AA3;padding:.9rem 1.1rem;border-radius:0 12px 12px 0;color:#24475D;margin:.75rem 0 1.15rem;line-height:1.55}
.card{height:100%;background:white;border:1px solid #E4EAF0;border-radius:15px;padding:1rem}
.card-label{color:#718197;font-size:.74rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em}
.card-body{color:#203750;margin-top:.45rem;line-height:1.5}
@media(max-width:900px){.block-container{padding:1.2rem 1rem 2rem}.hero{padding:1.4rem}}

:root{color-scheme:light}
[data-testid="stAppViewContainer"]{background:#F3F6F8}
.block-container{max-width:1480px;padding:1.6rem 2.6rem 3rem}
[data-testid="stSidebar"]{background:#14263D}
.hero{margin:.25rem 0 1rem}
.notice{background:#EDF5F6;border-left-color:#258D8B}
div[data-testid="stPlotlyChart"]{background:#fff;border:1px solid #E1E8EE;border-radius:16px;padding:0;box-shadow:0 5px 18px rgba(20,38,61,.045);overflow:hidden;height:auto!important}
.stTabs [data-baseweb="tab"]{color:#43586D!important;font-weight:600}
.stTabs [aria-selected="true"]{color:#147D7A!important;border-bottom-color:#168C91!important}
[data-testid="stCaptionContainer"]{color:#607487!important}
.stCaptionContainer{color:#607487!important}
.insight-card{background:#F2F7F8;border:1px solid #DCE9E9;border-left:4px solid #258D8B;border-radius:12px;padding:.8rem .95rem;margin:.2rem 0 .55rem;min-height:84px}
.insight-label{font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;font-weight:800;color:#27827F;margin-bottom:.3rem}
.insight-card strong{display:block;color:#19364E;font-size:.92rem;line-height:1.35;margin-bottom:.2rem}
.insight-card p{font-size:.84rem;color:#4A5F70;line-height:1.45;margin:0}
.section-intro{color:#566B7B;font-size:.94rem;line-height:1.55;margin:.1rem 0 .9rem}
.chart-legend{display:flex;flex-wrap:wrap;gap:.48rem 1rem;padding:.45rem .65rem .55rem;margin:0 .15rem .55rem}
.chart-legend-item{display:inline-flex;align-items:center;gap:.45rem;min-width:135px;color:#43596D;font-size:.78rem;line-height:1.35}
.chart-legend-swatch{width:11px;height:11px;border-radius:3px;flex:0 0 11px}
.method-card{height:100%;background:#fff;border:1px solid #E1E8EE;border-radius:14px;padding:1rem 1.05rem}
.method-card h4{margin:0 0 .45rem;color:#18354F;font-size:.95rem}
.method-card p{margin:0;color:#4A5F70;line-height:1.5;font-size:.88rem}
@media(max-width:900px){.block-container{padding:1.15rem .9rem 2rem}.hero{padding:1.35rem}.insight-card{min-height:0}}

</style>""",unsafe_allow_html=True)

@st.cache_data(show_spinner="Preparing analysis...")
def load_data(path,stamp):
    d=pd.read_csv(path,usecols=lambda c:c not in IDENTIFIERS,low_memory=False)
    for c in d.select_dtypes(include=["object","string"]).columns:
        d[c]=d[c].astype("string").str.strip()
    nums=["Customer_ID","Month","Age","Annual_Income","Monthly_Inhand_Salary","Num_Bank_Accounts","Num_Credit_Card","Interest_Rate","Num_of_Loan","Delay_from_due_date","Num_of_Delayed_Payment","Changed_Credit_Limit","Num_Credit_Inquiries","Outstanding_Debt","Credit_Utilization_Ratio","Credit_History_Age","Total_EMI_per_month","Amount_invested_monthly","Monthly_Balance"]
    for c in nums:
        if c in d:d[c]=pd.to_numeric(d[c],errors="coerce")
    d=d.dropna(subset=["Month","Credit_Score"]).copy()
    d["Month"]=d.Month.astype(int)
    d["Credit_Score"]=d.Credit_Score.astype("string").str.title()
    return d[d.Credit_Score.isin(SCORES)].copy()

def chart_style(f,h=390,legend=None):
    if legend is None:
        legend=f.layout.showlegend
        if legend is None:
            legend=any(getattr(trace, 'showlegend', True) is not False and trace.type not in ('heatmap','pie') for trace in f.data)
    bottom=108 if legend else 42
    f.update_layout(
        height=h,
        margin=dict(l=18,r=18,t=58,b=bottom),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif",color="#20384D",size=12),
        title=dict(font=dict(family="Arial, sans-serif",size=16,color="#17344D"),x=.025,xanchor="left"),
        showlegend=legend,
        legend=dict(
            orientation="h",x=.02,xanchor="left",y=-.25,yanchor="top",
            font=dict(family="Arial, sans-serif",size=10,color="#43596D"),
            bgcolor="rgba(255,255,255,0)",borderwidth=0,
            entrywidth=135,entrywidthmode="pixels",tracegroupgap=5
        ),
        hoverlabel=dict(font=dict(family="Arial, sans-serif",size=12))
    )
    f.update_xaxes(showgrid=False,linecolor="#DCE5EB",tickfont=dict(family="Arial, sans-serif",size=11,color="#41576A"),title_font=dict(family="Arial, sans-serif",size=11,color="#41576A"))
    f.update_yaxes(gridcolor="#E9EFF3",zeroline=False,tickfont=dict(family="Arial, sans-serif",size=11,color="#41576A"),title_font=dict(family="Arial, sans-serif",size=11,color="#41576A"))
    return f

def display_category(value):
    if pd.isna(value):
        return "Not reported"
    raw=str(value)
    return CATEGORY_LABELS.get(raw,raw.replace("_"," ").strip().title())

def category_colors(values,palette):
    result={}
    for i,raw in enumerate(values):
        raw=str(raw)
        result[display_category(raw)]=palette.get(raw,FALLBACK_COLORS[i%len(FALLBACK_COLORS)])
    return result

def stacked_share_chart(frame,column,title,palette):
    grouped=frame.groupby(["Credit_Score",column],observed=True).size().rename("Records").reset_index()
    if grouped.empty:
        return None,grouped,{}
    grouped["Share"]=grouped.Records/grouped.groupby("Credit_Score").Records.transform("sum")*100
    grouped["Category"]=grouped[column].map(display_category)
    available=set(grouped[column].dropna().astype(str).tolist())
    raw_values=[value for value in palette if value in available]+sorted(available.difference(palette))
    color_map=category_colors(raw_values,palette)
    category_order=[display_category(value) for value in raw_values]
    fig=px.bar(
        grouped,x="Credit_Score",y="Share",color="Category",barmode="stack",
        title=title,category_orders={"Credit_Score":SCORES,"Category":category_order},
        color_discrete_map=color_map,
        labels={"Credit_Score":"Score group","Share":"Share of filtered records","Category":""},
        custom_data=["Records"]
    )
    fig.update_yaxes(ticksuffix="%",range=[0,100],title_text="Share of records")
    fig.update_layout(bargap=.18,showlegend=False)
    fig.update_traces(hovertemplate="%{x}<br>%{fullData.name}: %{y:.1f}%<br>Rows: %{customdata[0]:,}<extra></extra>")
    return fig,grouped,color_map

def dominant_category_text(frame,column):
    summaries=[]
    for score in ("Poor","Good"):
        values=frame.loc[frame.Credit_Score.eq(score),column].dropna().astype(str)
        if values.empty:
            continue
        counts=values.value_counts()
        top=counts.index[0]
        share=counts.iloc[0]/counts.sum()*100
        summaries.append("{}: {} ({:.0f}%)".format(score.lower(),display_category(top),share))
    return " · ".join(summaries) if summaries else "Choose score groups with reported values to compare."

def insight_card(label,title,body):
    markup=(
        '<div class="insight-card"><div class="insight-label">{}</div>'
        '<strong>{}</strong><p>{}</p></div>'
    ).format(escape(str(label)),escape(str(title)),escape(str(body)))
    st.markdown(markup,unsafe_allow_html=True)

def category_summary(grouped):
    """Return the most frequent reported category within each score group."""
    if grouped.empty:
        return "No reported categories are available in this filtered view."
    summaries = []
    for score in SCORES:
        rows = grouped[grouped["Credit_Score"].eq(score)]
        if rows.empty:
            continue
        top = rows.loc[rows["Share"].idxmax()]
        summaries.append(
            "{}: {} ({:.1f}%)".format(
                score.lower(), escape(str(top["Category"])), float(top["Share"])
            )
        )
    return " · ".join(summaries) if summaries else "No selected score groups have reported values."

def detailed_explanation(title, what, reading, implication, limit, next_step=None):
    """Keep detailed chart interpretation available without crowding the page."""
    with st.expander("Chart explanation · {}".format(title)):
        sections = [
            ("What the chart shows", what),
            ("How to read the result", reading),
            ("Business interpretation", implication),
            ("Important limitation", limit),
        ]
        if next_step:
            sections.append(("Responsible next step", next_step))
        body = "\n\n".join(
            "**{}**\n\n{}".format(label, escape(str(text)))
            for label, text in sections
        )
        st.markdown(body)

def render_chart_legend(color_map):
    if not color_map:
        return
    items="".join(
        '<span class="chart-legend-item"><i class="chart-legend-swatch" style="background-color:{}"></i><span>{}</span></span>'.format(escape(color),escape(label))
        for label,color in color_map.items()
    )
    st.markdown('<div class="chart-legend">{}</div>'.format(items),unsafe_allow_html=True)

def banner(title,sub,tag="CREDIT HEALTH STUDIO"):
    st.markdown('<div class="hero"><div class="eyebrow">{}</div><h1>{}</h1><p>{}</p></div>'.format(tag,title,sub),unsafe_allow_html=True)
def card(title,body):
    st.markdown('<div class="card"><div class="card-label">{}</div><div class="card-body">{}</div></div>'.format(title,body),unsafe_allow_html=True)
def percent(v):return "—" if pd.isna(v) else "{:.1f}%".format(v)

if CSV is None:
    st.error("No dataset was found. Put dataset-2.csv beside app.py, set PAISABAZAAR_DATA, or restore data/credit_health_demo.csv.");st.stop()
try:data=load_data(str(CSV),CSV.stat().st_mtime)
except Exception as e:
    st.error("Could not load dataset-2.csv.");st.caption(str(e));st.stop()

with st.sidebar:
    st.markdown('<div style="padding:.4rem 0 1.1rem"><span style="color:#8DD7CC;font-size:.72rem;letter-spacing:.15em">PAISABAZAAR</span><div style="font-size:1.25rem;font-weight:800">Credit Portfolio Intelligence</div><span style="color:#A9B8C8">Data-backed portfolio decision support</span></div>',unsafe_allow_html=True)
    page=st.radio("Explore",["Executive overview","Portfolio drivers","Portfolio movement","Decision brief","Data & limits"],label_visibility="collapsed")
    st.markdown("---");st.markdown("#### Snapshot filters")
    lo,hi=int(data.Month.min()),int(data.Month.max())
    months=st.slider("Monthly snapshot range",lo,hi,(lo,hi))
    scores=st.multiselect("Credit-score groups",SCORES,default=SCORES)
    mixes=sorted(data.Credit_Mix.dropna().astype(str).unique())
    credit_mix=st.multiselect("Credit mix",mixes,default=mixes)
    st.caption("Movement analysis uses all groups within the selected months. No names, SSNs, or individual records are shown.")
    if USING_DEMO:
        st.caption("Public deployment: synthetic business-demo data.")

period=data[data.Month.between(*months)]
view=period[period.Credit_Score.isin(scores)&period.Credit_Mix.astype(str).isin(credit_mix)]
people=view.Customer_ID.nunique() if len(view) else 0
st.markdown('<div style="color:#607487;font-size:.72rem;font-weight:700;letter-spacing:.12em;margin-bottom:.4rem">BUSINESS INTELLIGENCE / PORTFOLIO ANALYTICS</div>',unsafe_allow_html=True)
if USING_DEMO:
    st.caption("Using synthetic demo data generated for this public business-analysis dashboard. It does not represent real customers or Paisabazaar operations.")

if page=="Executive overview":
    banner("Credit portfolio decision intelligence","Monitor portfolio composition, identify material segment differences, and define the evidence required for better operating decisions.","EXECUTIVE OVERVIEW")
    st.markdown('<div class="notice"><b>Read responsibly:</b> charts summarize groups. They describe associations; they do not explain score changes or predict repayment.</div>',unsafe_allow_html=True)
    if view.empty:st.warning("No records match these filters.");st.stop()
    a,b,c,d=st.columns(4)
    a.metric("Monthly records","{:,}".format(len(view)))
    b.metric("Customers represented","{:,}".format(people))
    c.metric("Good-score share",percent(view.Credit_Score.eq("Good").mean()*100))
    delay=view.Delay_from_due_date.median()
    d.metric("Median reported delay","—" if pd.isna(delay) else "{:.0f} days".format(delay))
    g=view.groupby(["Month","Credit_Score"],observed=True).size().rename("N").reset_index()
    g["Share"]=g.N/g.groupby("Month").N.transform("sum")*100
    composition=view.Credit_Score.value_counts(normalize=True).reindex(SCORES,fill_value=0)*100
    x,y=st.columns([1.45,1])
    with x:
        f=px.area(g,x="Month",y="Share",color="Credit_Score",markers=True,category_orders={"Credit_Score":SCORES},color_discrete_map=COLORS,title="Credit-score mix by monthly snapshot",labels={"Month":"Snapshot month","Share":"Share of records","Credit_Score":"Score group"})
        f.update_yaxes(ticksuffix="%",range=[0,100]);st.plotly_chart(chart_style(f,390),width="stretch")
    with y:
        f=go.Figure(go.Pie(labels=SCORES,values=[composition[s] for s in SCORES],hole=.66,sort=False,marker_colors=[COLORS[s] for s in SCORES],textinfo="label+percent"))
        f.update_layout(title="Selected portfolio composition",showlegend=False,annotations=[dict(text="{:,}".format(len(view)),x=.5,y=.5,font_size=22,showarrow=False),dict(text="records",x=.5,y=.39,font_size=11,showarrow=False)])
        st.plotly_chart(chart_style(f,390),width="stretch")
    monthly_shares=g.pivot(index="Month",columns="Credit_Score",values="Share").reindex(columns=SCORES).fillna(0)
    if not monthly_shares.empty:
        first_month,last_month=int(monthly_shares.index.min()),int(monthly_shares.index.max())
        first_good,last_good=float(monthly_shares.loc[first_month,"Good"]),float(monthly_shares.loc[last_month,"Good"])
        first_poor,last_poor=float(monthly_shares.loc[first_month,"Poor"]),float(monthly_shares.loc[last_month,"Poor"])
        with st.expander("Chart explanation · score mix and monthly trend"):
            st.markdown(
                "**Monthly trend:** each month is normalized to 100% of the selected monthly records. The areas show how the mix of supplied labels changes across snapshots; they do not follow individual customers or show score points.\n\n"
                "**Current filtered comparison:** Good-label share moved from **{:.1f}%** in month {} to **{:.1f}%** in month {}; Poor-label share moved from **{:.1f}%** to **{:.1f}%**. These are record shares, not verified improvements in repayment or creditworthiness.\n\n"
                "**Portfolio composition:** the ring chart summarizes the whole selected date range. A customer can appear repeatedly, so its denominator is monthly records, not distinct customers.\n\n"
                "**Business use and limits:** use the trend to prioritize portfolio investigation, data-quality review, and measurement design. Snapshot changes can reflect different records or reporting patterns; they do not establish why labels changed or which business action caused an effect.".format(
                    first_good,first_month,last_good,last_month,first_poor,last_poor
                )
            )
    st.markdown("### What stands out")
    a,b,c=st.columns(3)
    with a:card("Largest score group","{} accounts for {} of selected monthly records.".format(composition.idxmax(),percent(composition.max())))
    with b:card("Portfolio attention","{} of records are labelled Poor. Review their payment, debt, and inquiry profile before setting an operating hypothesis.".format(percent(composition.get("Poor",0))))
    with c:card("Trend context","Customers recur across months, so monthly records are not unique people.")
    with st.expander("Download aggregate monthly summary"):
        summary=g.pivot(index="Month",columns="Credit_Score",values="Share").reindex(columns=SCORES).fillna(0).reset_index()
        st.download_button("Download score-share CSV",summary.to_csv(index=False).encode(),"credit_health_monthly_aggregate.csv","text/csv")

elif page=="Portfolio drivers":
    banner("Which signals differentiate portfolio segments?","Compare reported credit mix, payment behaviour, debt, and operating indicators across supplied score labels.","PORTFOLIO DRIVERS")
    if view.empty:
        st.warning("No records match these filters.")
        st.stop()
    st.markdown('<div class="notice"><b>How to read this page:</b> every stacked bar is normalized within a score group. Percentages describe filtered customer-month records with reported categories, not unique people. Differences are associations, not proof of cause.</div>',unsafe_allow_html=True)
    t1,t2=st.tabs(["Payment & credit mix","Debt & repayment signals"])
    with t1:
        st.markdown('<div class="section-intro">Compare what customers report in the selected monthly snapshots. Colors identify response categories and remain consistent across filters.</div>',unsafe_allow_html=True)
        a,b=st.columns(2)
        with a:
            fig,grouped,color_map=stacked_share_chart(view,"Credit_Mix","Credit-mix composition",MIX_COLORS)
            if fig is not None:
                st.plotly_chart(chart_style(fig,340,legend=False),width="stretch")
                render_chart_legend(color_map)
                insight_card("Pattern in selected data","Most common reported mix",dominant_category_text(view,"Credit_Mix"))
                st.caption("Bars normalize to 100% among reported categories within each score group. A customer may contribute a row in multiple months.")
                detailed_explanation(
                    "Credit-mix composition",
                    "Each bar compares the share of reported Bad, Standard, and Good credit-mix categories among filtered monthly records in that score group.",
                    "The most common reported category in the current view is: {}. Compare the same color across Poor, Standard, and Good bars; the bar heights are percentages, not counts.".format(category_summary(grouped)),
                    "The distribution helps identify which segments merit further portfolio analysis and whether the credit-mix field is useful in a governed decision workflow.",
                    "Credit mix is associated with the supplied label in this dataset; this chart does not show that changing a person's mix will change their score. Repeated customer-month rows are not independent people, and the source category definitions are not independently verified.",
                    "Validate category definitions, availability timing, and potential leakage with the data owner before using this field in reporting or decision workflows. Do not use this chart alone for an individual decision."
                )
            else:
                st.info("No credit-mix values are available for this filter.")
        with b:
            fig,grouped,color_map=stacked_share_chart(view,"Payment_Behaviour","Reported payment behaviour",BEHAVIOUR_COLORS)
            if fig is not None:
                st.plotly_chart(chart_style(fig,340,legend=False),width="stretch")
                render_chart_legend(color_map)
                insight_card("Pattern in selected data","Most common reported behavior",dominant_category_text(view,"Payment_Behaviour"))
                st.caption("These are named report categories; they are not transaction-level payment amounts.")
                detailed_explanation(
                    "Reported payment behaviour",
                    "Each stacked bar shows the distribution of the dataset's high/low spending and large/medium/small payment-behaviour labels within a score group.",
                    "Most common label by score group in this view: {}. Read each segment as a share of records with a reported category; the legend spells out the category names.".format(category_summary(grouped)),
                    "The distribution may indicate a segment worth deeper operational analysis. It does not show that payment behaviour caused a label or that the field improves a business decision.",
                    "These are pre-labelled categories, not amounts, transaction histories, or a direct measure of whether a customer paid on time. The category semantics and units are not verified in the source.",
                    "Confirm how the source creates these labels, then test whether the field adds predictive or operational value using a time-separated validation set and real outcome data."
                )
            else:
                st.info("No payment-behavior values are available for this filter.")
        st.markdown("#### Minimum-payment response")
        st.markdown('<div class="section-intro">This chart compares the reported response categories. “Not mentioned” is a reporting category and should not be read as “missed payment.”</div>',unsafe_allow_html=True)
        fig,grouped,color_map=stacked_share_chart(view,"Payment_of_Min_Amount","Minimum-payment response categories",MIN_PAYMENT_COLORS)
        if fig is not None:
            st.plotly_chart(chart_style(fig,330,legend=False),width="stretch")
            render_chart_legend(color_map)
            insight_card("Data note","Interpret categories carefully",dominant_category_text(view,"Payment_of_Min_Amount"))
            st.caption("Each denominator includes filtered records with a non-null response category in that score group.")
            detailed_explanation(
                "Minimum-payment response",
                "The chart compares the dataset's recorded Yes, No, and NM responses within each supplied score group.",
                "Most frequent recorded response by score group in this view: {}. Each bar is normalized over records with a non-null response; NM remains a visible response category.".format(category_summary(grouped)),
                "The chart can identify reporting consistency and segment-level differences that merit data-quality review or deeper risk analysis.",
                "NM means the dataset says the response was not mentioned; it is not the same as No, a missed payment, or a default. The chart does not verify actual payment behavior or explain the score label.",
                "Verify the field's data dictionary and missingness process before drawing conclusions. If the field is used in an operating workflow, track stability, missingness, and outcome performance by segment."
            )
        else:
            st.info("No minimum-payment response values are available for this filter.")
    with t2:
        st.markdown('<div class="section-intro">Medians help compare typical values, but source units differ. Use the indexed view to compare relative profiles; select one field to see its original scale.</div>',unsafe_allow_html=True)
        opts={"Payment delay (source units)":"Delay_from_due_date","Outstanding debt (dataset units)":"Outstanding_Debt","Credit utilization (source scale)":"Credit_Utilization_Ratio","Monthly income (dataset units)":"Monthly_Inhand_Salary","Credit inquiries":"Num_Credit_Inquiries","Credit history (months)":"Credit_History_Age"}
        mode=st.radio("View median values as",["Relative index","One field · source scale"],horizontal=True)
        if mode=="Relative index":
            chosen=st.multiselect("Select indicators",list(opts),default=list(opts)[:3])
            if chosen:
                fields=[opts[name] for name in chosen]
                medians=view.groupby("Credit_Score",observed=True)[fields].median().reindex(SCORES)
                overall=view[fields].median()
                indexed=medians.divide(overall.replace(0,np.nan),axis=1).multiply(100)
                indexed=indexed.rename(columns={value:key for key,value in opts.items()}).reset_index()
                melted=indexed.melt(id_vars="Credit_Score",var_name="Indicator",value_name="Index")
                fig=px.bar(melted,x="Indicator",y="Index",color="Credit_Score",barmode="group",title="Group median relative to selected-data median",category_orders={"Credit_Score":SCORES},color_discrete_map=COLORS,labels={"Index":"Index (selected-data median = 100)","Credit_Score":"Score group"})
                fig.add_hline(y=100,line_dash="dot",line_color="#8394A3",annotation_text="Overall median",annotation_position="top left")
                st.plotly_chart(chart_style(fig,430,legend=True),width="stretch")
                insight_card("How to read the index","100 is the median of the filtered records","A value above 100 means the group median is higher than the selected-data median for that field. It is a relative comparison, not a risk score.")
                detailed_explanation(
                    "Relative median indicators",
                    "For every selected field, the chart divides each score group's median by the median across all currently filtered records and multiplies by 100.",
                    "The dotted 100 line is the filtered-data reference. A group at 120 is 20% above that field's reference median; 80 is 20% below. Compare groups within the same field, because fields use different units.",
                    "The chart can help analysts prioritize which portfolio patterns deserve validation or customer research. The direction alone does not identify a useful intervention.",
                    "A median does not describe every customer or the spread of values. Monthly records repeat customers, and a relative index is not a score, probability, causal effect, or personal risk rating.",
                    "Use the original-scale view to check units, inspect distributions and missingness, then validate whether the signal improves a defined business outcome."
                )
            else:
                st.info("Select at least one indicator.")
        else:
            chosen=st.selectbox("Choose one indicator",list(opts))
            column=opts[chosen]
            medians=view.groupby("Credit_Score",observed=True)[column].median().reindex(SCORES).rename("Median").reset_index()
            fig=px.bar(medians,x="Credit_Score",y="Median",color="Credit_Score",category_orders={"Credit_Score":SCORES},color_discrete_map=COLORS,title="Median {}".format(chosen.lower()),labels={"Credit_Score":"Score group","Median":chosen})
            fig.update_layout(showlegend=False)
            st.plotly_chart(chart_style(fig,400,legend=False),width="stretch")
            insight_card("Scale note",chosen,"This displays the median on the source field's scale. Currency, units, and utilization semantics are not verified.")
            median_values=" · ".join("{}: {}".format(row.Credit_Score,format(float(row.Median),",.2f")) for row in medians.itertuples() if pd.notna(row.Median))
            detailed_explanation(
                "Source-scale median · {}".format(chosen),
                "Each bar is the median value of the selected source field among filtered monthly records in that score group.",
                "Current group medians: {}. A median is the middle value after sorting; it is not a typical value for every person.".format(median_values or "No group has a reportable median."),
                "Use this view to describe the observed scale differences and to decide what field definitions should be checked next.",
                "The dataset's currency and field semantics are unverified. Credit utilization is shown on its original source scale, which has not been confirmed as a percentage. Repeated snapshots mean row-level medians are not customer-independent.",
                "Confirm units and definitions with the data owner before setting reporting thresholds or using the field in an operating decision workflow."
            )
        st.caption("Each monthly record is included; repeat snapshots from the same customer are not independent people.")

elif page=="Portfolio movement":
    banner("Monitor aggregate portfolio movement","Compare first and last supplied score labels across the selected observation window.","PORTFOLIO MOVEMENT")
    st.markdown('<div class="notice"><b>Decision use:</b> track whether the portfolio mix is stable or shifting, then investigate the segment, data, or operating-process factors behind material changes. IDs and individual histories are never displayed.</div>',unsafe_allow_html=True)
    if months[0]==months[1]:st.info("Choose at least two snapshots.")
    else:
        d=period.dropna(subset=["Customer_ID"]).sort_values(["Customer_ID","Month"]).groupby("Customer_ID").agg(start=("Credit_Score","first"),end=("Credit_Score","last"),first=("Month","first"),last=("Month","last")).reset_index(drop=True)
        d=d[d.first<d.last]
        if d.empty:st.warning("No customers have two snapshots.")
        else:
            rank={"Poor":0,"Standard":1,"Good":2};delta=d.end.map(rank)-d.start.map(rank);n=len(d)
            a,b,c,e=st.columns(4);a.metric("Profiles tracked","{:,}".format(n));b.metric("Higher label",percent((delta>0).mean()*100));c.metric("Stable label",percent((delta==0).mean()*100));e.metric("Lower label",percent((delta<0).mean()*100))
            count=pd.crosstab(d.start,d.end).reindex(index=SCORES,columns=SCORES,fill_value=0);share=count.div(count.sum(axis=1).replace(0,np.nan),axis=0)*100
            text=[["{:.1f}%<br>n={:,}".format(share.iloc[i,j] if pd.notna(share.iloc[i,j]) else 0,count.iloc[i,j]) for j in range(3)] for i in range(3)]
            f=go.Figure(go.Heatmap(z=share.fillna(0),x=SCORES,y=SCORES,colorscale=[[0,"#F1F5F8"],[.5,"#87B9BE"],[1,"#177E89"]],text=text,texttemplate="%{text}",colorbar=dict(title="Row share",ticksuffix="%")))
            f.update_layout(title="Last label by starting label (row percentages)",xaxis_title="Last snapshot",yaxis_title="First snapshot")
            st.plotly_chart(chart_style(f,410),width="stretch")
            st.caption("Each starting-score row sums to 100%; counts are anonymized profile-level pairs.")
            g=period.groupby(["Month","Credit_Score"],observed=True).size().rename("N").reset_index();g["Share"]=g.N/g.groupby("Month").N.transform("sum")*100
            f=px.line(g,x="Month",y="Share",color="Credit_Score",markers=True,category_orders={"Credit_Score":SCORES},color_discrete_map=COLORS,title="Score-label share across snapshots",labels={"Month":"Month","Share":"Share of records"})
            f.update_yaxes(ticksuffix="%");st.plotly_chart(chart_style(f,340),width="stretch")
            with st.expander("Decision interpretation · portfolio movement and monthly trend"):
                st.markdown(
                    "**First-to-last heatmap:** each row is a starting label and each cell shows the share and count of profiles ending in each label. Row percentages add to 100%. The summary applies the order Poor < Standard < Good; it does not measure numeric score points.\n\n"
                    "**Portfolio movement summary:** {:,} profiles have two or more selected snapshots; {:.1f}% moved to a higher label, {:.1f}% remained stable, and {:.1f}% moved to a lower label. This compares only first and last observations and ignores intermediate movement.\n\n"
                    "**Monthly line chart:** this shows portfolio composition by month. It is not the same calculation as the profile-level heatmap. The movement analysis uses all score groups and credit mixes within the selected months so the full portfolio is visible.\n\n"
                    "**Decision implication:** investigate material shifts with data-quality checks, cohort analysis, and actual outcome data before changing a policy, offer, or operating process. The chart is descriptive and cannot establish cause.".format(
                        n,(delta>0).mean()*100,(delta==0).mean()*100,(delta<0).mean()*100
                    )
                )

elif page=="Decision brief":
    banner("From portfolio signal to decision brief","Select a business lens, compare the segment profile, and define the evidence needed before changing an operating decision.","DECISION BRIEF")
    st.markdown('<div class="notice"><b>Use this for:</b> portfolio monitoring, analytical prioritisation, and decision-design hypotheses. It is not an automated underwriting, pricing, approval, or customer-level recommendation tool.</div>',unsafe_allow_html=True)
    opts={"Payment delays":("Delay_from_due_date","Reported delay (days)","Investigate whether payment-delay distribution is stable by segment and whether it adds value against verified delinquency or repayment outcomes."),"Credit utilization":("Credit_Utilization_Ratio","Utilization (source scale)","Validate the field definition and test its incremental value for a defined portfolio outcome before setting any threshold."),"Outstanding debt":("Outstanding_Debt","Debt (dataset units)","Confirm source units, monitor segment concentration, and evaluate whether debt exposure improves portfolio monitoring when joined to actual outcomes."),"Credit inquiries":("Num_Credit_Inquiries","Inquiry count","Check timing and data lineage, then test whether inquiry patterns add useful, stable information beyond existing portfolio indicators."),"Credit history":("Credit_History_Age","History (months)","Validate history-age derivation and assess whether the pattern is stable across time before using it in segment reporting.")}
    theme=st.selectbox("Business decision lens",list(opts));col,label,idea=opts[theme]
    g=period.groupby("Credit_Score",observed=True)[col].median().reindex(SCORES).dropna().rename("Median").reset_index()
    if not g.empty:
        f=px.bar(g,x="Credit_Score",y="Median",color="Credit_Score",category_orders={"Credit_Score":SCORES},color_discrete_map=COLORS,title="Portfolio median by score label",labels={"Credit_Score":"Score group","Median":label})
        f.update_layout(showlegend=False);st.plotly_chart(chart_style(f,370),width="stretch")
        st.markdown("### Decision hypothesis");card("Recommended analytical next step",idea)
        a,b,c=st.columns(3)
        with a:card("Business outcome","Join verified default, repayment, approval, conversion, or revenue outcomes before measuring impact.")
        with b:card("Decision control","Define an owner, decision threshold, review cadence, and escalation path before operational use.")
        with c:card("Evidence standard","Use a time-separated validation set or controlled experiment before attributing performance to a business change.")
        st.caption("Decision brief uses all score groups and credit mixes for the selected months.")
        detailed_explanation(
            "Decision brief · {}".format(theme),
            "The chart compares the selected indicator's median across supplied score labels for the selected months. The decision hypothesis identifies the next evidence-gathering step; it is not a customer-level recommendation.",
            "Read the bars as descriptive portfolio medians. They may help prioritise analysis, but they do not show which individual should receive an offer or whether a proposed operating change will work.",
            "Use this insight to define a decision owner, a target outcome, an evaluation window, and a comparison strategy. Only adopt an operating rule after it demonstrates value and stability on appropriately governed outcome data.",
            "The dataset does not contain verified default, repayment, applications, approvals, conversion, revenue, or policy-decision outcomes. Business impact cannot be calculated from these charts alone.",
            "Validate units, lineage, availability timing, stability, fairness, and outcome performance before deploying any model or rule. Maintain human review for consequential decisions."
        )

else:
    banner("Understand the evidence before acting","Definitions, calculations, data boundaries, and the limits of portfolio-level conclusions.","DATA & LIMITS")
    st.markdown('<div class="notice"><b>Project purpose:</b> a business-intelligence dashboard for aggregate credit-portfolio analysis and better decision design. It is not an automated credit-scoring, pricing, eligibility, or lending-decision service.</div>',unsafe_allow_html=True)
    st.markdown("### What the dashboard contains")
    col1,col2,col3=st.columns(3)
    with col1:
        st.markdown('<div class="method-card"><h4>{:,} monthly records</h4><p>{:,} customer profiles observed across {} snapshots. A monthly row is not a unique person.</p></div>'.format(len(data),data.Customer_ID.nunique(),data.Month.nunique()),unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="method-card"><h4>Three supplied labels</h4><p>Poor, Standard, and Good are the existing dataset categories, not observed default or repayment outcomes.</p></div>',unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="method-card"><h4>Aggregate-only interface</h4><p>Names, SSNs, and row-level customer detail are not displayed in the dashboard.</p></div>',unsafe_allow_html=True)

    col1,col2=st.columns(2)
    with col1:
        st.markdown("### How to read the charts")
        st.markdown("- **100% stacked bars:** each score-group bar is normalized to 100% after the current filters. Segment size shows a share of filtered monthly records.\n- **Monthly trend:** the denominator is records in each month; profiles can recur in later months.\n- **Median comparison:** typical values are compared by label. The relative-index view sets the filtered-data median to 100 for each selected field.\n- **Portfolio movement:** one first-to-last label pair per profile. It ignores intermediate changes and is not a numeric score change.")
    with col2:
        st.markdown("### Preparation and privacy")
        st.markdown("- ID, Name, and SSN are excluded while reading the CSV. Customer_ID is retained only for aggregate grouping.\n- Numeric-like fields are parsed safely; malformed values become missing.\n- NM is shown as “Not mentioned,” a report category. It is not automatically treated as a missed payment.\n- No text-NLP cleaning is applied because this is structured tabular data.\n- The raw source file contains direct identifiers. Keep it private and review notebook outputs before sharing.")

    if USING_DEMO:
        st.info("This public view uses synthetic demo data. Notebook statistics and model metrics from the private source dataset are intentionally not presented as results for this data.")
    else:
        with st.expander("Notebook statistical tests · full dataset, unfiltered"):
            st.markdown("The notebook summarizes one row per profile before testing, so the 8 monthly snapshots are not treated as 8 independent people. These are exploratory associations; the notebook does not document a multiple-testing correction.")
            st.markdown("- **Income by label:** Good median 45,800.93 vs Poor 31,607.29; one-sided Mann–Whitney U, p = 3.16e-143, rank-biserial correlation = 0.372. Units/currency are unverified.\n- **Credit mix and label:** chi-square(4) = 6,633.64, p < 1e-300 due to numerical underflow; Cramér’s V = 0.515. Association is not an eligibility rule.\n- **Payment delay by label:** Kruskal–Wallis H = 3,004.35, p < 1e-300 due to numerical underflow; epsilon-squared = 0.240. Profile mean delay: Poor 30.00, Standard 19.19, Good 10.66.")

        with st.expander("Notebook model benchmark · label classification, not business-outcome prediction"):
            st.markdown("The notebook fits Logistic Regression to reproduce the dataset’s existing Poor/Standard/Good label. It uses a profile-separated 80/20 split, preprocessing, and macro-F1 tuning. The app does not call this model.")
            st.markdown("- **Test-set accuracy:** 0.668; **balanced accuracy:** 0.711; **macro F1:** 0.662.\n- Tuning did not materially improve macro F1.\n- This does not measure default risk, repayment, approval quality, revenue, or the impact of a business decision. Do not use it for eligibility, pricing, or approval.")

    st.markdown("### What is not measured")
    st.markdown("The data has no verified defaults, delinquency outcomes, loan applications, approvals, policy decisions, conversions, or revenue. Therefore this project cannot establish that any process change will reduce defaults, improve approvals, or increase business performance. Those decisions require governed outcome data, time-based validation, and a defined comparison strategy.")

    if view.empty:
        st.info("No records match the current filters, so the current-view quality summary is empty.")
    else:
        a,b,c=st.columns(3)
        a.metric("Rows in current view","{:,}".format(len(view)))
        b.metric("Customers in current view","{:,}".format(people))
        c.metric("Missing cells in current view","{:,}".format(int(view.isna().sum().sum())))

st.markdown('<div style="padding-top:1.8rem;border-top:1px solid #E2E8EF;margin-top:2rem;color:#718197;font-size:.86rem">Paisabazaar Credit Portfolio Intelligence · Aggregate business analysis · No individual credit decisions</div>',unsafe_allow_html=True)
