# 巨人每日任务

`giant_daily.py` 发送一次指定 POST 请求并输出 HTTP 状态和响应正文，不自动重试。
HTTP 成功仅表示请求已送达，业务是否成功需查看返回内容。

## 每天北京时间 08:00

将 `.github/workflows/giant-daily.yml` 提交到 GitHub 默认分支，并启用 Actions。
在仓库 Settings → Secrets and variables → Actions 中添加仓库 Secrets：

- `GIANT_TOKEN`：请求的 token。
- `GIANT_COOKIE`：完整 Cookie 请求头。

可选设置仓库 Variable `GIANT_USER_ID`，默认 `7626347`。
凭据不要写入源码、工作流或提交记录。凭据失效时更新 Secrets。
工作流也支持手动运行。GitHub 定时任务可能延迟，不保证精确到分钟；
公共仓库长期无活动时定时工作流可能被 GitHub 停用。
只有工作流在默认分支且凭据已配置后，定时任务才可用。

## 本地运行

安装 `python -m pip install -r requirements-giant.txt`，通过安全的环境配置提供
`GIANT_USER_ID`、`GIANT_TOKEN`、`GIANT_COOKIE`，然后运行 `python giant_daily.py`。
脚本无需启动其他仓库 JS 任务，也不会发送额外通知。
