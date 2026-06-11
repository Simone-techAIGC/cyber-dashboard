import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import pycountry
import random

# ========== 页面设置 ==========
st.set_page_config(layout="wide", page_title="CYBER OPS CENTER", page_icon="🖥️")
st_autorefresh(interval=60_000, key="cyber_refresh")

# ========== 自定义赛博朋克 CSS ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    .main, .stApp {
        background: radial-gradient(circle at center, #0a0a0a 0%, #000000 100%);
        color: #00ffcc;
        font-family: 'Orbitron', 'Courier New', monospace;
    }

    .main::before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: repeating-linear-gradient(0deg,
            rgba(0, 255, 0, 0.03) 0px,
            rgba(0, 0, 0, 0.1) 2px,
            transparent 3px);
        pointer-events: none; z-index: 1000;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3em;
        text-shadow: 0 0 10px #0ff, 0 0 20px #0ff, 0 0 40px #0ff;
        color: #0ff;
        text-align: center;
        letter-spacing: 5px;
        margin-bottom: 0;
        animation: glow 1.5s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #0ff, 0 0 20px #0ff, 0 0 40px #0ff; }
        to { text-shadow: 0 0 20px #0ff, 0 0 40px #0ff, 0 0 80px #0ff; }
    }
    .cyber-subtitle {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2em;
        color: #ff00ff;
        text-shadow: 0 0 5px #f0f;
        text-align: center;
    }

    .card {
        background: rgba(0, 20, 20, 0.7);
        border: 1px solid #0ff;
        box-shadow: 0 0 15px #0ff;
        padding: 10px;
        border-radius: 8px;
        backdrop-filter: blur(5px);
    }

    .status-online {
        color: #00ff00;
        text-shadow: 0 0 10px #0f0;
        font-weight: bold;
    }
    .status-offline {
        color: #ff0040;
        text-shadow: 0 0 10px #f00;
        font-weight: bold;
        animation: blink 1s infinite;
    }
    @keyframes blink {
        50% { opacity: 0; }
    }

    .clock {
        font-family: 'Orbitron', monospace;
        font-size: 4em;
        color: #0ff;
        text-shadow: 0 0 20px #0ff;
        text-align: center;
    }

    .log-table {
        max-height: 200px;
        overflow-y: scroll;
        background: rgba(0, 15, 15, 0.8);
        border: 1px solid #0ff;
        padding: 5px;
        font-size: 0.8em;
    }

    canvas#particles {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -1;
        pointer-events: none;
    }

