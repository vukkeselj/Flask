from flask import Flask, render_template, request, json
import boto3
import datetime

app = Flask(__name__)

street = {}
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/form", methods=['GET', 'POST'])
def form():
        # get data from the form
    if request.method == "POST":
        street_name = request.form["element_1"]
        named_after = request.form["element_3"]
        description = request.form["element_2"]
        category = request.form["element_4"]
        year = request.form["element_5"]
        previous_name = request.form["element_6"]
        part_of_the_city = request.form["element_7"]
        references = request.form["element_8"]

        #creating a dictionary from variables and saving it as a JSON file
        for i in ["street_name", "named_after", "description", "category", "year", "previous_name", "part_of_the_city", "references"]:
            street[i] = eval(i)
        print(street)
        with open('street_name.json', 'w') as f:
            json.dump(street, f)
        
        #uploading JSON to S3 and adding a timestamp to its name
        now = datetime.datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M:%S")
        s3_filename = street_name + ' ' + dt
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file('/home/vuk/Flask/Flask/street_name.json', 'street-name', s3_filename)

        #sending an email notification confirming that new street was added
        sns = boto3.client('sns')
        sns_message = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:001173989425:Street_form_submitted',    
            Message=(s3_filename),
            Subject='new street'
        )

        # Send message to SQS queue
        sqs = boto3.client('sqs')
        queue_url = 'https://sqs.us-east-1.amazonaws.com/001173989425/JSON_street_name'
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageAttributes={
                'File': {
                    'DataType': 'String',
                    'StringValue': s3_filename
                }
            },
            #MessageGroupId='string',
            #MessageDeduplicationId='string',
            MessageBody=s3_filename
        )


        return render_template("ulica.html", ulica=street)
    else:
        return render_template("form.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)