---
title: "🎯 项目管理"
type: "README"
slot:
  accepts: ["Project Note"]
  lifecycle: active
  owner:
tags: [系统, 索引]
---

# 🎯 项目管理

> Projects - 有明确目标和截止日期的任务

---

## 📂 子文件夹

- [[工作项目/README|工作项目]] - 职场相关项目
- [[个人项目/README|个人项目]] - 个人目标项目
- [[学习项目/README|学习项目]] - 系统学习计划

---

## 📊 进行中的项目

```dataview
TABLE default(project_status, status) as "项目状态", priority as "优先级", start_date as "开始日期", due_date as "截止日期"
FROM "02-项目"
WHERE project_status = "active" OR (!project_status AND contains(["🚧 进行中", "进行中"], status))
SORT priority DESC, start_date DESC
```

看板只收录明确标注项目进度的笔记；列表为空不表示没有项目。`status: draft/stable` 不用于判断执行进度。

---

## ⏰ 待开始的项目

```dataview
TABLE priority as "优先级", start_date as "计划开始"
FROM "02-项目"
WHERE project_status = "planned" OR (!project_status AND contains(["⏳ 待开始", "🎯 计划中", "待开始", "计划中", "规划中"], status))
SORT priority DESC
```

---

## ✅ 最近完成的项目

```dataview
TABLE default(project_status, status) as "项目状态", end_date as "完成日期"
FROM "02-项目" OR "05-归档"
WHERE type = "Project Note" AND (project_status = "completed" OR (!project_status AND contains(["✅ 已完成", "已完成"], status)))
SORT end_date DESC
LIMIT 10
```

---

## 💡 使用指南

### 什么是项目？

项目必须同时满足:
- ✅ 有明确的目标和成果
- ✅ 有截止日期
- ✅ 需要多个步骤完成

### 项目 vs 领域

| 维度 | 项目 | 领域 |
|------|------|------|
| 时间 | 有截止日期 | 持续进行 |
| 目标 | 明确的成果 | 维持标准 |
| 完成 | 可以完成 | 无法完成 |
| 示例 | "完成XX课程" | "持续学习" |
| 示例 | "开发XX功能" | "技术能力" |

### 创建新项目

使用 [[00-系统/templates/work-project-template|项目模板]] 创建新项目笔记。

关键要素:
- 项目目标
- 时间规划
- 任务清单
- 相关人员
- 进度跟踪

### 项目状态

`status` 保留为文档成熟度（`draft/stable/deprecated`）；执行进度单独填写 `project_status`：

- `planned`：⏳ **待开始** - 已计划但未启动
- `active`：🚧 **进行中** - 正在执行
- `paused`：⏸️ **已暂停** - 临时暂停
- `completed`：✅ **已完成** - 达成目标
- `cancelled`：❌ **已取消** - 不再执行

用 `area` 填写关联领域名称（如 `职业发展`），用 `due_date` 记录截止日期、`end_date` 记录实际完成日期。旧的中文项目状态在未填写 `project_status` 时暂时兼容，详见 [[00-系统/Frontmatter 规范|Frontmatter 规范]]。

### 项目完成后

1. 在项目笔记中完成复盘
2. 提炼经验到 [[10-卡片盒-README|卡片盒]]
3. 移动到 [[05-归档/05-归档-README|归档]]
4. 更新相关 [[03-领域-README|领域]] 笔记

---

## 🔧 快速操作

- [[00-系统/templates/work-project-template|新建项目]]
- [[03-领域-README|查看领域]]
- [[00-系统/🏠 HOME|返回主页]]

---

*最后更新：`= dateformat(this.file.mtime, "yyyy-MM-dd")`*
