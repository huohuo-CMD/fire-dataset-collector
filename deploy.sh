#!/bin/bash
# 一键部署到 GitHub

set -e

echo "=========================================="
echo "GitHub 数据集采集器 - 一键部署"
echo "=========================================="

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "错误: 需要安装 Git"
    exit 1
fi

# 检查 GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "错误: 需要安装 GitHub CLI (gh)"
    echo "安装: https://cli.github.com/"
    exit 1
fi

# 登录检查
if ! gh auth status &> /dev/null; then
    echo "请先登录 GitHub:"
    gh auth login
fi

# 输入仓库名
read -p "请输入仓库名 [fire-dataset-collector]: " REPO_NAME
REPO_NAME=${REPO_NAME:-fire-dataset-collector}

echo ""
echo "创建 GitHub 仓库: $REPO_NAME"
echo ""

# 创建远程仓库
gh repo create "$REPO_NAME" --public --source=. --push

echo ""
echo "=========================================="
echo "部署完成!"
echo "=========================================="
echo ""
echo "下一步:"
echo "1. 访问 https://github.com/$(gh api user --jq .login)/$REPO_NAME"
echo "2. 进入 Actions 页面查看运行状态"
echo "3. 点击 'Run workflow' 手动触发采集"
echo "4. 等待数据积累，或配置 Git LFS 存储大文件"
echo ""
echo "提示: GitHub Actions 免费版限制:"
echo "- 每月 2000 分钟"
echo "- 每次运行最长 6 小时"
echo "- 仓库最大 1GB"
echo ""
echo "如需存储更多数据，建议使用 Git LFS:"
echo "gh repo lfs install"
echo "git lfs track 'dataset/**/*.jpg'"
echo ""