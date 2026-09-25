---
title: "🏠 Life Knowledge System"
created: 2026-01-22
type: "machine-index"
tags: [系统, 主页]
---

# 🏠 Life Knowledge System

> 你的个人知识管理中枢 - 记录生活，沉淀智慧，持续成长

---

## 🚀 快速入口

### 📅 今日视图
```dataviewjs
const today = moment();
const dailyNote = `20-日志/日记/${today.format("YYYY")}/${today.format("MM")}/${today.format("YYYY-MM-DD")}`;
const weeklyNote = `20-日志/周记/${today.format("YYYY")}-W${today.format("WW")}`;
const monthlyNote = `20-日志/月记/${today.format("YYYY-MM")}`;

dv.paragraph(
  `- [[${dailyNote}|今天的日记]]\n` +
  `- [[${weeklyNote}|本周回顾]]\n` +
  `- [[${monthlyNote}|本月复盘]]`
);
```

### 📝 核心功能
- [[01-收件箱/01-收件箱-README|📥 收件箱]] - 快速记录
- [[02-项目/02-项目-README|🎯 项目管理]] - 执行中的项目
- [[03-领域-README|🌟 领域总览]] - 人生各领域
- [[10-卡片盒-README|🗂️ 卡片盒]] - 永久笔记
- [[30-输出/30-输出-README|✍️ 创作输出]] - 文章与分享

### 🗺️ 系统导航
- [[00-系统/🗺️ 知识地图.canvas|🗺️ 知识地图]] - 可视化导航
- [[00-系统/📖 使用手册|📖 使用手册]] - 系统指南

---

## 📊 数据看板

### 🎯 进行中的项目

```dataview
TABLE default(project_status, status) as "项目状态", priority as "优先级", start_date as "开始日期", due_date as "截止日期"
FROM "02-项目"
WHERE project_status = "active" OR (!project_status AND contains(["🚧 进行中", "进行中"], status))
SORT priority DESC, start_date DESC
LIMIT 5
```

未标注项目进度的笔记不会列入本表；进入项目笔记确认后补充 `project_status`。`status: draft/stable` 只表示文档成熟度。

### ⏰ 待办事项

```dataview
TASK
FROM "02-项目" OR "03-领域"
WHERE !completed AND contains(file.etags, "#todo")
LIMIT 10
```

只有在笔记 frontmatter 的 `tags` 中明确加入 `todo` 的文件才纳入首页待办；普通习惯和未标注的清单不在这里汇总。

### 📚 最近笔记

```dataview
TABLE file.mtime as "更新时间"
FROM ""
WHERE file.name != "🏠 HOME"
SORT file.mtime DESC
LIMIT 8
```

---

## 🌟 本周聚焦

### 本周目标（请替换为本周目标）
- [x] 目标 1
- [x] 目标 2
- [x] 目标 3

### 本周重要项目
- 项目 1
- 项目 2

### 本周学习主题
- 学习主题

---

## 📖 阅读中的书

```dataview
TABLE author as "作者", default(reading_status, status) as "阅读进度", rating as "评分"
FROM "03-领域/读书写作/读书笔记"
WHERE reading_status = "reading" OR (!reading_status AND contains(["阅读中", "正在阅读"], status))
SORT file.mtime DESC
```

---

## 💡 最近思考

### 灵感闪念

```dataview
LIST
FROM "01-收件箱/灵感闪念"
SORT file.mtime DESC
LIMIT 5
```

### 卡片盒新增

```dataview
TABLE type as "类型", created as "创建时间"
FROM "10-卡片盒"
SORT created DESC
LIMIT 5
```

---

## 📈 系统统计

### 笔记数量统计

```dataview
TABLE length(rows) as "数量"
FROM ""
GROUP BY file.folder
SORT length(rows) DESC
```

---

## 🔧 快速操作

### 创建新笔记
- 📝 [[daily-note-template|新建日记]]
- 📚 [[00-系统/templates/reading-note-template|新建读书笔记]]
- 🎯 [[00-系统/templates/project-note-template|新建项目]]
- 💡 [[00-系统/templates/zettelkasten-template|新建卡片盒笔记]]
- 📋 [[00-系统/templates/meeting-note-template|新建会议记录]]

### 定期回顾
- 📅 [[00-系统/templates/weekly-review-template|周回顾模板]]
- 📅 [[00-系统/templates/monthly-review-template|月复盘模板]]

---

## 🎨 领域一览

```dataview
TABLE WITHOUT ID file.link as "领域", choice(contains(["healthy", "🟢 健康", "🟢"], health), "🟢 健康", choice(contains(["attention", "🟡 需关注", "🟡"], health), "🟡 需关注", choice(contains(["at_risk", "🔴 有风险", "🔴"], health), "🔴 有风险", "待评估"))) as "已记录健康度", default(last_review, "未记录") as "评估日期"
FROM "03-领域"
WHERE file.name = "README" AND length(split(file.folder, "/")) = 2
SORT file.folder ASC
```

健康度只显示领域入口中明确记录的 `health`（`healthy` / `attention` / `at_risk`），并附评估日期；没有评估记录时显示「待评估」。文档成熟度和最近编辑时间不能代替健康评估。

---

## 📌 常用链接

### 外部工具
- [滴答清单](https://dida365.com)
- [微信读书](https://weread.qq.com)
- [豆瓣](https://book.douban.com)

---

## 💬 使用提示

> **工作流提醒**:
> 1. 每天早上查看本页，设定今日目标
> 2. 随时记录到收件箱
> 3. 每晚花15分钟整理收件箱
> 4. 每周五进行周回顾
> 5. 每月底进行月复盘

> **新手引导**:
> - 第一次使用？阅读 [[00-系统/📖 使用手册|📖 使用手册]]
> - 查看 [[00-系统/🗺️ 知识地图.canvas|🗺️ 知识地图]] 了解系统结构
> - 从创建今天的日记开始你的知识管理之旅

---

**最后更新**: `= dateformat(this.file.mtime, "yyyy-MM-dd")`
**系统版本**: v1.0
