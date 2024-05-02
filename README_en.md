# LinuxDo Daily Check-in

## Project Description
This project automates daily check-ins on the [LinuxDo](https://linux.do/) website. It uses Python and the Playwright automation library to simulate browser login and check-in activities.

## Features
- Automatically logs into LinuxDo.
- Completes daily check-ins.
- Runs automatically in GitHub Actions.

## Technology Stack
- Python
- Playwright
- GitHub Actions

## How to Use
This section only explains how to use this automation within GitHub Actions. Please fork this repository before proceeding.

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