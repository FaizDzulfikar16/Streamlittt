import plotly.graph_objects as go
import streamlit as st

from climate_data import apply_page_header, chart_layout, load_data, year_values


data = load_data()
years = year_values(data)

apply_page_header(
	"ANALISIS TEMPORAL",
	"Grafik suhu harian",
	"Bandingkan rata-rata tahunan dan telusuri variasi harian pada satu tahun pilihan.",
)

annual_means = data.groupby("time.year").mean(dim=("time", "latitude", "longitude"))
annual_fig = go.Figure(
	go.Scatter(
		x=[int(year) for year in annual_means.year.values],
		y=annual_means.values,
		mode="lines+markers",
		line=dict(color="#2f7258", width=3),
		marker=dict(size=9, color="#c76a50", line=dict(color="white", width=2)),
		hovertemplate="%{x}: %{y:.1f} °C<extra></extra>",
	)
)
annual_fig.update_yaxes(title="Suhu rata-rata (°C)")
annual_fig.update_xaxes(title=None, dtick=1)
st.plotly_chart(chart_layout(annual_fig, 300), use_container_width=True, config={"displayModeBar": False})

selected_year = st.selectbox("Tahun untuk rincian harian", years, index=len(years) - 1)
year_data = data.where(data.time.dt.year == selected_year, drop=True)
daily_mean = year_data.mean(dim=("latitude", "longitude"))
rolling_mean = daily_mean.rolling(time=7, center=True, min_periods=1).mean()

daily_fig = go.Figure()
daily_fig.add_trace(
	go.Scatter(
		x=daily_mean.time.values,
		y=daily_mean.values,
		mode="lines",
		name="Rata-rata harian",
		line=dict(color="#a9b8ad", width=1),
		hovertemplate="%{x|%d %b}: %{y:.1f} °C<extra></extra>",
	)
)
daily_fig.add_trace(
	go.Scatter(
		x=rolling_mean.time.values,
		y=rolling_mean.values,
		mode="lines",
		name="Tren 7 hari",
		line=dict(color="#2f7258", width=2.5),
		hovertemplate="%{x|%d %b}: %{y:.1f} °C<extra></extra>",
	)
)
daily_fig.update_yaxes(title="Suhu rata-rata (°C)")
daily_fig.update_xaxes(title=None)
st.plotly_chart(chart_layout(daily_fig, 370), use_container_width=True, config={"displayModeBar": False})
