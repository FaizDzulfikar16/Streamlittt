import calendar

import plotly.graph_objects as go
import streamlit as st

from climate_data import apply_page_header, chart_layout, load_data, year_values


data = load_data()
years = year_values(data)

apply_page_header(
	"ANALISIS SPASIAL",
	"Peta suhu rata-rata",
	"Jelajahi sebaran suhu pada setiap titik grid. Pilih tahun dan periode untuk memperbarui peta.",
)

year_col, month_col = st.columns([1, 2])
with year_col:
	selected_year = st.selectbox("Tahun", years, index=len(years) - 1)
with month_col:
	month_options = ["Sepanjang tahun"] + [calendar.month_name[month] for month in range(1, 13)]
	selected_month = st.selectbox("Periode", month_options)

selection = data.where(data.time.dt.year == selected_year, drop=True)
if selected_month != "Sepanjang tahun":
	month_number = month_options.index(selected_month)
	selection = selection.where(selection.time.dt.month == month_number, drop=True)

spatial_mean = selection.mean(dim="time").sortby("latitude")
mean_value = float(spatial_mean.mean())
st.metric("Suhu rata-rata area", f"{mean_value:.1f} °C", help="Rata-rata seluruh titik grid dan hari pada periode terpilih.")

map_fig = go.Figure(
	go.Heatmap(
		x=spatial_mean.longitude.values,
		y=spatial_mean.latitude.values,
		z=spatial_mean.values,
		colorscale=[[0, "#d8e6bf"], [0.55, "#6eaa7e"], [1, "#c76a50"]],
		colorbar=dict(title="°C", thickness=14, outlinewidth=0),
		xgap=2,
		ygap=2,
		hovertemplate="Lon %{x:.2f}°<br>Lat %{y:.2f}°<br>%{z:.1f} °C<extra></extra>",
	)
)
map_fig.update_layout(yaxis=dict(autorange="reversed", title="Lintang"), xaxis=dict(title="Bujur", constrain="domain"))
st.plotly_chart(chart_layout(map_fig, 520), use_container_width=True, config={"displayModeBar": False})
st.caption("Setiap sel menunjukkan satu titik grid NetCDF. Resolusi data: 0,25° (24 titik).")
