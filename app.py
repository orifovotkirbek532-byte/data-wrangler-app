
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Wrangler & Visualizer", page_icon="🧹", layout="wide")

defaults = {"df":None,"original_df":None,"df_before":None,"filename":None,"transformation_log":[]}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

with st.sidebar:
    st.title("🧹 Data Wrangler")
    if st.session_state.filename:
        st.success(f"📁 {st.session_state.filename}")
        st.metric("Rows",f"{st.session_state.df.shape[0]:,}")
        st.metric("Columns",f"{st.session_state.df.shape[1]}")
        st.metric("Steps applied",len(st.session_state.transformation_log))
        st.divider()
    page = st.radio("Navigate to",[
        "📂 Page A — Upload & Overview",
        "🔧 Page B — Cleaning Studio",
        "📊 Page C — Visualization Builder",
        "📤 Page D — Export & Report"])

def load_file(file):
    n = file.name.lower()
    try:
        if n.endswith(".csv"): return pd.read_csv(file)
        elif n.endswith(".xlsx"): return pd.read_excel(file)
        elif n.endswith(".json"): return pd.read_json(file)
        else: st.error("Unsupported format."); return None
    except Exception as e: st.error(f"Error: {e}"); return None

def log_step(action,details):
    st.session_state.transformation_log.append({"step":len(st.session_state.transformation_log)+1,"action":action,"details":details,"rows_after":len(st.session_state.df),"cols_after":len(st.session_state.df.columns)})

def snapshot():
    st.session_state.df_before = st.session_state.df.copy()

# ═══════════════════════════════════════════════
# PAGE A
# ═══════════════════════════════════════════════
if page == "📂 Page A — Upload & Overview":
    st.title("🧹 AI-Assisted Data Wrangler & Visualizer")
    st.header("📂 Page A — Upload & Overview"); st.divider()
    if st.button("🔄 Reset Session",type="secondary"):
        for k,v in defaults.items(): st.session_state[k]=v
        st.rerun()
    uf = st.file_uploader("📁 Upload your dataset",type=["csv","xlsx","json"])
    if uf is not None:
        if st.session_state.filename != uf.name:
            df = load_file(uf)
            if df is not None:
                st.session_state.df=df.copy(); st.session_state.original_df=df.copy()
                st.session_state.filename=uf.name; st.session_state.transformation_log=[]
                st.success(f"✅ '{uf.name}' loaded!")
    if st.session_state.df is not None:
        df=st.session_state.df
        st.subheader("📊 Quick Overview")
        c1,c2,c3,c4=st.columns(4)
        c1.metric("📋 Rows",f"{df.shape[0]:,}"); c2.metric("📌 Columns",f"{df.shape[1]}")
        c3.metric("🕳️ Missing",f"{df.isnull().sum().sum():,}"); c4.metric("🔁 Duplicates",f"{df.duplicated().sum():,}")
        st.info(f"📦 Number of columns: **{df.shape[1]}**"); st.divider()
        st.subheader("🗂️ Column Names & Data Types")
        st.dataframe(pd.DataFrame({"Column":df.columns.tolist(),"Type":df.dtypes.astype(str).tolist(),"Non-Null":df.notnull().sum().tolist(),"Null Count":df.isnull().sum().tolist(),"Null %":(df.isnull().sum()/len(df)*100).round(2).tolist()}),use_container_width=True,hide_index=True)
        st.divider(); st.subheader("📈 Summary Statistics")
        t1,t2=st.tabs(["🔢 Numeric","🔤 Categorical"])
        with t1:
            num=df.select_dtypes(include="number")
            st.dataframe(num.describe().T.round(3),use_container_width=True) if not num.empty else st.info("No numeric columns.")
        with t2:
            cat=df.select_dtypes(include=["object","category"])
            st.dataframe(pd.DataFrame({"Column":cat.columns.tolist(),"Unique":cat.nunique().tolist(),"Top":[cat[c].mode().iloc[0] if not cat[c].dropna().empty else "N/A" for c in cat.columns]}),use_container_width=True,hide_index=True) if not cat.empty else st.info("No categorical columns.")
        st.divider(); st.subheader("🕳️ Missing Values")
        miss=df.isnull().sum()
        mdf=pd.DataFrame({"Column":miss.index,"Missing":miss.values,"Missing %":(miss/len(df)*100).round(2).values})
        mdf=mdf[mdf["Missing"]>0].sort_values("Missing %",ascending=False)
        st.success("✅ No missing values!") if mdf.empty else st.dataframe(mdf,use_container_width=True,hide_index=True)
        st.divider(); st.subheader("👀 Data Preview")
        st.dataframe(df.head(st.slider("Rows",5,50,10,5)),use_container_width=True)
    else:
        st.info("👆 Upload a file above to begin.")

