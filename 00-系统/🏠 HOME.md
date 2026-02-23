---
title: "🏠 Life Knowledge System"
created: 2026-01-22
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
TABLE status as "状态", priority as "优先级", start_date as "开始日期"
FROM "02-项目"
WHERE status = "🚧 进行中"
SORT priority DESC, start_date DESC
LIMIT 5
```

### ⏰ 待办事项

```dataview
TASK
FROM "02-项目" OR "03-领域"
WHERE !completed
LIMIT 10
```

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
- [ ] 目标 1
- [ ] 目标 2
- [ ] 目标 3

### 本周重要项目
- 项目 1
- 项目 2

### 本周学习主题
- 学习主题

---

## 📖 阅读中的书

```dataview
TABLE author as "作者", status as "状态", rating as "评分"
FROM "04-资源/阅读笔记"
WHERE status = "阅读中"
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
GROUP BY folder
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

| 领域 | 健康度 | 最近更新 |
|------|--------|----------|
| [[03-领域/职业发展/README\|💼 职业发展]] | 🟢 | 待更新 |
| [[03-领域/技术领导力/README\|🚀 技术领导力]] | 🟢 | 2026-02-08 |
| [[03-领域/软件工程/README\|🏗️ 软件工程]] | 🟢 | 2026-02-08 |
| [[03-领域/健康管理/README\|🏃 健康管理]] | 🟡 | 待更新 |
| [[03-领域/财务规划/README\|💰 财务规划]] | 🟢 | 待更新 |
| [[03-领域/人际关系/README\|👥 人际关系]] | 🟢 | 待更新 |
| [[03-领域/兴趣爱好/README\|🎨 兴趣爱好]] | 🟢 | 待更新 |

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

**最后更新**: 2026-01-22
**系统版本**: v1.0
