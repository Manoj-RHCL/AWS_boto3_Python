#!/usr/bin/python
#Python Program for creating a connection
import boto3
import time
from csv import DictReader
from re import sub
#Function for connecting to EC2
ec2 = boto3.client('ec2')

# open file in read mode
with open('C:\\Users\\Admin\\Downloads\\EC2.csv', 'r') as read_obj:
    # pass the file object to DictReader() to get the DictReader object
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        #Function for creating a EC2
        instances = ec2.run_instances(
                ImageId=row['ImageId'],
                InstanceType=row['InstanceType'],
                MaxCount=1,
                MinCount=1,
                #SubnetId='subnet-05d5abef5fe57a847',
                UserData=open(row['UserData']).read(),
                KeyName=row['KeyName'],
                DisableApiTermination=False,
                InstanceInitiatedShutdownBehavior='terminate',
                #PrivateIpAddress='string',
                #SecurityGroupIds='sssd',
                BlockDeviceMappings=[
                    {'DeviceName': '/dev/xvda',
                     'VirtualName': 'OS_DISK',
                     'Ebs': {'VolumeType' :row['Volume_OS_Type'] },
                     'NoDevice': ''
                    }
                    ],
                TagSpecifications=[
                    {
                        'ResourceType': 'volume',
                        'Tags': [
                            {'Key':row['Tag_Key_1'], 'Value':row['Tag_Value_1']},
                            {'Key':row['Tag_Key_2'], 'Value':row['Tag_Value_2']},
                            {'Key':row['Tag_Key_3'], 'Value':row['Tag_Value_3']},
                            {'Key':row['Tag_Key_4'], 'Value':row['Tag_Value_4']},
                            {'Key':row['Tag_Key_5'], 'Value':row['Tag_Value_5']},
                            {'Key':row['Tag_Key_6'], 'Value':row['Tag_Value_6']}
                        ]
                    }
                ],
                NetworkInterfaces= [
                    {'AssociatePublicIpAddress': False, 'DeviceIndex': 0, 'SubnetId': row['SubnetId'] }
                ],
                IamInstanceProfile={
                    'Name': row['IamInstanceProfile']
                }
                )
        print(instances['Instances'][0]['InstanceId'])
        #waiter=ec2.get_waiter('instance_running')
        #waiter.wait(instances['Instances'][0]['InstanceId'])
        #Function for EC2 Tags
        ec2.create_tags(
                    Resources=[instances['Instances'][0]['InstanceId']], 
                    Tags=[
                        {'Key':row['Tag_Key_1'], 'Value':row['Tag_Value_1']},
                        {'Key':row['Tag_Key_2'], 'Value':row['Tag_Value_2']},
                        {'Key':row['Tag_Key_3'], 'Value':row['Tag_Value_3']},
                        {'Key':row['Tag_Key_4'], 'Value':row['Tag_Value_4']},
                        {'Key':row['Tag_Key_5'], 'Value':row['Tag_Value_5']},
                        {'Key':row['Tag_Key_6'], 'Value':row['Tag_Value_6']}])
        
        count = 1
        while (count <= int(row['Volume_Count'])):
            volume= ec2.create_volume(
                    AvailabilityZone=row['Zone'],
                    Encrypted=False,
                    #Iops=100,
                    #KmsKeyId='string',
                    Size=int(row['Volume_DATA_Size_' + str(count)]),
                    VolumeType=(row['Volume_DATA_Type_' + str(count)]), 
                    DryRun=False)
            print(volume['VolumeId'])
            
            #volume_id = volume['VolumeId']
        
            #Function for Volume Tags
            ec2.create_tags(
                    Resources=[volume['VolumeId']], 
                        Tags=[
                            {'Key':row['Tag_Key_1'], 'Value':row['Tag_Value_1']},
                            {'Key':row['Tag_Key_2'], 'Value':row['Tag_Value_2']},
                            {'Key':row['Tag_Key_3'], 'Value':row['Tag_Value_3']},
                            {'Key':row['Tag_Key_4'], 'Value':row['Tag_Value_4']},
                            {'Key':row['Tag_Key_5'], 'Value':row['Tag_Value_5']},
                            {'Key':row['Tag_Key_6'], 'Value':row['Tag_Value_6']}])

            time.sleep(40)

            volume = ec2.attach_volume(
                    Device=(row['Device_D_' + str(count)]), 
                    InstanceId=instances['Instances'][0]['InstanceId'], 
                    VolumeId=volume['VolumeId'],
                    DryRun=False)
            print("State : ",volume['State'])
            count = count + 1