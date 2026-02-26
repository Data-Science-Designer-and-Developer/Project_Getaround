import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="GetAround Dashboard", page_icon="🚗", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx')
    return df

df = load_data()

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/GetAround_logo.svg/1200px-GetAround_logo.svg.png", width=200)
st.sidebar.title("⚙️ Settings")

scope = st.sidebar.radio("Feature scope", options=["All vehicles", "Connect only", "Mobile only"], index=0)
threshold = st.sidebar.slider("Minimum time between 2 rentals (minutes)", min_value=0, max_value=720, value=60, step=15)

st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Reading guide**")
st.sidebar.markdown("Adjust the timeframe and scope to see the impact in real time.")

if scope == "Connect only":
    df_filtered = df[df['checkin_type'] == 'connect']
elif scope == "Mobile only":
    df_filtered = df[df['checkin_type'] == 'mobile']
else:
    df_filtered = df.copy()

st.title("🚗 GetAround — Analysis of checkout delays")
st.markdown("**Objective:** Help the Product Manager decide on the threshold and scope of the minimum delay feature.")
st.markdown("---")

total_rentals = len(df_filtered)
late_mask = df_filtered['delay_at_checkout_in_minutes'] > 0
total_late = late_mask.sum()
pct_late = total_late / df_filtered['delay_at_checkout_in_minutes'].notna().sum() * 100
blocked = df_filtered[df_filtered['time_delta_with_previous_rental_in_minutes'] < threshold]
pct_blocked = len(blocked) / total_rentals * 100
median_delay = df_filtered[late_mask]['delay_at_checkout_in_minutes'].median()

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="📦 Total rentals", value=f"{total_rentals:,}")
col2.metric(label="⏰ Late returns", value=f"{total_late:,}", delta=f"{pct_late:.1f}% of total", delta_color="inverse")
col3.metric(label="⏱️ Median delay", value=f"{median_delay:.0f} min")
col4.metric(label="🚫 Blocked rentals", value=f"{len(blocked):,}", delta=f"{pct_blocked:.1f}% of total", delta_color="inverse")

st.markdown("---")
st.header("📊 Analysis of delays")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Distribution of delays")
    late_data = df_filtered[df_filtered['delay_at_checkout_in_minutes'] > 0]['delay_at_checkout_in_minutes']
    late_data_capped = late_data[late_data <= 720]
    fig1 = px.histogram(late_data_capped, nbins=40, color_discrete_sequence=['#FF6B6B'], labels={'value': 'Delay (minutes)', 'count': 'Number of rentals'})
    fig1.add_vline(x=late_data.median(), line_color="red", annotation_text=f"Median: {late_data.median():.0f}min")
    fig1.add_vline(x=threshold, line_color="blue", line_dash="dash", annotation_text=f"Threshold: {threshold}min")
    fig1.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    st.subheader("Delays: Connect vs Mobile")
    compare = df.groupby('checkin_type').apply(lambda x: pd.Series({
        'Total': len(x),
        'Late': (x['delay_at_checkout_in_minutes'] > 0).sum(),
        'Late %': (x['delay_at_checkout_in_minutes'] > 0).sum() / x['delay_at_checkout_in_minutes'].notna().sum() * 100
    })).reset_index()
    fig2 = px.bar(compare, x='checkin_type', y='Late %', color='checkin_type',
        color_discrete_map={'connect': '#4ECDC4', 'mobile': '#FF6B6B'},
        labels={'checkin_type': 'Check-in type', 'Late %': '% late'}, text='Late %')
    fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig2.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.header("🎯 Impact of the chosen threshold")

