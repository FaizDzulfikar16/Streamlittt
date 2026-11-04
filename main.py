import streamlit as st

st.set_page_config(
	page_title="Iklim Harian | BMKG x UPI",
	page_icon="🌦️",
	layout="wide",
	initial_sidebar_state="expanded",
)

st.markdown(
	"""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

	:root {
		--ink: #1d2925;
		--muted: #64736d;
		--paper: #f5f7f3;
		--line: #dce4dc;
		--green: #2f7258;
		--lime: #d8e6bf;
		--coral: #c76a50;
	}
	html, body, [class*="css"] { font-family: 'Manrope', sans-serif; color: var(--ink); }
	[data-testid="stAppViewContainer"] { background: var(--paper); }
	[data-testid="stHeader"] { background: transparent; }
	[data-testid="stSidebar"] { background: #edf2eb; border-right: 1px solid var(--line); }
	[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--muted); }
	[data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3 { color: var(--ink) !important; letter-spacing: 0; }
	h1 { font-size: 2rem !important; font-weight: 700 !important; }
	h2 { font-size: 1.35rem !important; font-weight: 700 !important; }
	.eyebrow { color: var(--green); font: 500 0.72rem 'DM Mono', monospace; text-transform: uppercase; letter-spacing: 0.08em; }
	.page-intro { color: var(--muted); max-width: 760px; margin-top: -0.5rem; }
	.notice { border-left: 4px solid var(--coral); background: #fff3ec; padding: 0.85rem 1rem; color: #553b31; border-radius: 0 4px 4px 0; }
	.metric-label { color: var(--muted); font: 500 0.72rem 'DM Mono', monospace; text-transform: uppercase; }
	div[data-testid="stMetric"] { background: #fff; border: 1px solid var(--line); border-radius: 4px; padding: 0.85rem 1rem; }
	div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] *,
	[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p { color: var(--muted) !important; font-size: 0.78rem; }
	div[data-testid="stMetricValue"] { color: var(--ink); font-weight: 700; }
	div[data-testid="stPlotlyChart"] { background: #fff; border: 1px solid var(--line); border-radius: 4px; padding: 0.25rem; }
	.brand-rule { border-top: 1px solid var(--line); margin: 1.25rem 0; }
	.brand-note { color: var(--muted); font-size: 0.82rem; }
	</style>
	""",
	unsafe_allow_html=True,
)

pages = {
	"Eksplorasi": [
		st.Page("pages/Beranda.py", title="Beranda", icon=":material/home:", default=True),
		st.Page("pages/Grafik.py", title="Grafik", icon=":material/show_chart:"),
		st.Page("pages/Peta.py", title="Peta", icon=":material/map:"),
	]
}

st.navigation(pages).run()
