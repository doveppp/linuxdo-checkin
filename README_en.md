# LinuxDo Daily Check-in

## Project Description
This project is designed to automatically log into the [LinuxDo](https://linux.do/) website and randomly read several posts. It utilizes Python in conjunction with the Playwright automation library to simulate browser login and post browsing activities.

## Features
- Automatically logs into LinuxDo.
- Completes daily check-ins.
- Automatically browse posts.
- Runs automatically in GitHub Actions.

## How to Use
This section solely focuses on how to utilize GitHub Actions. Prior to proceeding, you need to fork this project first.

### Setting Environment Variables
Before using this automation script, you need to configure two environment variables `USERNAME` and `PASSWORD` in your GitHub repository, which will be used to log into LinuxDo. Follow these steps to set up:

1. Log into GitHub and navigate to your repository.
2. Click on the `Settings` tab of the repository.
3. Find the `Secrets` section on the left menu and click on `Actions`.
4. Click the `New repository secret` button.
5. Add both `USERNAME` and `PASSWORD`:
   - In the `Name` field, enter `USERNAME` and in the `Value` field, enter your LinuxDo username or email.
   - Repeat the process, this time entering `PASSWORD` as the `Name` and the corresponding password as the `Value`.

### GitHub Actions Automatic Execution
The GitHub Actions configuration in this project automatically runs the check-in script at midnight UTC every day. You do not need to take any action to initiate this automated task. The workflow file is located in the `.github/workflows` directory and is named `daily-check-in.yml`.

If you need to manually trigger this workflow, you can do so by following these steps:

1. Go to the `Actions` tab of your GitHub repository.
2. Select the workflow you want to run.
3. Click the `Run workflow` button, choose the branch, and then click `Run workflow` to initiate the workflow.
