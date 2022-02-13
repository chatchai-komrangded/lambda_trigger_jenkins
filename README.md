# Lambda_trigger_jenkins remotely
This is starter function to trigger jenkin remotely, Deploy it in 3 steps

0.) Enable jenkin remote trigger in your pipelines first


1.) Clone this repository, and deploy to Lambda function (Test in Python 3.9)


2.) Since, We store secret in AWS Secret manager, Please ensure Lambda role has permission to call it


3.) Configure Lambda environment such as jenkin url, jenkin pipeline name, jenkin auth token/api_token, and aws regions, You can check name in python code.
