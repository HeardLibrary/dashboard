import boto3
import json # library for working with JSON 
import csv  # library to reaad/write/parse CSV files

# ----------------------------------
# for notes on this labmda_handler function that reads the data, see scripts/lambda/bucket-drop-test.md

def lambda_handler(event, context):
    # read the file name from the event JSON
    in_file_name = event['Records'][0]['s3']['object']['key']
    in_bucket_name = 'baskauf-lambda-trigger-test'
    in_folder = ''
    s3_in_path = in_folder + in_file_name
    
    # configure the file input and read the file content
    # hacked from https://github.com/aws-samples/aws-python-sample/blob/master/s3_sample.py
    s3in = boto3.resource('s3') # s3 object
    in_bucket = s3in.Bucket(in_bucket_name) # bucket object
    in_file = in_bucket.Object(s3_in_path) # file object
    fileText = in_file.get()['Body'].read() # this inputs all the text in the file
    # infile.get() retrieves a dict.  The value of 'Body' in the dict is the StreamingBody() function
    # So the .read() method reads the stream and it gets passed to fileText
    # see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object
    
    # process the input text
    # note: since the fileText was read in as bytes, the .decode() function was required to make it a string
    # not sure what will happen if the encoding isn't utf-8 ...
    
    #outString = 'This was read from the file: '+in_file_name+'\n'+fileText.decode('utf-8')
    jsonString = fileText.decode('utf-8')

# ----------------------------------
# Text processing script

# for full documentation of the processing script, see the Jupyter notebook segment-text.ipynb

# variables hard-coded for testing

    # inputFilePath = '20140801CBS.json'
    outputFilePath = in_file_name.split(".")[0]+'-sentenceTable.csv'
    # print(inputFilePath)


# read episode text from file generated by text-to-speach

    # inputFileObject = open(inputFilePath, 'rt', newline='')
    # jsonString = inputFileObject.read()    # reads from the file object as text
    jsonStructure = json.loads(jsonString) # turns the JSON text into a Python dictionary


# traverse the JSON structure to get to the level of items

    items = jsonStructure['results']['items']


# create an empty objects for building the array of sentence data

    sentences = []   # empty list to contain sentence data
    firstWord = True # a flag indicating that the first encountered word is the start of a sentence


#  step through the items and assemble them into sentences

    for item in items:
        
        # if the item is a word, add it to the end of the sentence and reset the sentence end time
        if item['type'] == 'pronunciation':    
            endTime = item['end_time']          # the end time will be reset later if this isn't the last word
            if firstWord:
                startTime = item['start_time']  # if this is the first word in a sentence, record the start time
                sentence = item['alternatives'][0]['content']  # begin a new sentence with the first word
                firstWord = False               # the next word encountered will not be the first word in s sentence
            else:
                sentence += ' ' + item['alternatives'][0]['content']
            
        # if the item is punctuation, figure out if it ends the sentence or not
        elif item['type'] == 'punctuation':
            
            # the punctuation is a comma, so continue the sentence
            if item['alternatives'][0]['content'] == ',':
                sentence += ','
                
            # the punctuation is something else, end the sentence
            else:
                sentence += item['alternatives'][0]['content']   # add final punctuation
                sentences.append([startTime, endTime, sentence]) # add the sentence to the sentence list
                firstWord = True # the next word encountered will be considered the first word of a sentence
        
        # I don't believe that there are any other types of content, but if any show up, print them
        else:
            print(item['type'])  


# ## output the sentences to a CSV file

#    outputObject = open(outputFilePath, 'wt', newline = '', encoding = 'utf-8')
#    csvOutput = csv.writer(outputObject, delimiter = ',')
#    csvOutput.writerow(['startTime', 'endTime', 'sentence'])  # output the header row
#    for sentence in sentences:
#        csvOutput.writerow(sentence)  # output the data for each sentence
#    outputObject.close()

# Concatenate all of the sentence strings into a single string to be output
    outString = '"startTime","endTime","sentence"\n'
    for sentence in sentences:
        outString += '"'+sentence[0]+'","'+sentence[1]+'","'+sentence[2]+'"\n'

# ----------------------------------

# returning to the lambda handler function described at scripts/lambda/bucket-drop-test.md

    # configure the output
    out_bucket_name = 'baskauf-lambda-output'
    out_file_name = outputFilePath
    out_folder = ''
    s3_out_path = out_folder + out_file_name

    s3out = boto3.resource("s3")
    s3out.Bucket(out_bucket_name).put_object(Key=s3_out_path, Body=outString)
