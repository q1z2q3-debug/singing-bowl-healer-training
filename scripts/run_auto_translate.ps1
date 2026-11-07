# run_auto_translate.ps1
# Wrapper invoked by Windows Task Scheduler every 30 minutes.
# Runs auto_translate_driver.py with the project's Python.
$ErrorActionPreference = "SilentlyContinue"
$py  = "C:\Users\RunzeAI\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
$script = "C:\Users\RunzeAI\WorkBuddy\疗愈天地\singing-bowl-healer-training\scripts\auto_translate_driver.py"
& $py $script
