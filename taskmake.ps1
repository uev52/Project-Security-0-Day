# Create a new task action
$filename = "{Filepath}"

$taskAction = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument '-File $filename'
$taskAction

$taskTrigger = New-ScheduledTaskTrigger -Daily -At 9AM
$tasktrigger

# Register the new PowerShell scheduled task

# The name of your scheduled task.
$taskName = "Update server tool"

# Describe the scheduled task.
$description = "Update de server"

# Register the scheduled task
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $taskAction `
    -Trigger $taskTrigger `
    -Description $description