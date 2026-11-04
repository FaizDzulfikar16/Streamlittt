from pathlib import Path

import streamlit as st
import xarray as xr


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
LOGO_BMKG = ROOT / "logo-bmkg.png"
LOGO_UPI = ROOT / "LogoUPI.png"


@st.cache_data(show_spinner="Memuat data NetCDF...")
def load_data():
    files = sorted(DATA_DIR.glob("*.nc"))
    if not files:
        raise FileNotFoundError(f"Tidak ada file NetCDF di {DATA_DIR}")

    arrays = []
    for path in files:
        with xr.open_dataset(path) as dataset:
            if not dataset.data_vars:
                continue

            variable = next(iter(dataset.data_vars))
            data = dataset[variable].load()
            time_name = next(
                (
                    name
                    for name in data.dims
                    if name in {"time", "valid_time", "date"}
                    or dataset[name].attrs.get("standard_name") == "time"
                ),
                None,
            )
            if time_name is None:
                raise ValueError(f"Koordinat waktu tidak ditemukan di {path.name}")
            if time_name != "time":
                data = data.rename({time_name: "time"})

            units = str(data.attrs.get("units", "")).strip().lower()
            if units in {"k", "kelvin"}:
                data = data - 273.15
                data.attrs.update(dataset[variable].attrs)
                data.attrs["units"] = "°C"

            arrays.append(data)

    if not arrays:
        raise ValueError("File NetCDF tidak berisi variabel data yang dapat dibaca.")

    return xr.concat(arrays, dim="time").sortby("time")


def format_value(value, units="°C"):
    return f"{float(value):.1f} {units}"


def year_values(data):
    return sorted({int(year) for year in data.time.dt.year.values})


def apply_page_header(section, title, description):
    st.markdown(f'<div class="eyebrow">{section}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="page-intro">{description}</p>', unsafe_allow_html=True)


def render_data_notice():
    st.markdown(
        '<div class="notice"><strong>Catatan data</strong><br>'
        "File NetCDF yang tersedia berisi suhu udara 2 meter (<code>t2m</code>) "
        "dalam Kelvin, bukan data curah hujan. Nilai pada aplikasi dikonversi "
        "ke °C. Untuk analisis curah hujan, diperlukan file dengan variabel "
        "presipitasi, misalnya <code>tp</code> atau <code>precipitation</code>.</div>",
        unsafe_allow_html=True,
    )


def chart_layout(fig, height=360):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Manrope, sans-serif", color="#1d2925", size=12),
        hoverlabel=dict(bgcolor="white", font_size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, linecolor="#dce4dc", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#edf1ec", linecolor="#dce4dc", zeroline=False)
    return fig