# AWS Infrastructure Documentation

Generated: 2025-04-15T07:11:46.972041

## Overview

- ec2: 2 resources
- s3: 12 resources
- rds: 0 resources
- lambda: 11 resources

## Resources

### EC2

#### i-0c15ccc48053c63d9

**Tags:**
- Name: target_machine

**Configuration:**
```json
{
  "id": "i-0c15ccc48053c63d9",
  "launch_time": "2025-02-05T09:13:20+00:00",
  "security_groups": [
    {
      "GroupId": "sg-003b6a7641a93cfdb",
      "GroupName": "launch-wizard-6"
    }
  ],
  "state": "stopped",
  "subnet_id": "subnet-0ebdea56a36355102",
  "tags": [
    {
      "Key": "Name",
      "Value": "target_machine"
    }
  ],
  "type": "t2.micro",
  "vpc_id": "vpc-081134d54dec74aa3"
}
```

**Security Groups:**
- sg-003b6a7641a93cfdb: launch-wizard-6



---
#### i-0e5fac8adcc567f98

**Tags:**
- Name: mylinuxvm

**Configuration:**
```json
{
  "id": "i-0e5fac8adcc567f98",
  "launch_time": "2025-02-25T01:03:09+00:00",
  "security_groups": [
    {
      "GroupId": "sg-0a781c6b5fe9b6dff",
      "GroupName": "launch-wizard-3"
    }
  ],
  "state": "stopped",
  "subnet_id": "subnet-0ebdea56a36355102",
  "tags": [
    {
      "Key": "Name",
      "Value": "mylinuxvm"
    }
  ],
  "type": "t2.micro",
  "vpc_id": "vpc-081134d54dec74aa3"
}
```

**Security Groups:**
- sg-0a781c6b5fe9b6dff: launch-wizard-3



---
### S3

#### blpgathon


**Configuration:**
```json
{
  "creation_date": "2025-04-14T16:41:25+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": true
      }
    ]
  },
  "location": null,
  "name": "blpgathon"
}
```




---
#### cdk-hnb659fds-assets-381492198534-us-east-1


**Configuration:**
```json
{
  "creation_date": "2025-03-15T09:25:32+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "aws:kms"
        },
        "BucketKeyEnabled": false
      }
    ]
  },
  "location": null,
  "name": "cdk-hnb659fds-assets-381492198534-us-east-1"
}
```




---
#### cf-templates-1bg1nmsv04efv-us-east-1


**Configuration:**
```json
{
  "creation_date": "2025-03-14T09:42:20+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": false
      }
    ]
  },
  "location": null,
  "name": "cf-templates-1bg1nmsv04efv-us-east-1"
}
```




---
#### codepipeline-us-east-1-5c9d6940c007-4983-a615-45268572582c


**Configuration:**
```json
{
  "creation_date": "2025-04-14T06:13:57+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": false
      }
    ]
  },
  "location": null,
  "name": "codepipeline-us-east-1-5c9d6940c007-4983-a615-45268572582c"
}
```




---
#### deepusid


**Configuration:**
```json
{
  "creation_date": "2024-07-05T09:09:31+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": true
      }
    ]
  },
  "location": "us-east-2",
  "name": "deepusid"
}
```




---
#### elasticbeanstalk-us-east-1-381492198534


**Configuration:**
```json
{
  "creation_date": "2025-02-10T01:23:47+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": false
      }
    ]
  },
  "location": null,
  "name": "elasticbeanstalk-us-east-1-381492198534"
}
```




---
#### email-recipient-data


**Configuration:**
```json
{
  "creation_date": "2025-01-11T01:28:44+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": true
      }
    ]
  },
  "location": null,
  "name": "email-recipient-data"
}
```




---
#### my-deepika-unique-bucket-name


**Configuration:**
```json
{
  "creation_date": "2025-02-06T11:09:54+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": false
      }
    ]
  },
  "location": "us-west-2",
  "name": "my-deepika-unique-bucket-name"
}
```




---
#### my-mail-storage


**Configuration:**
```json
{
  "creation_date": "2025-01-11T05:37:19+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": true
      }
    ]
  },
  "location": null,
  "name": "my-mail-storage"
}
```




---
#### ownwebsite


**Configuration:**
```json
{
  "creation_date": "2024-07-05T08:44:13+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": true
      }
    ]
  },
  "location": "us-east-2",
  "name": "ownwebsite"
}
```




