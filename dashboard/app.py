import streamlit as st
import plotly.express as px
from analytics.kpis import frame, summary, grouped, targets
from analytics.trends import daily_revenue
from analytics.insights import generate_insights, alerts
from analytics.anomaly_detection import detect_daily_revenue_anomalies
st.set_page_config(page_title='NexaRetail Analytics',layout='wide')
st.title('NexaRetail | Business Performance Monitor')
d=frame(); st.sidebar.header('Filters'); regions=st.sidebar.multiselect('Region',sorted(d.region.unique()),default=sorted(d.region.unique())); cats=st.sidebar.multiselect('Category',sorted(d.category.unique()),default=sorted(d.category.unique())); d=d[d.region.isin(regions)&d.category.isin(cats)]
page=st.sidebar.radio('Section',['Executive Overview','Sales Analytics','Product Analytics','Customer Analytics','Regional Analytics','Operations Monitoring'])
k=summary(d); cols=st.columns(4)
for col,(label,key,fmt) in zip(cols,[('Net Revenue','total_revenue','${:,.0f}'),('Orders','total_orders','{:,.0f}'),('AOV','average_order_value','${:,.2f}'),('Gross Margin','gross_margin','{:.1%}')]): col.metric(label,fmt.format(k[key]))
if page=='Executive Overview':
    st.plotly_chart(px.line(daily_revenue(),x='order_date',y='revenue',title='Daily completed revenue'),use_container_width=True); a,b=st.columns(2); a.plotly_chart(px.bar(grouped('region',d),x='region',y='revenue',title='Revenue by region'),use_container_width=True); b.plotly_chart(px.bar(grouped('category',d),x='category',y='revenue',title='Revenue by category'),use_container_width=True); st.subheader('Business insights'); [st.write('• '+x) for x in generate_insights()]; st.subheader('Alerts'); [st.warning(x) for x in alerts()]
elif page in ('Sales Analytics','Regional Analytics','Product Analytics'):
    col='sales_channel' if page=='Sales Analytics' else ('region' if page=='Regional Analytics' else 'product_name'); st.plotly_chart(px.bar(grouped(col,d).head(25),x=col,y='revenue',color='profit',title=f'{page} performance'),use_container_width=True); st.dataframe(grouped(col,d).head(50),use_container_width=True)
elif page=='Customer Analytics': st.dataframe(d.groupby('customer_id',as_index=False).net_revenue.sum().sort_values('net_revenue',ascending=False).head(50),use_container_width=True)
else: st.dataframe(__import__('pandas').DataFrame(targets(k)),use_container_width=True); st.dataframe(detect_daily_revenue_anomalies(),use_container_width=True)
