import boto3
import json
import botocore

class S3Submissions():
    def __init__(self, subredditid, submission):
        self.subredditid = subredditid
        self.submission = submission
        self.clear_subredditid_submissions()
        self.prefix = 'submissions'
        
    def get_resource(self):
        return boto3.resource('s3')
        
    def clear_subredditid_submissions():
        s3 = self.get_resource()
        obj = s3.Object('repic-db', self.prefix+'/'+str(subredditid))
        try:
            obj.load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print('key does not exist')
            else:
                # Something else has gone wrong.
                raise
        else:
            obj.delete()
            
    def dict_to_binary(self):
        submission_str = json.dumps(self.submission)
        binary = ' '.join(format(ord(letter), 'b') for letter in submission_str)
        self.binary = binary
        
    def upload(self):
        s3 = self.get_resource()
        obj = s3.Object('repic-db', self.prefix+'/'+self.subredditid)
        obj.put(Body=self.binary)    