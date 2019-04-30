# IAM role ARNs

Here is a list of the ARNs that we have used and can potentially reuse for new lambdas or other AWS services

| ARN | used with | CloudWatch Logs | S3 | SNS | DynamoDB | Step Functions |
|---|---|---|---|---|---|---|
| arn:aws:iam::555751041262:role/vizTest_dashboard | weather_viz weather_db | full access | | | full access | |
| arn:aws:iam::555751041262:role/service-role/StepFunctionExecutionRoleForWeather | weather_viz weather_db | | | | | weather_viz |
| arn:aws:iam::555751041262:role/lambda_s3_dynamodb_cloudwatch_baskauf | bokeh-test | AWSOpsWorksCloudWatchLogs | full access | | baskauf_read_all_dynamodb | |

----
Revised 2019-04-30