thresholds_range = list(range(0, 721, 15))
df_with_prev = df_filtered[df_filtered['previous_ended_rental_id'].notna()].copy()
df_prev_info = df[['rental_id', 'delay_at_checkout_in_minutes']].rename(columns={'rental_id': 'previous_ended_rental_id', 'delay_at_checkout_in_minutes': 'prev_delay'})
df_merged = df_with_prev.merge(df_prev_info, on='previous_ended_rental_id', how='left')
df_merged['was_impacted'] = df_merged['prev_delay'] > df_merged['time_delta_with_previous_rental_in_minutes']
total_problems = df_merged['was_impacted'].sum()

sim_results = []
for t in thresholds_range:
    blocked_count = len(df_filtered[df_filtered['time_delta_with_previous_rental_in_minutes'] < t])
    solved_count = len(df_merged[(df_merged['was_impacted'] == True) & (df_merged['time_delta_with_previous_rental_in_minutes'] < t)])
    sim_results.append({'Threshold (min)': t, 'Blocked rentals': blocked_count, '% blocked': blocked_count / len(df_filtered) * 100,
        'Problems solved': solved_count, '% problems solved': (solved_count / total_problems * 100) if total_problems > 0 else 0})

df_sim = pd.DataFrame(sim_results)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df_sim['Threshold (min)'], y=df_sim['% blocked'], name='% blocked rentals (cost)',
    line=dict(color='#FF6B6B', width=2), fill='tozeroy', fillcolor='rgba(255,107,107,0.1)'))
fig3.add_trace(go.Scatter(x=df_sim['Threshold (min)'], y=df_sim['% problems solved'], name='% problems solved (benefit)',
    line=dict(color='#4ECDC4', width=2), fill='tozeroy', fillcolor='rgba(78,205,196,0.1)'))
fig3.add_vline(x=threshold, line_color="#FFE66D", line_width=3, line_dash="dash", annotation_text=f"Current threshold: {threshold}min")
fig3.update_layout(title="Trade-off: Blocked Rentals vs. Resolved Issues", xaxis_title="Threshold (minutes)", yaxis_title="Percentage (%)", hovermode='x unified', height=400)
st.plotly_chart(fig3, use_container_width=True)

current = df_sim[df_sim['Threshold (min)'] == threshold].iloc[0]
st.info(f"""
**📊 For a threshold of {threshold} minutes:**
- 🚫 Blocked rentals: **{current['Blocked rentals']:.0f}** ({current['% blocked']:.1f}%)
- ✅ Problems resolved: **{current['Problems solved']:.0f}** ({current['% problems solved']:.1f}% of problematic cases)
""")

st.markdown("---")
st.header("💰 Impact on revenue")

col_r1, col_r2 = st.columns(2)

with col_r1:
    st.subheader("Blocked rentals by scope and threshold")
    scope_results = []
    for scope_type in ['connect', 'mobile']:
        df_scope = df[df['checkin_type'] == scope_type]
        for t in [30, 60, 120, 180, 240]:
            blocked_rev = len(df_scope[df_scope['time_delta_with_previous_rental_in_minutes'] < t])
            scope_results.append({'Scope': scope_type, 'Threshold': f"{t}min", 'Blocked': blocked_rev, '% blocked': blocked_rev / len(df_scope) * 100})
    df_scope_results = pd.DataFrame(scope_results)
    fig4 = px.bar(df_scope_results, x='Threshold', y='% blocked', color='Scope', barmode='group', color_discrete_map={'connect': '#4ECDC4', 'mobile': '#FF6B6B'})
    fig4.update_layout(height=350)
    st.plotly_chart(fig4, use_container_width=True)

with col_r2:
    st.subheader("Connect vs Mobile Distribution")
    type_counts = df['checkin_type'].value_counts()
    fig5 = px.pie(values=type_counts.values, names=type_counts.index, color_discrete_map={'connect': '#4ECDC4', 'mobile': '#FF6B6B'})
    fig5.update_layout(height=350)
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
with st.expander("🔍 View raw data"):
    st.dataframe(df_filtered.head(100))
    st.caption(f"Showing first 100 rows out of {len(df_filtered)} total")
