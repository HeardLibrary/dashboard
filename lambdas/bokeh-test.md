# Notes on failed test to deploy Bokeh in an AWS lambda 2019-04-29

## Bokeh quickstart

I started here: https://bokeh.pydata.org/en/latest/docs/user_guide/quickstart.html#userguide-quickstart

and used their code example to create an HTML page.  

The output processing is determined by the command for the results.  In the example, it's `show()`, but for output to a file it needs to be `save()`.  See https://bokeh.pydata.org/en/latest/docs/reference/io.html#bokeh-io for info on the save command.  The challenge here is to actually output to an S3 bucket while the `save()` function outputs to the file system. 

## writing to the filesystem

This StackOverflow question asks about how to do that https://stackoverflow.com/questions/55071809/location-of-bokeh-plot-output-following-aws-lambda-function, which references this page: https://stackoverflow.com/questions/35006874/how-do-you-write-to-the-file-system-of-an-aws-lambda-instance .  Unfortunately, it's a Javascript example.   Nevertheless, it doesn't seem too hard to access the `/temp` directory of the local file system, as indicated here: https://stackoverflow.com/questions/35641994/accessing-local-filesystem-in-aws-lambda/35642189 and even more simply here: https://apassionatechie.wordpress.com/2018/01/21/write-to-tmp-directory-in-aws-lambda-with-python/ 

I was able to read and write in this test lambda:

```python
import os

def lambda_handler(event, context):
    os.chdir('/tmp')
    someText = "Goin' into the file!"
    with open('datafile.txt', 'wt', encoding='utf-8') as fileObject:
        fileObject.write(someText)
    
    with open('datafile.txt', 'rt', encoding='utf-8') as fileObject:
        lineList = fileObject.read()
    print(lineList)
```

In theory, one can change to the tmp directory as in the example, let Bokeh write to the file, then load the HTML file as in the example above and save the text into the S3 bucket.  

## Uploading the Bokeh module

Since Bokeh isn't part of the standard AWS library, it will have to be uploaded as part of a .zip file.  Initially, I downloaded the entire thing, including all of the dependencies, using 

```
pip install bokeh -t ~/temp
```

I then added the stub Python lambda to the directory, zipped it up, then uploaded using this AWS CLI command:

```
aws lambda create-function --region us-east-2 --function-name bokeh --zip-file fileb://bokeh.zip --role arn:aws:iam::555751041262:role/lambda_s3_access --handler bokeh.lambda_handler --runtime python3.6 --memory-size 512
```

However, it was too big to edit online and it failed with no real way for me to troubleshoot.  

However, some of the dependencies like numpy are now part of the AWS standard library.  I found one example of somebody actually trying to use Bokeh: https://stackoverflow.com/questions/54542060/aws-lambda-layer-for-bokeh .  It involved using AWS "layers", which is apparently a new thing.  See this post: https://medium.com/@qtangs/creating-new-aws-lambda-layer-for-python-pandas-library-348b126e9f3e for more on that.  Unfortunately, I haven't seen that anybody has already created a layer for Bokeh: https://github.com/mthenw/awesome-layers .  It looks like I might be able to follow the first StackOverflow to build the layer, or maybe install Bokeh by creating a zip that doesn't include all of the dependencies.  

Did that - it was pretty simple.  I just created the 'requirements.txt' file, then ran the get_layer_packages.sh shell script to created the layer. Packaged the "python" directory as a .zip file.  

I then followed the directions under "Managing Layers" at https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html .  I used the command

```
aws lambda publish-layer-version --layer-name bokeh-layer --description "Bokeh layer" --license-info "MIT" \
--content S3Bucket=baskauf-bokeh,S3Key=python.zip --compatible-runtimes python3.6
```

The creation was successful and I got this result:
```
"LayerArn": "arn:aws:lambda:us-east-2:555751041262:layer:bokeh-layer"
"LayerVersionArn": "arn:aws:lambda:us-east-2:555751041262:layer:bokeh-layer:1"
"Description": "Bokeh layer"
```