---
#### serverless-chat-dev-serverlessdeploymentbucket-w2v2yvrkstkg


**Configuration:**
```json
{
  "creation_date": "2024-12-02T09:55:40+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": false
      }
    ]
  },
  "location": null,
  "name": "serverless-chat-dev-serverlessdeploymentbucket-w2v2yvrkstkg"
}
```




---
#### serverless-framework-deployments-us-east-1-9c0c8fd0-151d


**Configuration:**
```json
{
  "creation_date": "2025-03-14T16:02:48+00:00",
  "encryption": {
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": false
      }
    ]
  },
  "location": null,
  "name": "serverless-framework-deployments-us-east-1-9c0c8fd0-151d"
}
```




---
### RDS

### LAMBDA

#### serverless-chat-dev-custom-resource-apigw-cw-role


**Configuration:**
```json
{
  "handler": "api-gateway-cloud-watch-role/handler.handler",
  "last_modified": "2025-03-14T14:28:57.000+0000",
  "memory": 1024,
  "name": "serverless-chat-dev-custom-resource-apigw-cw-role",
  "role": "arn:aws:iam::381492198534:role/serverless-chat-dev-IamRoleCustomResourcesLambdaExe-kCHBU8MBRVhg",
  "runtime": "nodejs20.x",
  "timeout": 180,
  "vpc_config": null
}
```



**Runtime Info:**
- Runtime: nodejs20.x
- Handler: api-gateway-cloud-watch-role/handler.handler
- Memory: 1024MB
- Timeout: 180s

---
#### websocket-api-chat-app-tu-SendMessageHandlerDCEABF-EQ3PpM4JehQb


**Configuration:**
```json
{
  "handler": "index.handler",
  "last_modified": "2025-03-14T09:44:12.417+0000",
  "memory": 128,
  "name": "websocket-api-chat-app-tu-SendMessageHandlerDCEABF-EQ3PpM4JehQb",
  "role": "arn:aws:iam::381492198534:role/websocket-api-chat-app-tu-SendMessageHandlerService-M8g8FrjsWmUZ",
  "runtime": "nodejs20.x",
  "timeout": 3,
  "vpc_config": null
}
```



**Runtime Info:**
- Runtime: nodejs20.x
- Handler: index.handler
- Memory: 128MB
- Timeout: 3s

---
#### SwasthyasheStack-SubscriptionHandlerAD1B68B4-4eNQ1By6WToY


**Configuration:**
```json
{
  "handler": "subscription.handler",
  "last_modified": "2025-03-28T10:38:57.000+0000",
  "memory": 128,
  "name": "SwasthyasheStack-SubscriptionHandlerAD1B68B4-4eNQ1By6WToY",
  "role": "arn:aws:iam::381492198534:role/SwasthyasheStack-SubscriptionHandlerServiceRoleEB93-NpsHDY1GY7K4",
  "runtime": "nodejs18.x",
  "timeout": 3,
  "vpc_config": {
    "Ipv6AllowedForDualStack": false,
    "SecurityGroupIds": [],
    "SubnetIds": [],
    "VpcId": ""
  }
}
```



**Runtime Info:**
- Runtime: nodejs18.x
- Handler: subscription.handler
- Memory: 128MB
- Timeout: 3s

---
#### websocket-api-chat-app-tu-DisconnectHandlerCB7ED6F-YXy9NEWIMknG


**Configuration:**
```json
{
  "handler": "index.handler",
  "last_modified": "2025-03-14T09:44:12.318+0000",
  "memory": 128,
  "name": "websocket-api-chat-app-tu-DisconnectHandlerCB7ED6F-YXy9NEWIMknG",
  "role": "arn:aws:iam::381492198534:role/websocket-api-chat-app-tu-DisconnectHandlerServiceR-5tnZUKAKVExj",
  "runtime": "nodejs20.x",
  "timeout": 3,
  "vpc_config": null
}
```



**Runtime Info:**
- Runtime: nodejs20.x
- Handler: index.handler
- Memory: 128MB
- Timeout: 3s

---
#### serverless-chat-dev-websocketHandler


