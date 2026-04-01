# hplc-club

HPLC 技术交流社区。

## 项目地址与在线站点

- GitHub: https://github.com/Tangrenbin/hplc-club
- Gitee: https://gitee.com/tangrenbin/hplc-club
- 主站地址: https://hplc-club.990124.xyz/
- Vercel 地址: https://hplc-club.vercel.app/

这个仓库已经配置为使用 MkDocs 将 `md_doc/` 目录中的 Markdown 文件构建成静态网页，并通过 GitHub Actions 自动发布到 Vercel。

## 文档站本地预览

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-docs.txt
mkdocs serve
```

默认访问地址：`http://127.0.0.1:8000`

如果本机没有安装 `python3-venv`，也可以直接用用户级安装临时预览：

```bash
python3 -m pip install --user -r requirements-docs.txt
python3 -m mkdocs serve
```

## 自动部署到 Vercel

工作流文件：`.github/workflows/deploy-docs-vercel.yml`

触发条件：

- 推送到 `main` 或 `master`
- 且变更包含 `md_doc/**`、`mkdocs.yml`、`requirements-docs.txt`、`vercel.json` 或工作流文件本身
- 也支持手动触发 `workflow_dispatch`

### 需要提前配置

1. 先在 Vercel 中准备一个项目。推荐用本地 `vercel link` 直接创建或关联项目，而不是开启 Vercel 自己的 Git 自动部署。
2. 在 GitHub 仓库的 `Settings -> Secrets and variables -> Actions` 中配置：

- Repository Secret: `VERCEL_TOKEN`
- Repository Secret: `VERCEL_ORG_ID`
- Repository Secret: `VERCEL_PROJECT_ID`

### 这些值从哪里拿

- `VERCEL_TOKEN`
  在 Vercel 个人设置或团队设置里创建 Token。
- `VERCEL_ORG_ID`
  组织 ID 或个人账号 ID。
- `VERCEL_PROJECT_ID`
  当前 Vercel 项目的项目 ID。

最直接的获取方式是本地装一次 Vercel CLI，在仓库根目录执行：

```bash
vercel link
cat .vercel/project.json
```

其中 `projectId` 对应 `VERCEL_PROJECT_ID`，`orgId` 对应 `VERCEL_ORG_ID`。`.vercel/` 已加入 `.gitignore`，不会被提交。

如果你已经在 Vercel 里导入过这个 GitHub 仓库，建议把 Vercel 侧的 Git 自动部署关掉，避免和 GitHub Actions 产生两套重复部署。

配置完成后，只要你向 `main` 分支推送新的 Markdown 文件，或者修改 `md_doc/` 下现有文件，GitHub Actions 就会自动重新构建并发布站点。

## 文档目录约定

- `md_doc/` 是文档源目录
- `md_doc/index.md` 是站点首页
- `vercel.json` 里定义了 Vercel 的构建命令和输出目录
- 其他 `.md` 文件会自动出现在导航中，不需要每次新增文档都手动改 `mkdocs.yml`

## 部署实现说明

当前方案使用 Vercel 官方 CLI：

- `vercel pull` 拉取项目配置
- `vercel build` 在 GitHub Actions 中执行 `vercel.json` 里的 MkDocs 构建
- `vercel deploy --prebuilt --prod` 将预构建结果发布到生产环境
