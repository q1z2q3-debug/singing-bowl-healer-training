# 安全政策

## 密钥管理红线

本仓库为公开开源项目，**严禁**将以下内容提交进仓库：

- API 密钥 / Token（PyPI、GitHub、Zenodo 等任何平台的访问令牌）
- 账号密码、邮箱密码
- `.env`、`pypi.txt` 等任何含凭据的本地文件

以上内容已在 `.gitignore` 中排除。提交前请自查：

```bash
git diff --staged | grep -iE "token|password|secret|ghp_|sk-|pypi-"
```

如发现密钥泄露，请立即在对应平台**吊销（revoke）并轮换**密钥，Git 历史中删除并不能使密钥失效。

## 报告漏洞

如发现本仓库存在安全问题，请勿公开提交 Issue，请联系仓库维护者。
