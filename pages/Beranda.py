import plotly.graph_objects as go
import streamlit as st

from climate_data import (
	LOGO_BMKG,
	LOGO_UPI,
	apply_page_header,
	chart_layout,
	format_value,
	load_data,
	render_data_notice,
	year_values,
)


data = load_data()
years = year_values(data)
annual_means = data.groupby("time.year").mean(dim=("time", "latitude", "longitude"))
overall_mean = float(data.mean())
minimum = float(data.min())
maximum = float(data.max())

logo_left, title_col, logo_right = st.columns([1, 7, 1])
with logo_left:
	st.image(str(LOGO_BMKG), width=72)
with title_col:
	apply_page_header(
		"BMKG x UPI / DATA IKLIM",
		"Ringkasan suhu harian",
		"Eksplorasi data suhu udara rata-rata harian pada grid wilayah Jawa Barat, 2021-2025.",
	)
with logo_right:
	st.image(str(LOGO_UPI), width=72)

render_data_notice()
st.write("")

metric_a, metric_b, metric_c, metric_d = st.columns(4)
metric_a.metric("Rentang data", f"{years[0]} - {years[-1]}")
metric_b.metric("Rata-rata periode", format_value(overall_mean))
metric_c.metric("Nilai minimum", format_value(minimum))
metric_d.metric("Nilai maksimum", format_value(maximum))

st.markdown("<div class='brand-rule'></div>", unsafe_allow_html=True)
st.subheader("Rata-rata suhu per tahun")
fig = go.Figure(
	go.Bar(
		x=[int(year) for year in annual_means.year.values],
		y=annual_means.values,
		marker_color="#2f7258",
		marker_line_width=0,
		hovertemplate="%{x}: %{y:.1f} °C<extra></extra>",
	)
)
fig.update_yaxes(title="Suhu (°C)")
fig.update_xaxes(title=None, dtick=1)
st.plotly_chart(chart_layout(fig, 320), use_container_width=True, config={"displayModeBar": False})

st.markdown(
	'<p class="brand-note">Sumber: file NetCDF di folder data. Logo BMKG dan UPI digunakan sebagai identitas sumber aplikasi.</p>',
	unsafe_allow_html=True,
)