div[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    color: #ffffff !important;
}
div[data-testid="stMetricLabel"] {
    font-family: 'Orbitron', monospace !important;
    color: #cccccc !important;
}
</style>
""", unsafe_allow_html=True)

# ========== 动态粒子背景 ==========
st.components.v1.html("""
<canvas id="particles"></canvas>
<script>
const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const particles = [];
for(let i=0; i<80; i++) {
    particles.push({
        x: Math.random()*canvas.width,
        y: Math.random()*canvas.height,
        vx: (Math.random()-0.5)*1.5,
        vy: (Math.random()-0.5)*1.5,
        size: Math.random()*2+1
    });
}
function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = '#00ffcc';
    particles.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
        ctx.fill();
        p.x += p.vx;
        p.y += p.vy;
        if(p.x<0||p.x>canvas.width) p.vx *= -1;
        if(p.y<0||p.y>canvas.height) p.vy *= -1;
    });
    requestAnimationFrame(draw);
}
draw();
window.onresize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
};
</script>
""", height=0)

# ========== API 配置 ==========
API_URL = "https://analytics-api.daifayo7.workers.dev/api/stats"
HEADERS = {"Authorization": f"Bearer {st.secrets['API_TOKEN']}"}  # ⚠️ 替换为你的 Token

@st.cache_data(ttl=50)
def fetch_data():
    try:
        resp = requests.get(API_URL, headers=HEADERS, timeout=10)
        return resp.json()
    except:
        return None

data = fetch_data()

# ========== 模拟数据生成 ==========
simulated_online = random.randint(1, 15)          # 当前在线人数 (1-15)
simulated_cpu_temp = round(random.uniform(35, 75), 1)   # CPU 温度 (°C)

# ========== 顶部标题 + 实时时钟 ==========
col_logo, col_clock = st.columns([3, 2])
with col_logo:
    st.markdown('<div class="cyber-title">NEO-OC // 监控矩阵</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-subtitle">● 所有系统数据流已同步 ●</div>', unsafe_allow_html=True)
with col_clock:
    st.components.v1.html("""
    <div class="clock" id="liveClock"></div>
    <script>
    function updateClock() {
        const now = new Date();
        document.getElementById('liveClock').innerText =
            now.toISOString().replace('T', ' ').slice(0, 19) + ' UTC';
    }
    updateClock();
    setInterval(updateClock, 1000);
    </script>
    """, height=100)

st.markdown("---")

if data is None:
    st.error("⚠️ 无法连接到数据中枢... 系统离线")
    st.stop()

# ========== 核心指标（6列布局） ==========
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("今日 PV", data['pv'])
col2.metric("今日 UV", data['uv'])
online_count = sum(1 for m in data['monitor'] if m['status_code'] == 200)
col3.metric("在线站点", f"{online_count}/{len(data['monitor'])}")
avg_resp = sum(m['response_time'] for m in data['monitor'] if m['response_time']) / max(len(data['monitor']), 1)
col4.metric("平均响应", f"{avg_resp:.0f} ms")
col5.metric("当前在线", simulated_online)          # 模拟在线人数
col6.metric("CPU 温度", f"{simulated_cpu_temp} °C") # 模拟 CPU 温度

# ========== 站点监控面板 ==========
st.markdown("### █ 网络节点状态")
if data['monitor']:
    monitor_cols = st.columns(len(data['monitor']))
    for i, m in enumerate(data['monitor']):
        with monitor_cols[i]:
            online = m['status_code'] == 200
            status_class = "status-online" if online else "status-offline"
            status_text = "在线" if online else f"离线 ({m.get('error','?')})"
            st.markdown(f"""
            <div class="card">
                <strong>{m['name']}</strong><br>
                <span class="{status_class}">{status_text}</span><br>
                响应: {m['response_time']}ms<br>
                检查: {m['checked_at'][:16]}
            </div>
            """, unsafe_allow_html=True)

    # 离线声音告警
    offline_sites = [m for m in data['monitor'] if m['status_code'] != 200]
    if offline_sites:
        st.components.v1.html("""
        <script>
            var audio = new Audio('data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAAABmYWN0BAAAAA==');
            audio.play();
        </script>
        """, height=0)

st.markdown("---")

# ========== 图表区域 ==========
col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    st.subheader("📈 站点访问量分布")
    if data['sitePv']:
        df_site = pd.DataFrame(data['sitePv'])
        fig = px.bar(df_site, x='site_id', y='pv', color='site_id',
                     color_discrete_sequence=px.colors.sequential.Plasma_r)
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    st.subheader("🔗 流量来源 TOP10")
    if data['referrers']:
        df_ref = pd.DataFrame(data['referrers'])
        # ====== 友好名称映射 ======
        def map_referrer(r):
            # 关键词模糊匹配
            keywords = [
                ('starlit-kangaroo', '个人作品集网站'),
                ('simone.ccwu.cc', '个人博客'),
                ('cyber-portfolio', '3D赛博朋克作品集'),
                ('printforge', '3D打印企业官网'),
                ('LUNARIS', '电商独立站'),
                ('nav-simone', '个人导航站'),
                ('stock-app', '库存管理系统(Web)'),
                ('android-stock-app', '库存管理系统(安卓)'),
                ('image-manage', '图床'),
                ('furniro', '家居品牌网站'),   # 包含所有 furniro 变体
            ]
            if r == 'direct':
                return '直接访问'
            for kw, name in keywords:
                if kw in r:
                    return name
            # 其它来源只显示主域名
            try:
                from urllib.parse import urlparse
                return urlparse(r).netloc or r
            except:
                return r
        df_ref['referrer'] = df_ref['referrer'].apply(map_referrer)
        # ====== 绘制饼图 ======
        fig = px.pie(df_ref, names='referrer', values='count', hole=0.4,
                     color_discrete_sequence=["#00ffff", "#00cccc", "#009999", "#006666", "#003333"])
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# 用户画像
col_dev1, col_dev2, col_dev3 = st.columns(3)
with col_dev1:
    st.subheader("🖥️ 设备类型")
    if data['devices']:
        df_dev = pd.DataFrame(data['devices'])
        fig = px.bar(df_dev, x='device_type', y='count', color='device_type',
                     color_discrete_sequence=['#ff00ff','#00ffff','#ffff00'])
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with col_dev2:
    st.subheader("🌐 浏览器")
    if data['browsers']:
        df_browser = pd.DataFrame(data['browsers'])
        fig = px.pie(df_browser, names='browser', values='count', hole=0.3,
                     color_discrete_sequence=px.colors.qualitative.Prism)
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

with col_dev3:
    st.subheader("💻 操作系统")
    if data['oses']:
        df_os = pd.DataFrame(data['oses'])
        fig = px.pie(df_os, names='os', values='count', hole=0.3,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# 世界地图
st.subheader("🌍 访问者地理位置")
if data['countries']:
    df_country = pd.DataFrame(data['countries'])
    def get_iso3(country_code):
        try:
            return pycountry.countries.get(alpha_2=country_code).alpha_3
        except:
            return None
    df_country['iso3'] = df_country['country'].apply(get_iso3)
    df_country = df_country.dropna(subset=['iso3'])
    if not df_country.empty:
        fig = px.choropleth(df_country, locations='iso3', color='count',
                            color_continuous_scale='plasma',
                            labels={'count':'访问量'})
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                          geo=dict(bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig, use_container_width=True)

# 最近访问日志
st.markdown("### 📟 最近访问日志")
if data['recent']:
    df_log = pd.DataFrame(data['recent'])
    st.markdown('<div class="log-table">', unsafe_allow_html=True)
    st.dataframe(df_log.style.map(lambda _: 'color: #00ffcc; background-color: #001a1a'), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#ff00ff;'>/// 系统运行于边缘网络 /// 数据永不离线 ///</p>", unsafe_allow_html=True)
