# LinuxDo 每日签到（每日打卡）

## 项目描述
这个项目用于自动登录 [LinuxDo](https://linux.do/) 网站并随机读取几个帖子。它使用 Python 和 Playwright 自动化库模拟浏览器登录并浏览帖子，以达到自动签到的功能。

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
3. 在左侧菜单中找到 `Secrets and variables` 部分，点击 `Actions`。
4. 点击 `New repository secret` 按钮。
5. 分别添加 `USERNAME` 和 `PASSWORD`：
   - 在 `Name` 字段中输入 `USERNAME`，在 `Value` 字段中输入你的 LinuxDo 用户名或者邮箱。
   - 重复上述步骤，这次输入 `PASSWORD` 作为 `Name`，相应的密码作为 `Value`。

### GitHub Actions 自动运行
此项目的 GitHub Actions 配置会自动每天 UTC 时间1点运行签到脚本。你无需进行任何操作即可启动此自动化任务。GitHub Actions 的工作流文件位于 `.github/workflows` 目录下，文件名为 `daily-check-in.yml`。

如果你需要手动触发此工作流，可以通过以下步骤操作：

1. 进入 GitHub 仓库的 `Actions` 选项卡。
2. 选择你想运行的工作流。
3. 点击 `Run workflow` 按钮，选择分支，然后点击 `Run workflow` 以启动工作流。

## 运行结果

### 网页中查看
`Actions`栏 -> 点击最新的`Daily Check-in` workflow run -> `run_script` -> `Execute script`

可看到`Connect Info`：
（新号可能这里为空，多挂几天就有了）
![image](https://github.com/user-attachments/assets/853549a5-b11d-4d5a-9284-7ad2f8ea698b)

### Telegram 通知

可选功能：配置 Telegram 通知，实时获取签到结果。

需要在 GitHub Secrets 中配置：
- `TELEGRAM_TOKEN`：Telegram Bot Token
- `TELEGRAM_USERID`：Telegram 用户 ID

获取方法：
1. Bot Token：与 [@BotFather](https://t.me/BotFather) 对话创建机器人获取
2. 用户 ID：与 [@userinfobot](https://t.me/userinfobot) 对话获取

未配置时将自动跳过通知功能，不影响签到。

## 自动更新

默认状态下自动更新是关闭的，[点击此处](https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web/blob/main/README_CN.md#%E6%89%93%E5%BC%80%E8%87%AA%E5%8A%A8%E6%9B%B4%E6%96%B0)查看打开自动更新步骤。
