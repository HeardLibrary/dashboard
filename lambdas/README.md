# Lambdas for AWS

This directory contains python scripts to be uploaded as lambdas in AWS. 

## Contents

The lambdas themselves have .py extensions.

The lambdas must be packaged in .zip files before being uploaded.  Those zip files are stored in the zips subdirectory.  If the Python script requires any modules that aren't included by default in the AWS system, they need to be downloaded and included in the zip.

Here's the command to download a module ("requests") using PIP to the `~/temp` directory:

```
pip install requests -t ~/temp
```

Corresponding files with .sh extensions are shell scripts that contain the AWS CLI (command line interface) commands to upload the zip files to the user's AWS account.  Here's an example CLI command:

```
aws lambda create-function --region us-east-2 --function-name weather_viz --zip-file fileb://weather.zip --role arn:aws:iam::555751041262:role/vizTest_dashboard --handler weather.lambda_handler --runtime python3.7 --memory-size 512
```

The `--handler` switch should have the Python file name before the dot and the handler function name after the dot.  `--function-name` can be anything - it's how the function will be named on the list of lambdas.  The `--zip-file` switch requires `fileb://` in front of the file name for a file in the local directory (not sure why).  `--region` is `us-east-2` for Ohio and `us-east-1` for northern Virginia.

# Notes 

## bash scripts

The bash scripts must start with 

```
#!/bin/bash
```

which is the shebang that indicates that bash is the shell to be used.

The permissions of the script can be changed using 

```
chmod u+x hello-world.sh
```

to make the file executable.  Use

```
ls -lha
```

to view the permissions.  But it's simpler to just enter

```
sh hello-world.sh
```

to execute the shell script.  

## DynamoDB

I struggled with trying to save numbers in DynamoDB but kept running into the error "Float types are not supported. Use Decimal types instead." even when the number passed was an integer zero.  So I gave up and just saved the data as strings.  So when they are read from the database, they will have to be converted from strings to numbers again.

## Adding IAM execution roles to lambdas for step functions

When the step function is created, there is an opportunity to automatically add an inline policy for each invoked lambda that will allow the step function to trigger the lambda.  However, if additional lambdas are added to the step function, they will fail unless they also have an added inline policy that allows them to also be executed by the step function.

Go to the IAM console and find the role that was created automatically for the initial lambda (for example `StepFunctionExecutionRoleForWeather`).  Click on the policy, then click on the `Lambda` service.  Click on `InvokeFunction`.  You'll see the existing lambda functions that can be invoked.  Click on the `Edit policy` button.  Expand the `Lambda` dropdown. Click on the `Resources` block. Click on `Add ARN to restrict access` link.  In the popup window, click on `List ARNs manually`.  Paste in the ARN of the new labda to be added.  Click the `Add` button.  Then click on the `Review policy` button.  Then click on the `Save changes` button.

## Triggering the step function with a CRON job

See <https://aws.amazon.com/getting-started/tutorials/scheduling-a-serverless-workflow-step-functions-cloudwatch-events/> for details.  I created one called `arn:aws:events:us-east-2:555751041262:rule/saveWeatherData` to collect the weather data each night at 11:59 PM (GMT -5 = Central Daylight time) = 04:59 UTC.  It has the same kind of specific IAM execution role as described in the last section.

----
Revised 2019-04-16
