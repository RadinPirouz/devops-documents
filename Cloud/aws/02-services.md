biling: 
we can see budger used in this month used on old months and more for iam user we must active iam permmsion with root account and give access to target account

on this service we have somthing named budget can set limit for us and send alert for us if thresholds got filled  

we have diffrent types of budget:
Zero spend budgetCreate a budget that notifies you once your spending exceeds $0.01.
Monthly cost budgetCreate a monthly budget that notifies you if you exceed, or are forecasted to exceed, the budget amount.
Daily Savings Plans coverage budgetCreate a coverage budget for your Savings Plans that notifies you when you fall below the defined target.
Daily reservation utilization budgetCreate a utilization budget for your reservations that notifies you when you fall below the defined target.


EC2: Elastic Compute Cloud = IASS

bootsrapping mean run script on vm start 

security groups are firewall of ec2 instance in aws for create ec2 instance we go to ec2 menu and instance menu and create instance 

when use Auto-assigned IP address after off and on instance it changed and its dynamic but private ip dont changed 

EC2 Insteance Types:

1.Gernal Purpose: greate for workload such as a web server and balance between campute(cpu) , memory , disk , networking .. for example t2
2.Compute Optimzied: greate for high cpu procces for example high speed web server , machine learning , gaming server and more started with c (c5)
3.memory optimzed: fast performance for large data in memory application for exmaple databases , cache stores and ... started with R (R5)
4.storage optimzed: greate for storage task need highed space for saving data or highed speed for example redis , data wearhouse applications and more and started with i
naming:
m5.2xlarge

m: instance class
5: genration
xlarge: size within instance class



security group : 

fundamental of network security in aws and control how traffic allowed into or out of our ec2 instance 

security groups works with ip / port and protocol in ec2 instance and if 
instance 1 : have policy 1 ,2
instance 2: have policy 2
instance 2 and 1 can see each and communicate with each together 

security groups have 2 mode inbound and outbound


ec2 iam role: 

we can create and use role for ec2 for example if we want see iam list we can create role and give access iam read to role and attach role into ec2 instance and aws cli command work without any aws login 


for create role we go to iam and click on role and create role select ec2 for service and attach IAMReadOnlyAccess policy

create ec2 and in action select modify iam role use iam role create 

now if we connect to instance 

and use this command we see
```bash
aws iam list-users
```


ec2 instance storage:

ebs: elastic block stroage its use network driver not phisical drive its locked to an avalility zone 