# ═══════════════════════════════════════════════
# PAGE B
# ═══════════════════════════════════════════════
elif page == "🔧 Page B — Cleaning Studio":
    st.title("🔧 Page B — Cleaning Studio")
    if st.session_state.df is None: st.warning("⚠️ Upload a dataset on Page A first."); st.stop()
    df=st.session_state.df
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Rows",f"{df.shape[0]:,}"); c2.metric("Columns",f"{df.shape[1]}")
    c3.metric("Missing",f"{df.isnull().sum().sum():,}"); c4.metric("Steps",len(st.session_state.transformation_log))
    if st.session_state.df_before is not None and st.session_state.transformation_log:
        if st.button("↩️ Undo Last Step"):
            st.session_state.df=st.session_state.df_before.copy(); st.session_state.df_before=None
            st.session_state.transformation_log.pop(); st.toast("✅ Undone!"); st.rerun()
    st.divider()

    with st.expander("1️⃣  Missing Values"):
        miss=df.isnull().sum(); mc=miss[miss>0].index.tolist()
        if not mc: st.success("✅ No missing values!")
        else:
            st.warning(f"⚠️ Missing in: {', '.join(mc)}")
            act=st.radio("Action",["Fill missing values","Drop rows","Drop columns"],key="mv_a")
            if act=="Fill missing values":
                col=st.selectbox("Column",mc,key="mv_c"); meth=st.selectbox("Method",["Mean","Median","Mode","Forward Fill (ffill)","Backward Fill (bfill)","Custom Value"],key="mv_m")
                cval=st.text_input("Custom value",key="mv_cv") if meth=="Custom Value" else ""
                if st.button("✅ Apply",key="mv_ap"):
                    snapshot(); s=st.session_state.df
                    if meth=="Mean": s[col]=s[col].fillna(s[col].mean())
                    elif meth=="Median": s[col]=s[col].fillna(s[col].median())
                    elif meth=="Mode": s[col]=s[col].fillna(s[col].mode()[0])
                    elif meth=="Forward Fill (ffill)": s[col]=s[col].ffill()
                    elif meth=="Backward Fill (bfill)": s[col]=s[col].bfill()
                    else: s[col]=s[col].fillna(cval)
                    log_step("Fill Missing",f"{col} | {meth}"); st.toast("✅ Done!"); st.rerun()
            elif act=="Drop rows":
                sub=st.multiselect("Columns (empty=all)",df.columns.tolist(),key="mv_dr")
                sv=sub or None; nd=df[df.isnull().any(axis=1)].shape[0] if sv is None else df[df[sv].isnull().any(axis=1)].shape[0]
                st.info(f"Rows to remove: {nd}")
                if st.button("✅ Drop",key="mv_drb"):
                    snapshot(); rb=len(st.session_state.df); st.session_state.df=st.session_state.df.dropna(subset=sv).reset_index(drop=True)
                    log_step("Drop Rows",f"Removed:{rb-len(st.session_state.df)}"); st.toast("✅ Done!"); st.rerun()
            else:
                thr=st.slider("Drop cols with >X% missing",0,100,50,key="mv_t")
                dt=[c for c in df.columns if(df[c].isnull().sum()/len(df)*100)>thr]
                st.info(f"To drop: {dt or 'None'}")
                if dt and st.button("✅ Drop",key="mv_dcb"):
                    snapshot(); st.session_state.df=st.session_state.df.drop(columns=dt)
                    log_step("Drop Columns",f"{dt}"); st.toast("✅ Done!"); st.rerun()

    with st.expander("2️⃣  Duplicate Rows"):
        nd=df.duplicated().sum()
        if nd==0: st.success("✅ No duplicates!")
        else:
            st.warning(f"⚠️ {nd} duplicate rows found.")
            sub=st.multiselect("Check on columns (empty=all)",df.columns.tolist(),key="dp_s")
            keep=st.radio("Keep",["first","last","none — drop all"],key="dp_k")
            kv=False if "none" in keep else keep; sv=sub or None
            st.info(f"Rows to remove: {df.duplicated(subset=sv,keep=kv).sum()}")
            if st.checkbox("Preview duplicates",key="dp_pr"): st.dataframe(df[df.duplicated(subset=sv,keep=False)].head(10),use_container_width=True)
            if st.button("✅ Remove",key="dp_ap"):
                snapshot(); rb=len(st.session_state.df); st.session_state.df=st.session_state.df.drop_duplicates(subset=sv,keep=kv).reset_index(drop=True)
                log_step("Remove Duplicates",f"Removed:{rb-len(st.session_state.df)}"); st.toast("✅ Done!"); st.rerun()

    with st.expander("3️⃣  Data Types"):
        col=st.selectbox("Column",df.columns.tolist(),key="dt_c")
        st.caption(f"Type: {df[col].dtype} | Sample: {df[col].dropna().head(3).tolist()}")
        tgt=st.selectbox("Convert to",["Numeric (float)","Numeric (integer)","Text (string)","Datetime","Category"],key="dt_t")
        if st.button("✅ Convert",key="dt_ap"):
            snapshot(); s=st.session_state.df
            try:
                if tgt=="Numeric (float)": s[col]=pd.to_numeric(s[col],errors="coerce")
                elif tgt=="Numeric (integer)": s[col]=pd.to_numeric(s[col],errors="coerce").astype("Int64")
                elif tgt=="Text (string)": s[col]=s[col].astype(str)
                elif tgt=="Datetime": s[col]=pd.to_datetime(s[col],errors="coerce")
                elif tgt=="Category": s[col]=s[col].astype("category")
                log_step("Convert Type",f"{col} → {tgt}"); st.toast("✅ Done!"); st.rerun()
            except Exception as e: st.error(f"❌ {e}")

    with st.expander("4️⃣  Categorical Tools"):
        cc=df.select_dtypes(include=["object","category"]).columns.tolist()
        if not cc: st.info("No categorical columns.")
        else:
            col=st.selectbox("Column",cc,key="ct_c"); act=st.radio("Action",["Trim & fix case","Group rare categories","Replace a value"],key="ct_a")
            if act=="Trim & fix case":
                case=st.selectbox("Case",["lowercase","UPPERCASE","Title Case","No change"],key="ct_cs")
                if st.button("✅ Apply",key="ct_ap"):
                    snapshot(); s=st.session_state.df; s[col]=s[col].astype(str).str.strip()
                    if case=="lowercase": s[col]=s[col].str.lower()
                    elif case=="UPPERCASE": s[col]=s[col].str.upper()
                    elif case=="Title Case": s[col]=s[col].str.title()
                    log_step("Fix Case",f"{col}|{case}"); st.toast("✅ Done!"); st.rerun()
            elif act=="Group rare categories":
                thr=st.slider("Less than X%",1,25,5,key="ct_t"); vc=df[col].value_counts(normalize=True)*100; rare=vc[vc<thr].index.tolist()
                repl=st.text_input("Replace with","Other",key="ct_r"); st.info(f"Rare: {rare}")
                if rare and st.button("✅ Group",key="ct_gb"):
                    snapshot(); st.session_state.df[col]=st.session_state.df[col].replace(rare,repl)
                    log_step("Group Rare",f"{col}"); st.toast("✅ Done!"); st.rerun()
            else:
                uv=df[col].dropna().unique().tolist(); ov=st.selectbox("Replace",uv,key="ct_ov"); nv=st.text_input("With",key="ct_nv")
                if nv and st.button("✅ Replace",key="ct_rb"):
                    snapshot(); st.session_state.df[col]=st.session_state.df[col].replace(ov,nv)
                    log_step("Replace Value",f"{ov}→{nv}"); st.toast("✅ Done!"); st.rerun()

    with st.expander("5️⃣  Outlier Detection"):
        nc=df.select_dtypes(include="number").columns.tolist()
        if not nc: st.info("No numeric columns.")
        else:
            col=st.selectbox("Column",nc,key="od_c"); meth=st.radio("Method",["IQR","Z-Score"],key="od_m"); cd=df[col].dropna()
            if meth=="IQR":
                Q1,Q3=cd.quantile(0.25),cd.quantile(0.75); IQR=Q3-Q1; lo,hi=Q1-1.5*IQR,Q3+1.5*IQR
                out=cd[(cd<lo)|(cd>hi)]; st.info(f"IQR [{lo:.2f},{hi:.2f}] → {len(out)} outliers")
            else:
                zt=st.slider("Z threshold",1.0,4.0,3.0,0.1,key="od_zt"); zs=np.abs(stats.zscore(cd)); out=cd[zs>zt]; st.info(f"Z>{zt} → {len(out)} outliers")
            if len(out)>0:
                st.caption(f"Sample: {sorted(out.tolist())[:5]}")
                act=st.radio("Action",["Cap values","Remove rows"],key="od_a")
                if st.button("✅ Apply",key="od_ap"):
                    snapshot(); rb=len(st.session_state.df); s=st.session_state.df
                    if meth=="IQR":
                        if act=="Cap values": s[col]=s[col].clip(lo,hi); log_step("Cap Outliers IQR",col)
                        else:
                            st.session_state.df=s[(s[col]>=lo)&(s[col]<=hi)].reset_index(drop=True)
                            log_step("Remove Outliers IQR",f"Removed:{rb-len(st.session_state.df)}")
                    else:
                        za=np.abs(stats.zscore(s[col].fillna(s[col].mean())))
                        if act=="Cap values":
                            mn,sd=s[col].mean(),s[col].std(); s[col]=s[col].clip(mn-zt*sd,mn+zt*sd); log_step("Cap Outliers Z",col)
                        else:
                            st.session_state.df=s[za<=zt].reset_index(drop=True)
                            log_step("Remove Outliers Z",f"Removed:{rb-len(st.session_state.df)}")
                    st.toast("✅ Done!"); st.rerun()
            else: st.success("✅ No outliers!")

    with st.expander("6️⃣  Normalisation & Scaling"):
        nc=df.select_dtypes(include="number").columns.tolist()
        if not nc: st.info("No numeric columns.")
        else:
            col=st.selectbox("Column",nc,key="ns_c"); meth=st.radio("Method",["Min-Max (0 to 1)","Z-Score (mean=0, std=1)"],key="ns_m")
            cd=df[col].dropna(); c1,c2,c3=st.columns(3)
            c1.metric("Min",f"{cd.min():.3f}"); c2.metric("Mean",f"{cd.mean():.3f}"); c3.metric("Max",f"{cd.max():.3f}")
            if st.button("✅ Scale",key="ns_ap"):
                snapshot(); s=st.session_state.df
                if "Min-Max" in meth:
                    mn,mx=s[col].min(),s[col].max()
                    if mx==mn: st.error("All values identical.")
                    else: s[col]=(s[col]-mn)/(mx-mn); log_step("Min-Max Scale",col); st.toast("✅ Done!"); st.rerun()
                else:
                    mn,sd=s[col].mean(),s[col].std()
                    if sd==0: st.error("Std=0.")
                    else: s[col]=(s[col]-mn)/sd; log_step("Z-Score Scale",col); st.toast("✅ Done!"); st.rerun()

    with st.expander("7️⃣  Column Operations"):
        op=st.radio("Operation",["Rename","Drop columns","Create column"],key="co_op")
        if op=="Rename":
            old=st.selectbox("Column",df.columns.tolist(),key="co_old"); new=st.text_input("New name",key="co_new")
            if new and st.button("✅ Rename",key="co_rb"):
                snapshot(); st.session_state.df=st.session_state.df.rename(columns={old:new})
                log_step("Rename",f"{old}→{new}"); st.toast("✅ Done!"); st.rerun()
        elif op=="Drop columns":
            td=st.multiselect("Select columns",df.columns.tolist(),key="co_td")
            if td:
                st.warning(f"Will drop: {td}")
                if st.button("✅ Drop",key="co_db"):
                    snapshot(); st.session_state.df=st.session_state.df.drop(columns=td)
                    log_step("Drop Columns",f"{td}"); st.toast("✅ Done!"); st.rerun()
        else:
            nn=st.text_input("New column name",key="co_nn"); how=st.radio("How?",["Formula","Bin numeric column"],key="co_how")
            if how=="Formula":
                fm=st.text_input("Formula (e.g. Unit_Price * Quantity)",key="co_fm"); st.caption(f"Columns: {df.columns.tolist()}")
                if nn and fm and st.button("✅ Create",key="co_cb"):
                    try:
                        snapshot(); st.session_state.df[nn]=st.session_state.df.eval(fm)
                        log_step("Create Column",f"{nn}={fm}"); st.toast("✅ Done!"); st.rerun()
                    except Exception as e: st.error(f"❌ {e}")
            else:
                nc2=df.select_dtypes(include="number").columns.tolist(); bc=st.selectbox("Column to bin",nc2,key="co_bc")
                nb=st.slider("Bins",2,10,4,key="co_nb"); li=st.text_input("Labels","Low,Medium,High,Very High",key="co_li")
                lb=[l.strip() for l in li.split(",")]
                if len(lb)!=nb: st.warning(f"⚠️ {len(lb)} labels ≠ {nb} bins")
                elif nn and st.button("✅ Bin",key="co_bb"):
                    try:
                        snapshot(); st.session_state.df[nn]=pd.cut(st.session_state.df[bc],bins=nb,labels=lb)
                        log_step("Bin Column",f"{bc}→{nn}"); st.toast("✅ Done!"); st.rerun()
                    except Exception as e: st.error(f"❌ {e}")

    with st.expander("8️⃣  Data Validation"):
        vt=st.radio("Rule",["Numeric range","Allowed categories","Non-null check"],key="dv_t")
        if vt=="Numeric range":
            nc=df.select_dtypes(include="number").columns.tolist(); vc=st.selectbox("Column",nc,key="dv_nc")
            c1,c2=st.columns(2); vmn=c1.number_input("Min",value=float(df[vc].min()),key="dv_mn"); vmx=c2.number_input("Max",value=float(df[vc].max()),key="dv_mx")
            if st.button("🔍 Check",key="dv_nb"):
                v=df[(df[vc]<vmn)|(df[vc]>vmx)]
                st.success("✅ No violations!") if v.empty else st.error(f"❌ {len(v)} violations!") or st.dataframe(v,use_container_width=True)
                log_step("Validate Range",f"{vc}[{vmn},{vmx}] Violations:{len(v)}")
        elif vt=="Allowed categories":
            cc2=df.select_dtypes(include=["object","category"]).columns.tolist(); vc=st.selectbox("Column",cc2,key="dv_cc")
            av=df[vc].dropna().unique().tolist(); al=st.multiselect("Allowed",av,default=av,key="dv_al")
            if st.button("🔍 Check",key="dv_cb"):
                v=df[~df[vc].isin(al)&df[vc].notna()]
                st.success("✅ No violations!") if v.empty else st.error(f"❌ {len(v)} violations!") or st.dataframe(v,use_container_width=True)
                log_step("Validate Categories",f"{vc} Violations:{len(v)}")
        else:
            vc=st.selectbox("Column",df.columns.tolist(),key="dv_nullc")
            if st.button("🔍 Check",key="dv_nullb"):
                nc3=df[vc].isnull().sum()
                st.success(f"✅ No nulls in '{vc}'!") if nc3==0 else st.error(f"❌ {nc3} nulls!") or st.dataframe(df[df[vc].isnull()],use_container_width=True)
                log_step("Validate Nulls",f"{vc} Nulls:{nc3}")

    st.divider(); st.subheader("📋 Transformation Log")
    st.info("No steps yet.") if not st.session_state.transformation_log else st.dataframe(pd.DataFrame(st.session_state.transformation_log),use_container_width=True,hide_index=True)
    st.subheader("👀 Current Dataset"); st.dataframe(df.head(10),use_container_width=True)

