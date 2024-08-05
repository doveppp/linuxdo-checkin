 [English](./README_en.md)
 
# LinuxDo 每日签到（每日打卡）

## 项目描述
这个项目用于自动登录 [LinuxDo](https://linux.do/) 网站并随机读取几个帖子。它使用 Python 和 Playwright 自动化库模拟浏览器登录并浏览帖子。

## 功能
- 自动登录 LinuxDo。
- 自动浏览帖子。
- 每天在 GitHub Actions 中自动运行。

## 如何使用
本节只介绍在github actions中如何使用。在进行之前需要先fork本项目。

### 设置环境变量
在使用此自动化脚本之前，需要在 GitHub 仓库中配置两个环境变量 `USERNAME` 和 `PASSWORD`，这两个变量将用于登录 LinuxDo。按照以下步骤设置：

1. 登录 GitHub，进入你的项目仓库。
2. 点击仓库的 `Settings` 选项卡。
3. 在左侧菜单中找到 `Secrets` 部分，点击 `Actions`。
4. 点击 `New repository secret` 按钮。
5. 分别添加 `USERNAME` 和 `PASSWORD`：
   - 在 `Name` 字段中输入 `USERNAME`，在 `Value` 字段中输入你的 LinuxDo 用户名或者邮箱。
   - 重复上述步骤，这次输入 `PASSWORD` 作为 `Name`，相应的密码作为 `Value`。

### GitHub Actions 自动运行
此项目的 GitHub Actions 配置会自动每天零点 UTC 时间运行签到脚本。你无需进行任何操作即可启动此自动化任务。GitHub Actions 的工作流文件位于 `.github/workflows` 目录下，文件名为 `daily-check-in.yml`。

如果你需要手动触发此工作流，可以通过以下步骤操作：

1. 进入 GitHub 仓库的 `Actions` 选项卡。
2. 选择你想运行的工作流。
3. 点击 `Run workflow` 按钮，选择分支，然后点击 `Run workflow` 以启动工作流。
