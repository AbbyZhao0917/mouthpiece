# 📣 嘴替 · Zuiti

> I 人的 AI 嘴替助手 —— 帮你把每一句话都说到位

[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Powered by Claude](https://img.shields.io/badge/Powered%20by-Claude%20Sonnet%204.6-purple.svg)](https://anthropic.com)

---

## 是什么

**嘴替**是一款基于 Claude AI 的中文文字润色工具，专为不擅长"把话说漂亮"的人设计。

输入你想表达的大概意思，选好场景和风格，AI 帮你输出一版说得体、说得准、说得好的文字。

**适合场景**：写公文、发微信消息、写发言稿、写工作总结、发小红书、写邀请函……共 22 种场景。

---

## 功能特点

- 🎯 **22 种使用场景** — 公文红头 / 工作报告 / 微信消息 / 发言稿 / PPT文案 / 发小红书 / 给长辈消息 / 生日祝福……
- ✍️ **12 种处理方式** — 整体润色 / 精简缩写 / 扩充内容 / 书面化 / 专业化 / 去AI味 / 中英互译 / 标准化语音……
- 🎨 **15 种语气风格** — 商务正式 / 温暖亲切 / 俏皮可爱 / 严谨专业 / 言辞激烈 / 疯感 / 幽默调侃 / 引经据典……
- 👥 **10 种发送对象** — 政府人员 / 上级领导 / 会员单位 / 同事 / 长辈 / 朋友……
- 📎 **文件上传** — 支持 Word / PDF / TXT，AI 直接读取内容处理
- 🎤 **语音输入** — PC 端支持（Chrome / Edge）
- 🔍 **原文对比** — 字符级 diff，红色标注删改，绿色标注新增
- 📋 **会话历史** — 侧边栏记录本次所有处理结果，可随时调取
- 📱 **手机 + PC 双端** — 响应式设计，手机浏览器直接访问

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python · FastAPI · Uvicorn |
| AI | Anthropic Claude Sonnet 4.6 |
| 前端 | 原生 HTML / CSS / JS（无框架依赖） |
| 部署 | Render（免费层可用） |
| 文件解析 | pypdf · python-docx |

---

## 快速部署（Render 免费）

### 前提

需要一个 [Anthropic API Key](https://console.anthropic.com/)（注册后在 API Keys 页面创建）。

### 步骤

**1. Fork 本仓库**

点击右上角 `Fork` 按钮，复制到你自己的 GitHub 账号。

**2. 注册 Render 并连接 GitHub**

前往 [render.com](https://render.com)，用 GitHub 账号登录，点击 `New +` → `Web Service`，选择你 Fork 的仓库。

**3. 填写配置**

| 字段 | 填写内容 |
|------|---------|
| Language | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Instance Type | Free |

**4. 添加环境变量**

在 `Environment Variables` 中添加：

```
ANTHROPIC_API_KEY = sk-ant-你的key
```

**5. 点击 Deploy**

等待 3–5 分钟，部署完成后 Render 会给你一个 `https://你的项目名.onrender.com` 的地址，手机 PC 均可访问。

> ⚠️ Render 免费版在 15 分钟无人访问后会进入休眠，首次访问需等待约 30–60 秒唤醒，之后正常。

---

## 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/mouthpiece.git
cd mouthpiece

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key
cp .env.example .env
# 编辑 .env，填入你的 ANTHROPIC_API_KEY

# 4. 启动
python main.py

# 浏览器打开 http://localhost:8513
```

---

## 费用说明

本项目调用 Anthropic Claude API，**每次润色请求约消耗 $0.01–0.04**（几分钱人民币）。

费用由**你自己的 API Key** 承担，与本仓库作者无关。

建议在 [Anthropic 控制台](https://console.anthropic.com/settings/limits)设置月度消费上限，避免超预期支出。

---

## 目录结构

```
ccfa-polish/
├── main.py          # FastAPI 后端，场景/风格定义，Claude API 调用
├── index.html       # 完整前端（单文件，含所有 CSS / JS）
├── requirements.txt # Python 依赖
├── .env.example     # 环境变量模板
├── .gitignore       # 已排除 .env，不会泄露 Key
└── LICENSE          # MIT License
```

---

## 自定义

想改成自己的业务场景？编辑 `main.py` 顶部的字典即可：

- `SCENES` — 使用场景及对应的 AI 提示语
- `STYLES` — 处理方式
- `TONES` — 语气风格

前端场景标签在 `index.html` 的 `sceneGrid` 区域修改。

---

## 版本历史

| 版本 | 主要变化 |
|------|---------|
| v0.9 | 清新果冻风设计，侧边栏历史，22个场景，15种语气风格 |
| v0.8 | 布局重构，字符级 diff 对比，新增场景/风格 |
| v0.7 | 浅蓝主题，历史记录，发送对象，语音修复 |
| v0.6 | 深色科技主题 |
| v0.5 | 语气风格，原文对比，手机语音 |
| v0.4 | 语音输入（PC端），去AI味风格 |
| v0.3 | 文件上传，流式输出 |
| v0.2 | 场景 / 处理方式 / 发送对象 |
| v0.1 | 基础润色功能上线 |

---

## License

[MIT](LICENSE) © 2026 [AbbyZhao0917](https://github.com/AbbyZhao0917/mouthpiece)

---

*由 Claude Sonnet 4.6 驱动 · 用 Claude Code 开发*
