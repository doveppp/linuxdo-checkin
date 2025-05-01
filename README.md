# LinuxDo 每日签到（每日打卡）

## 项目描述

这个项目用于自动登录 [LinuxDo](https://linux.do/) 网站并随机读取几个帖子。它使用 Python 和 Playwright
自动化库模拟浏览器登录并浏览帖子，以达到自动签到的功能。

## 功能

- 自动登录`LinuxDo`。
- 自动浏览帖子。
- 每天在`GitHub Actions`中自动运行。
- 支持`青龙面板` 和 `Github Actions` 自动运行。
- (可选)`Telegram`通知功能，推送获取签到结果（目前只支持GitHub Actions方式）。
- (可选)`Gotify`通知功能，推送获取签到结果。
- (可选)`Server酱³`通知功能，推送获取签到结果。
## 环境变量配置

### 必填变量

| 环境变量名称             | 描述                | 示例值                                |
|--------------------|-------------------|------------------------------------|
| `LINUXDO_USERNAME` | 你的 LinuxDo 用户名或邮箱 | `your_username` 或 `your@email.com` |
| `LINUXDO_PASSWORD` | 你的 LinuxDo 密码     | `your_password`                    |

~~之前的USERNAME和PASSWORD环境变量仍然可用，但建议使用新的环境变量~~

### 可选变量

| 环境变量名称            | 描述                   | 示例值                                    |
|-------------------|----------------------|----------------------------------------|
| `GOTIFY_URL`      | Gotify 服务器地址         | `https://your.gotify.server:8080`      |
| `GOTIFY_TOKEN`    | Gotify 应用的 API Token | `your_application_token`               |
| `TELEGRAM_TOKEN`  | Telegram Bot Token   | `123456789:ABCdefghijklmnopqrstuvwxyz` |
| `TELEGRAM_USERID` | Telegram 用户 ID       | `123456789`                            |
| `SC3_PUSH_KEY`    | Server酱³ SendKey     | `sctpxxxxt`                             |
| `BROWSE_ENABLED`  | 是否启用浏览帖子功能        | `true` 或 `false`，默认为 `true`           |

---

## 如何使用

### GitHub Actions 自动运行

此项目的 GitHub Actions 配置会自动每天运行2次签到脚本。你无需进行任何操作即可启动此自动化任务。GitHub Actions 的工作流文件位于 `.github/workflows` 目录下，文件名为 `daily-check-in.yml`。

#### 配置步骤

1. **设置环境变量**：
    - 在 GitHub 仓库的 `Settings` -> `Secrets and variables` -> `Actions` 中添加以下变量：
        - `LINUXDO_USERNAME`：你的 LinuxDo 用户名或邮箱。
        - `LINUXDO_PASSWORD`：你的 LinuxDo 密码。
        - (可选) `BROWSE_ENABLED`：是否启用浏览帖子，`true` 或 `false`，默认为 `true`。
        - (可选) `GOTIFY_URL` 和 `GOTIFY_TOKEN`。
        - (可选) `SC3_PUSH_KEY`。
        - (可选) `TELEGRAM_TOKEN` 和 `TELEGRAM_USERID`。

2. **手动触发工作流**：
    - 进入 GitHub 仓库的 `Actions` 选项卡。
    - 选择你想运行的工作流。
    - 点击 `Run workflow` 按钮，选择分支，然后点击 `Run workflow` 以启动工作流。

#### 运行结果

##### 网页中查看

`Actions`栏 -> 点击最新的`Daily Check-in` workflow run -> `run_script` -> `Execute script`

可看到`Connect Info`：
（新号可能这里为空，多挂几天就有了）
![image](https://github.com/user-attachments/assets/853549a5-b11d-4d5a-9284-7ad2f8ea698b)

### 青龙面板使用

*注意：如果是docker容器创建的青龙，**请使用`whyour/qinglong:debian`镜像**，latest（alpine）版本可能无法安装部分依赖*

1. **依赖安装**
    - 首次运行前需要安装Python依赖
    - 进入青龙面板 -> 依赖管理 -> 安装依赖
      - 依赖类型选择`python3`
      - 自动拆分选择`是`
      - 名称填写(仓库`requirements.txt`文件的完整内容)：
        ```
        playwright==1.43.0
        wcwidth==0.2.13
        tabulate==0.9.0
        loguru==0.7.2
        requests==2.32.3
        ```
      - 点击`确定`按钮，等待安装完成

2. **添加仓库**
    - 进入青龙面板 -> 订阅管理 -> 创建订阅
    - 依次在对应的字段填入内容（未提及的不填）：
      - **名称**：Linux.DO 签到
      - **类型**：公开仓库
      - **链接**：https://github.com/doveppp/linuxdo-checkin.git
      - **分支**：main
      - **定时类型**：`crontab`
      - **定时规则**(拉取上游代码的时间，一天一次，可以自由调整频率): 0 0 * * *
      - **执行前**(注意：要先完成上一步的依赖安装才能执行这个指令)：`playwright install --with-deps firefox`

3. **配置环境变量**
    - 进入青龙面板 -> 环境变量 -> 创建变量
    - 需要配置以下变量：
        - `LINUXDO_USERNAME`：你的LinuxDo用户名/邮箱
        - `LINUXDO_PASSWORD`：你的LinuxDo密码
        - (可选) `BROWSE_ENABLED`：是否启用浏览帖子功能，`true` 或 `false`，默认为 `true`
        - (可选) `GOTIFY_URL`：Gotify服务器地址
        - (可选) `GOTIFY_TOKEN`：Gotify应用Token
        - (可选) `SC3_PUSH_KEY`：Server酱³ SendKey        
        - (可选) `TELEGRAM_TOKEN`：Telegram Bot Token
        - (可选) `TELEGRAM_USERID`：Telegram用户ID

4. **手动拉取脚本**
    - 首次添加仓库后不会立即拉取脚本，需要等待到定时任务触发，当然可以手动触发拉取
    - 点击右侧"运行"按钮可手动执行

#### 运行结果

##### 青龙面板中查看
- 进入青龙面板 -> 定时任务 -> 找到`Linux.DO 签到` -> 点击右侧的`日志`

### Gotify 通知

当配置了 `GOTIFY_URL` 和 `GOTIFY_TOKEN` 时，签到结果会通过 Gotify 推送通知。
具体 Gotify 配置方法请参考 [Gotify 官方文档](https://gotify.net/docs/).

### Server酱³ 通知

当配置了 `SC3_PUSH_KEY` 时，签到结果会通过 Server酱³ 推送通知。
获取 SendKey：请访问 [Server酱³ SendKey获取](https://sc3.ft07.com/sendkey) 获取你的推送密钥。

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

- **Github Actions**：默认状态下自动更新是关闭的，[点击此处](https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web/blob/main/README_CN.md#%E6%89%93%E5%BC%80%E8%87%AA%E5%8A%A8%E6%9B%B4%E6%96%B0)
查看打开自动更新步骤。
- **青龙面板**：更新是以仓库设置的定时规则有关，按照本文配置，则是每天0点更新一次。