# ═══════════════════════════════════════════════
# PAGE C
# ═══════════════════════════════════════════════
elif page == "📊 Page C — Visualization Builder":
    st.title("📊 Page C — Visualization Builder")
    if st.session_state.df is None: st.warning("⚠️ Upload a dataset on Page A first."); st.stop()
    df=st.session_state.df
    num_cols=df.select_dtypes(include="number").columns.tolist()
    cat_cols=df.select_dtypes(include=["object","category"]).columns.tolist()
    all_cols=df.columns.tolist()
    if not num_cols: st.warning("⚠️ No numeric columns."); st.stop()

    st.subheader("🎨 Choose Chart Type")
    chart=st.selectbox("Chart type",["📊 Histogram","📦 Box Plot","🔵 Scatter Plot","📈 Line Chart","📊 Grouped Bar Chart","🌡️ Correlation Heatmap"],key="chart")
    st.divider()

    with st.expander("🔍 Filters (optional)"):
        fdf=df.copy()
        if cat_cols:
            fc=st.selectbox("Filter by category",["None"]+cat_cols,key="fc")
            if fc!="None":
                uv=df[fc].dropna().unique().tolist(); sv=st.multiselect(f"{fc} values",uv,default=uv,key="fc_v")
                fdf=fdf[fdf[fc].isin(sv)]
        if num_cols:
            fn=st.selectbox("Filter by range",["None"]+num_cols,key="fn")
            if fn!="None":
                mn2,mx2=float(df[fn].min()),float(df[fn].max())
                if mn2<mx2:
                    rng=st.slider(fn,mn2,mx2,(mn2,mx2),key="fn_r")
                    fdf=fdf[(fdf[fn]>=rng[0])&(fdf[fn]<=rng[1])]
        st.caption(f"Rows: {len(fdf):,} / {len(df):,}")
    st.divider()

    COLORS=["#4CAF50","#2196F3","#FF9800","#E91E63","#9C27B0","#00BCD4","#FF5722","#8BC34A"]

    def sfig():
        fig,ax=plt.subplots(figsize=(10,5))
        fig.patch.set_facecolor("#0e1117"); ax.set_facecolor("#161b22")
        ax.tick_params(colors="white",labelsize=9); ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white"); ax.title.set_color("white")
        for s in ax.spines.values(): s.set_edgecolor("#444")
        return fig,ax

    try:
        if chart=="📊 Histogram":
            col=st.selectbox("Column",num_cols,key="h_c"); bins=st.slider("Bins",5,100,30,key="h_b")
            fig,ax=sfig(); ax.hist(fdf[col].dropna(),bins=bins,color=COLORS[0],edgecolor="#333",alpha=0.85)
            ax.set_xlabel(col); ax.set_ylabel("Frequency"); ax.set_title(f"Histogram — {col}")
            plt.tight_layout(); st.pyplot(fig); plt.close()

        elif chart=="📦 Box Plot":
            cols=st.multiselect("Columns",num_cols,default=num_cols[:4] if len(num_cols)>=4 else num_cols,key="bp_c")
            if cols:
                fig,ax=sfig(); data=[fdf[c].dropna().values for c in cols]
                bp=ax.boxplot(data,labels=cols,patch_artist=True)
                for patch,c in zip(bp["boxes"],COLORS): patch.set_facecolor(c); patch.set_alpha(0.75)
                for el in ["whiskers","caps","medians"]:
                    for item in bp[el]: item.set_color("white")
                ax.set_ylabel("Value"); ax.set_title("Box Plot")
                plt.xticks(rotation=30,ha="right",color="white"); plt.tight_layout(); st.pyplot(fig); plt.close()

        elif chart=="🔵 Scatter Plot":
            xc=st.selectbox("X axis",num_cols,key="sc_x"); yc=st.selectbox("Y axis",num_cols,index=min(1,len(num_cols)-1),key="sc_y")
            cc2=st.selectbox("Colour by (optional)",["None"]+cat_cols,key="sc_c")
            fig,ax=sfig()
            if cc2!="None" and cc2 in fdf.columns:
                cats=fdf[cc2].dropna().unique(); cmap=plt.cm.Set2(range(len(cats)))
                for cat,col in zip(cats,cmap):
                    m=fdf[cc2]==cat; ax.scatter(fdf.loc[m,xc],fdf.loc[m,yc],label=str(cat),alpha=0.6,s=18,color=col)
                ax.legend(fontsize=8,facecolor="#222",edgecolor="#555",labelcolor="white")
            else: ax.scatter(fdf[xc],fdf[yc],alpha=0.5,s=15,color=COLORS[0])
            ax.set_xlabel(xc); ax.set_ylabel(yc); ax.set_title(f"Scatter — {xc} vs {yc}")
            plt.tight_layout(); st.pyplot(fig); plt.close()

        elif chart=="📈 Line Chart":
            xc=st.selectbox("X axis",all_cols,key="lc_x"); yc=st.selectbox("Y axis",num_cols,key="lc_y")
            agg=st.selectbox("Aggregation",["None","Mean","Sum","Count","Median"],key="lc_a")
            pdf=fdf[[xc,yc]].dropna().sort_values(xc)
            if agg!="None":
                fn2={"Mean":"mean","Sum":"sum","Count":"count","Median":"median"}[agg]
                pdf=pdf.groupby(xc)[yc].agg(fn2).reset_index()
            labels=pdf[xc].astype(str).tolist(); vals=pdf[yc].tolist()
            fig,ax=sfig(); ax.plot(range(len(vals)),vals,color=COLORS[0],linewidth=1.8,marker="o",markersize=3)
            step=max(1,len(labels)//10); ax.set_xticks(range(0,len(labels),step))
            ax.set_xticklabels(labels[::step],rotation=45,ha="right",fontsize=8,color="white")
            ax.set_xlabel(xc); ax.set_ylabel(yc); ax.set_title(f"Line — {yc} over {xc}")
            plt.tight_layout(); st.pyplot(fig); plt.close()

        elif chart=="📊 Grouped Bar Chart":
            cc3=st.selectbox("Category (X)",cat_cols if cat_cols else all_cols,key="gb_c")
            nc4=st.selectbox("Numeric (Y)",num_cols,key="gb_n"); agg=st.selectbox("Aggregation",["Mean","Sum","Count","Median"],key="gb_a")
            fn3={"Mean":"mean","Sum":"sum","Count":"count","Median":"median"}[agg]
            pdf2=fdf.groupby(cc3)[nc4].agg(fn3).reset_index().sort_values(nc4,ascending=False)
            fig,ax=sfig(); cmap2=plt.cm.Set2(range(len(pdf2)))
            bars=ax.bar(pdf2[cc3].astype(str),pdf2[nc4],color=cmap2,edgecolor="#333",alpha=0.85)
            for bar in bars:
                h=bar.get_height(); ax.text(bar.get_x()+bar.get_width()/2.,h,f"{h:.1f}",ha="center",va="bottom",color="white",fontsize=8)
            ax.set_xlabel(cc3); ax.set_ylabel(f"{agg} of {nc4}"); ax.set_title(f"{agg} of {nc4} by {cc3}")
            plt.xticks(rotation=30,ha="right",color="white"); plt.tight_layout(); st.pyplot(fig); plt.close()

        elif chart=="🌡️ Correlation Heatmap":
            sel=st.multiselect("Numeric columns",num_cols,default=num_cols[:6] if len(num_cols)>=6 else num_cols,key="hm_s")
            if len(sel)>=2:
                corr=fdf[sel].corr(); fig,ax=sfig()
                im=ax.imshow(corr.values,cmap="RdYlGn",vmin=-1,vmax=1,aspect="auto"); plt.colorbar(im,ax=ax)
                ax.set_xticks(range(len(sel))); ax.set_yticks(range(len(sel)))
                ax.set_xticklabels(sel,rotation=45,ha="right",fontsize=9,color="white")
                ax.set_yticklabels(sel,fontsize=9,color="white")
                for i in range(len(sel)):
                    for j in range(len(sel)):
                        v=corr.values[i,j]; ax.text(j,i,f"{v:.2f}",ha="center",va="center",color="black" if abs(v)<0.5 else "white",fontsize=8,fontweight="bold")
                ax.set_title("Correlation Heatmap"); plt.tight_layout(); st.pyplot(fig); plt.close()
            else: st.info("Select at least 2 columns.")

    except Exception as e: st.error(f"❌ Chart error: {e}"); plt.close("all")

# ═══════════════════════════════════════════════
# PAGE D
# ═══════════════════════════════════════════════

elif page == "📤 Page D — Export & Report":
    st.title("📤 Page D — Export & Report")

    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset on Page A first.")
        st.stop()

    import json, io
    from datetime import datetime

    df      = st.session_state.df
    orig_df = st.session_state.original_df
    log     = st.session_state.transformation_log

    # ── Summary metrics ───────────────────────────────────
    st.subheader("📊 Cleaning Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Steps Applied",    len(log))
    c2.metric("Rows Removed",     f"{len(orig_df) - len(df):,}",
              delta=f"-{len(orig_df)-len(df)}", delta_color="inverse")
    c3.metric("Missing Cells Now",f"{df.isnull().sum().sum():,}",
              delta=f"-{orig_df.isnull().sum().sum()-df.isnull().sum().sum()}",
              delta_color="inverse")
    c4.metric("Columns Now",      f"{df.shape[1]}")
    st.divider()

    # ── Before vs After comparison ────────────────────────
    st.subheader("🔄 Before vs After")
    t1, t2 = st.columns(2)
    with t1:
        st.caption("**Original Dataset**")
        st.dataframe(pd.DataFrame({
            "Metric":["Rows","Columns","Missing Cells","Duplicate Rows"],
            "Value":[f"{len(orig_df):,}", f"{orig_df.shape[1]}",
                     f"{orig_df.isnull().sum().sum():,}",
                     f"{orig_df.duplicated().sum():,}"]
        }), use_container_width=True, hide_index=True)
    with t2:
        st.caption("**Cleaned Dataset**")
        st.dataframe(pd.DataFrame({
            "Metric":["Rows","Columns","Missing Cells","Duplicate Rows"],
            "Value":[f"{len(df):,}", f"{df.shape[1]}",
                     f"{df.isnull().sum().sum():,}",
                     f"{df.duplicated().sum():,}"]
        }), use_container_width=True, hide_index=True)
    st.divider()

    # ── Transformation log ────────────────────────────────
    st.subheader("📋 Transformation Log")
    if not log:
        st.info("No cleaning steps were applied. Go to Page B to clean your data.")
    else:
        st.dataframe(pd.DataFrame(log), use_container_width=True, hide_index=True)
    st.divider()

    # ── Downloads ─────────────────────────────────────────
    st.subheader("⬇️ Download Files")

    col1, col2, col3 = st.columns(3)

    # 1. Download cleaned CSV
    with col1:
        st.markdown("**📄 Cleaned Dataset**")
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_buf.getvalue(),
            file_name=f"cleaned_{st.session_state.filename or 'dataset.csv'}",
            mime="text/csv",
            use_container_width=True
        )
        st.caption(f"{len(df):,} rows × {df.shape[1]} columns")

    # 2. Download transformation log as JSON
    with col2:
        st.markdown("**📋 Transformation Log**")
        report = {
            "generated_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "original_file":  st.session_state.filename,
            "original_shape": {"rows": len(orig_df), "columns": orig_df.shape[1]},
            "cleaned_shape":  {"rows": len(df),      "columns": df.shape[1]},
            "steps_applied":  len(log),
            "transformation_log": log
        }
        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(report, indent=2, default=str),
            file_name="transformation_report.json",
            mime="application/json",
            use_container_width=True
        )
        st.caption(f"{len(log)} steps recorded")

    # 3. Download human-readable text report
    with col3:
        st.markdown("**📝 Text Report**")
        lines = [
            "=" * 50,
            "  AI-ASSISTED DATA WRANGLER — TRANSFORMATION REPORT",
            "=" * 50,
            f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"File      : {st.session_state.filename}",
            "",
            "BEFORE CLEANING",
            f"  Rows          : {len(orig_df):,}",
            f"  Columns       : {orig_df.shape[1]}",
            f"  Missing cells : {orig_df.isnull().sum().sum():,}",
            f"  Duplicates    : {orig_df.duplicated().sum():,}",
            "",
            "AFTER CLEANING",
            f"  Rows          : {len(df):,}",
            f"  Columns       : {df.shape[1]}",
            f"  Missing cells : {df.isnull().sum().sum():,}",
            f"  Duplicates    : {df.duplicated().sum():,}",
            "",
            f"STEPS APPLIED ({len(log)})",
        ]
        for s in log:
            lines.append(f"  Step {s['step']}: {s['action']} — {s['details']}")
        lines += ["", "=" * 50]
        txt_report = "\n".join(lines)
        st.download_button(
            label="⬇️ Download TXT",
            data=txt_report,
            file_name="transformation_report.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.caption("Human-readable summary")

    st.divider()

    # ── Preview cleaned data ──────────────────────────────
    st.subheader("👀 Cleaned Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # ── Column stats comparison ───────────────────────────
    st.subheader("📈 Column-by-Column Missing Values: Before vs After")
    miss_orig = orig_df.isnull().sum()
    miss_clean = df.isnull().sum()
    common_cols = [c for c in orig_df.columns if c in df.columns]
    comp_df = pd.DataFrame({
        "Column":          common_cols,
        "Missing (Before)": [int(miss_orig.get(c, 0)) for c in common_cols],
        "Missing (After)":  [int(miss_clean.get(c, 0)) for c in common_cols],
        "Improvement":      [int(miss_orig.get(c,0)) - int(miss_clean.get(c,0)) for c in common_cols],
    }).sort_values("Improvement", ascending=False)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

