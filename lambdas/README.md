# Lambdas for AWS

This directory contains python scripts to be uploaded as lambdas in AWS. 

## Contents

The lambdas themselves have .py extensions.

The lambdas must be packaged in .zip files before being uploaded.  Those zip files are stored in the zips subdirectory.  If the Python script requires any modules that aren't included by default in the AWS system, they need to be downloaded and included in the zip.

Corresponding files with .sh extensions are shell scripts that contain the AWS CLI (command line interface) commands to upload the zip files to the user's AWS account.  Here's an example CLI command:

```
aws lambda create-function --region us-east-2 --function-name weather_viz --zip-file fileb://weather.zip --role arn:aws:iam::555751041262:role/vizTest_dashboard --handler weather.lambda_handler --runtime python3.7 --memory-size 512
```

The `--handler` switch should have the Python file name before the dot and the handler function name after the dot.  `--function-name` can be anything - it's how the function will be named on the list of lambdas.  The `--zip-file` switch requires `fileb://` in front of the file name for a file in the local directory (not sure why).  `--region` is `us-east-2` for Ohio and `us-east-1` for northern Virginia.

## Notes 

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

----
Revised 2019-04-16
