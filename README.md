# 🖥️ NEO-OC // 监控矩阵

<div align="center">

![Cyber Dashboard](https://img.shields.io/badge/Status-Online-brightgreen?style=for-the-badge&logo=statuspal)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red?style=for-the-badge&logo=streamlit)
![Cloudflare](https://img.shields.io/badge/Cloudflare-Edge-orange?style=for-the-badge&logo=cloudflare)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

一个赛博朋克风格的实时网站监控与分析大屏，基于 **Streamlit** 构建，通过自建的 **Cloudflare Workers + D1** 数据管道，将你名下所有网站的访问量、用户画像、站点可用性集中展示在一块屏幕上。

> “数据永不离线，所有系统脉搏尽在掌握。”

---

## ✨ 功能亮点

- 🌐 **多站点统一监控**：支持 10+ 个独立网站（GitHub Pages、Vercel、Netlify、Cloudflare Pages 等）
- 📊 **实时数据展示**：今日 PV/UV、站点在线状态、平均响应时间
- 🗺️ **用户画像分析**：设备类型、浏览器、操作系统、国家热力地图
- 🔗 **流量来源追踪**：自动识别来源域名并映射为友好项目名称
- ⏱️ **每 60 秒自动刷新**：配合 Streamlit 自动刷新组件，保持数据最新
- 🎨 **赛博朋克视觉风格**：动态粒子背景、霓虹光效、Orbitron 字体、扫描线效果
- 🔊 **离线告警**：站点异常时红色闪烁动画 + 声音提示
- 🔐 **API 安全加固**：Token 认证防泄露，Worker 端 Referrer 白名单防滥用
- 🕒 **实时 UTC 时钟** + 当前在线人数 + CPU 温度模拟

---

## 🧱 技术架构
网站 → Tracker Worker → D1 数据库 → Monitor / API / Cleanup Workers → Streamlit 大屏



- **数据采集**：轻量 `<script>` 嵌入网站，透明 GIF 回传，不阻塞页面
- **数据存储**：Cloudflare D1（免费额度 5GB），SQLite 兼容
- **监控检查**：Cron Worker 每 5 分钟 HEAD 请求检测站点状态
- **API 服务**：Worker 提供 JSON 数据，Bearer Token 认证
- **可视化**：Streamlit + Plotly + 自定义 CSS 构建赛博朋克界面

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/cyber-dashboard.git
cd cyber-dashboard
```
2. 安装依赖
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. 配置 API Token
编辑 app.py，将 HEADERS 中的 Token 替换为你 Cloudflare API Worker 的真实 Token：

```python
HEADERS = {"Authorization": "Bearer 你的真实Token"}
```
Token 从 Cloudflare D1 项目中的 .dev.vars 获取，或通过 wrangler secret put 生成。

4. 启动本地大屏
```bash
streamlit run app.py
```
浏览器访问 http://localhost:8501 即可看到监控矩阵。

已为你将该段内容重新整理为规范的 Markdown 格式，直接替换即可：


## 🌍 部署到 Streamlit Cloud（推荐）

1. 将本项目推送至你的 GitHub 仓库
2. 登录 [Streamlit Cloud](https://share.streamlit.io)
3. 点击 **“New app”**，选择仓库、分支 `main`、主文件 `app.py`
4. 部署完成后获得公开 URL，例如 `https://你的用户名-cyber-dashboard.streamlit.app`

> 💡 如需保持大屏常驻在线，可使用 [UptimeRobot](https://uptimerobot.com/) 设置每 5 分钟一次的 HTTP 监控，防止应用休眠。

---

## 📝 自定义

### 添加新网站

1. 在 Cloudflare D1 中 `INSERT` 新站点
2. 在新网站中嵌入追踪脚本（`site_id` 需一致）
3. 在 `app.py` 的 `keywords` 列表中添加一行：
   ```python
   ('你的域名关键词', '显示名称'),
   ```
4. 推送更新，Streamlit Cloud 自动重新部署

### 调整刷新频率

修改 `app.py` 中的 `st_autorefresh(interval=60_000)`，单位毫秒。

### 关闭声音告警

注释或删除 `app.py` 中以下代码段：
```python
if offline_sites:
    st.components.v1.html(...)
```

---

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 数据采集 & API | Cloudflare Workers (JavaScript) |
| 数据库 | Cloudflare D1 (SQLite) |
| 定时任务 | Cloudflare Cron Triggers |
| 可视化大屏 | Streamlit + Plotly + Pandas |
| 风格特效 | 自定义 CSS + Canvas 粒子动画 |
| 部署平台 | Streamlit Community Cloud |

---

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源，欢迎自由使用和修改。

---

## ⭐ 支持

如果你觉得这个项目对你有帮助，请给一个 **Star** ⭐  
也欢迎在 Issues 中提出建议或报告问题。

<div align="center">
  <img src="https://ca9f093e.image-manage.pages.dev/file/AgACAgUAAyEGAATolNddAAMQaiqvlpYgxzl1BdY41Clhh7Or12cAAvwPaxtNjVlVK2G2VPn9asoBAAMCAAN3AAM7BA.png" width="800" />
  <p><em>“NEO-OC 监控矩阵”——你的数字资产神经中枢</em></p>
</div>


