<%*
// 只对 YYYY-MM-DD 格式的文件名应用此模板
if (!tp.file.title.match(/^\d{4}-\d{2}-\d{2}$/)) {
  return;
}
const date = tp.file.title;
const yyyy = moment(date).format("YYYY");
const mm = moment(date).format("MM");
const targetPath = `20-日志/日记/${yyyy}/${mm}/${date}`;
if (tp.file.path(true) !== targetPath + ".md") {
  await tp.file.move(targetPath);
}
-%>
---
date: <% date %>
day: <% moment(date).format("dddd") %>
week: <% moment(date).format("YYYY-[W]WW") %>
tags: [日记]
---


# <% date %> <% moment(date).format("dddd") %>

## 📋 今日目标

- [ ] 目标1
- [ ] 目标2
- [ ] 目标3

## 💼 工作日志

### ✅ 已完成


### 🚧 进行中


### ❓ 遇到的问题


## 💡 灵感思考


## 🔗 相关笔记

-

## 📊 今日数据

| 项目 | 数值 |
|------|------|
| 工作时长 | h |
| 专注度 | /10 |
| 能量值 | /10 |

## ✨ 今日亮点


---

<%*
const prevDate = moment(date).subtract(1, "days");
const nextDate = moment(date).add(1, "days");
const prevStr = prevDate.format("YYYY-MM-DD");
const nextStr = nextDate.format("YYYY-MM-DD");
const prevPath = `20-日志/日记/${prevDate.format("YYYY")}/${prevDate.format("MM")}/${prevStr}`;
const nextPath = `20-日志/日记/${nextDate.format("YYYY")}/${nextDate.format("MM")}/${nextStr}`;
tR += `⬅️ [[${prevPath}|${prevStr}]] | [[20-日志/日记/${yyyy}/README|返回日记目录]] | [[${nextPath}|${nextStr}]] ➡️`;
%>
