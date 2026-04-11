---
title: "📔 2026 年日记"
created: 2026-01-01
tags: [日记, 索引]
---

# 📔 日记指南

> 记录每一天，追踪成长与变化

---

## 📝 日记写什么

日记不是流水账，而是对一天的**有意识提炼**。建议围绕以下几个维度记录：

### 事实层（发生了什么）
- 今天做了哪些重要的事？
- 遇到了什么人、什么情况？

### 感受层（我的反应）
- 什么事让我有强烈的情绪反应？为什么？
- 今天的能量状态如何？

### 思考层（我学到了什么）
- 今天有什么新的认识或想法？
- 如果重来，我会做什么不同的选择？

### 行动层（明天怎么做）
- 有什么未完成的事需要跟进？
- 明天最重要的一件事是什么？

> [!tip] 写作建议
> 不求长篇大论，5 分钟也能写出有价值的日记。重要的是**持续记录**，而不是每篇都完美。

---

## 📊 今年日记统计

### 按月分布

```dataview
TABLE length(rows) AS "篇数", min(file.name) AS "最早", max(file.name) AS "最近"
FROM ""
WHERE contains(file.folder, this.file.folder) AND file.name != "README"
GROUP BY substring(file.name, 5, 2) AS "月份"
SORT substring(file.name, 5, 2) ASC
```

### 所有日记

```dataview
TABLE day AS "星期", week AS "周次"
FROM ""
WHERE contains(file.folder, this.file.folder) AND file.name != "README"
SORT file.name DESC
```

---

[[20-日志/20-日志-README|← 返回日志首页]]