**Configuration:**
```json
{
  "handler": "src/handler.handle",
  "last_modified": "2025-03-14T14:28:57.000+0000",
  "memory": 1024,
  "name": "serverless-chat-dev-websocketHandler",
  "role": "arn:aws:iam::381492198534:role/serverless-chat-dev-us-east-1-lambdaRole",
  "runtime": "nodejs18.x",
  "timeout": 6,
  "vpc_config": {
    "Ipv6AllowedForDualStack": false,
    "SecurityGroupIds": [],
    "SubnetIds": [],
    "VpcId": ""
  }
}
```



**Runtime Info:**
- Runtime: nodejs18.x
- Handler: src/handler.handle
- Memory: 1024MB
- Timeout: 6s

---
#### my_mail_function


**Configuration:**
```json
{
  "handler": "lambda_function.lambda_handler",
  "last_modified": "2025-01-11T06:00:45.000+0000",
  "memory": 128,
  "name": "my_mail_function",
  "role": "arn:aws:iam::381492198534:role/My_mail",
  "runtime": "python3.9",
  "timeout": 3,
  "vpc_config": null
}
```



**Runtime Info:**
- Runtime: python3.9
- Handler: lambda_function.lambda_handler
- Memory: 128MB
- Timeout: 3s

---
#### deepuwebsocketsend


**Configuration:**
```json
{
  "handler": "lambda_function.lambda_handler",
  "last_modified": "2025-03-10T06:29:46.000+0000",
  "memory": 128,
  "name": "deepuwebsocketsend",
  "role": "arn:aws:iam::381492198534:role/service-role/deepuwebsocketsend-role-pkdipd6b",
  "runtime": "python3.9",
  "timeout": 3,
  "vpc_config": null
}
```



**Runtime Info:**
- Runtime: python3.9
- Handler: lambda_function.lambda_handler
- Memory: 128MB
- Timeout: 3s

---
#### deepusocketdelete


**Configuration:**
```json
{
  "handler": "lambda_function.lambda_handler",
  "last_modified": "2025-03-10T06:26:37.000+0000",
  "memory": 128,
  "name": "deepusocketdelete",
  "role": "arn:aws:iam::381492198534:role/service-role/deepusocketdelete-role-0m9gwvz8",
  "runtime": "python3.9",
  "timeout": 3,
  "vpc_config": null
}
```



**Runtime Info:**
- Runtime: python3.9
- Handler: lambda_function.lambda_handler
- Memory: 128MB
- Timeout: 3s

---
#### websocket-api-chat-app-tuto-ConnectHandler2FFD52D8-B8iGLokNQIcF


**Configuration:**
```json
{
  "handler": "index.handler",
  "last_modified": "2025-03-14T09:44:12.556+0000",
  "memory": 128,
  "name": "websocket-api-chat-app-tuto-ConnectHandler2FFD52D8-B8iGLokNQIcF",
  "role": "arn:aws:iam::381492198534:role/websocket-api-chat-app-tu-ConnectHandlerServiceRole-FtL2q5f5IvSm",
  "runtime": "nodejs20.x",
  "timeout": 3,
  "vpc_config": null
}
```



**Runtime Info:**
- Runtime: nodejs20.x
- Handler: index.handler
- Memory: 128MB
- Timeout: 3s

---
#### send-bulk-email


**Configuration:**
```json
{
  "handler": "lambda_function.lambda_handler",
  "last_modified": "2025-01-11T02:13:22.000+0000",
  "memory": 128,
  "name": "send-bulk-email",
  "role": "arn:aws:iam::381492198534:role/mass_mailing",
  "runtime": "python3.9",
  "timeout": 3,
  "vpc_config": null
}
```



**Runtime Info:**
- Runtime: python3.9
- Handler: lambda_function.lambda_handler
- Memory: 128MB
- Timeout: 3s

---
#### websocket-api-chat-app-tuto-DefaultHandler604DF7AC-de3Y3udO0bKx


**Configuration:**
```json
{
  "handler": "index.handler",
  "last_modified": "2025-03-14T09:44:12.457+0000",
  "memory": 128,
  "name": "websocket-api-chat-app-tuto-DefaultHandler604DF7AC-de3Y3udO0bKx",
  "role": "arn:aws:iam::381492198534:role/websocket-api-chat-app-tu-DefaultHandlerServiceRole-fgiNsLoUbSIB",
  "runtime": "nodejs20.x",
  "timeout": 3,
  "vpc_config": null
}
```



**Runtime Info:**
- Runtime: nodejs20.x
- Handler: index.handler
- Memory: 128MB
- Timeout: 3s

---
