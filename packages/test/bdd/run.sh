#!/bin/bash
mkdir screenshots
mkdir logs

behave --tags=Regression -f allure_behave.formatter:AllureFormatter -o reports/allure_result -f pretty
echo "Environment=${ENVIRONMENT_NAME}"> reports/allure_result/environment.properties
/opt/allure-2.24.1/bin/allure generate reports/allure_result -o reports/allure_report --clean
echo "uploading reports...."
zip -r $FolderPath/$ReportFolder $FolderPath
aws s3 cp $FolderPath/$ReportFolder s3://$ReportBucket
webhook=$(python3 get_slack_webhook_url.py)

send_notification() {
  local colour='good'
  if [ "$1" == 'ERROR' ]; then
    colour='danger'
  elif [ "$1" == 'WARN' ]; then
    colour='warning'
  fi
  local message="payload={\"channel\": \"#goi-release\",\"attachments\":[{\"pretext\":\"$2\",\"text\":\"$3\",\"color\":\"$colour\"}]}"
  curl -s -X POST --data-urlencode "$message" ${webhook}
}
send_notification $Status "Automation Test: $ScriptName" "The Automation job has completed on ${ENVIRONMENT_NAME} environment with status: $Result.\nThe results can be found at: $S3Info"
