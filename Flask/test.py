import boto3
import json
def lambda_handler(event,context):        
        sqs = boto3.client('sqs')
        
        queue_url = 'https://sqs.eu-central-1.amazonaws.com/001173989425/fifo_q.fifo'
        
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
        )
        
        message = response['Messages'][0]
        file_name = message['Body']
        print(file_name)

        
        s3 = boto3.client('s3')
        my_bucket = s3.get_object(Bucket='players-lambda', Key=file_name)
        cont = my_bucket['Body'].read().decode('utf-8')
        
        
        lista_igraca = cont.splitlines()
        
        db = boto3.resource('dynamodb')
        table = db.Table('players')
        
        for x in lista_igraca:
            player_name=x
            titles=0
            current_stadium='Old Traford'
            preferred_position=''
            age=''
            
            input = {
                'Player': player_name,
                'Club': file_name[:-10].capitalize(), 
                'titles': titles, 
                'Stadium': current_stadium, 
                'PreferredPosition': preferred_position,
                'Age': age
                
            }
            table.put_item(Item=input)
            

        sns = boto3.client('sns')
        sns_message = sns.publish(
            TopicArn='arn:aws:sns:eu-central-1:001173989425:players_db_updated',    
            Message=('the following players were added to DB \n' + cont),
            Subject='Players_DB_updated'
        )
        
        
