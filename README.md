# Yuanne 💬

AI 聊天陪伴 App，Flask 后端 + PWA 前端，手机添加到主屏幕即可像原生 App 一样使用。

## 功能

- 🤖 **多角色 AI 聊天** — 创建不同人设的 AI 对话伙伴
- 🔔 **实时通知** — SSE 推送，AI 主动发消息提醒
- 📱 **朋友圈** — AI 角色自动发动态、互评
- 📲 **PWA 手机 App** — 添加到主屏幕，全屏无浏览器边框

## 本地运行

```bash
# 设置 DeepSeek API Key（仅需一次）
# Windows PowerShell:
$env:DEEPSEEK_API_KEY="sk-你的密钥"
# macOS / Linux:
export DEEPSEEK_API_KEY="sk-你的密钥"

# 安装依赖
pip install -r requirements.txt

# 启动
python server.py
# 浏览器打开 http://localhost:5099
```

## 技术栈

| 层 | 技术 |
|---|------|
| 后端 | Flask + DeepSeek API (OpenAI SDK) |
| 前端 | 原生 HTML/CSS/JS，单文件 SPA |
| 实时通信 | Server-Sent Events (SSE) |
| PWA | Manifest + Service Worker |
| 部署 | Render / 任意支持 Flask 的平台 |

## 项目结构

```
├── server.py              # Flask 后端，API + SSE
├── templates/
│   └── index.html         # 完整前端（HTML+CSS+JS）
├── static/                # PWA 资源
│   ├── manifest.json      # PWA 配置
│   ├── sw.js              # Service Worker
│   ├── icon-192.png       # App 图标
│   └── icon-512.png       # App 图标
├── requirements.txt       # Python 依赖
├── Procfile               # 云部署启动命令
└── data.json              # 对话数据（不入库）
```

## 部署

1. Fork 本仓库
2. 在 [Render](https://render.com) 新建 Web Service，连接仓库
3. 设置环境变量 `DEEPSEEK_API_KEY` 为你的 API 密钥
4. 部署完成后，手机浏览器打开 URL → 添加到主屏幕

## License

MIT
