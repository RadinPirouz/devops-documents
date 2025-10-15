import redis

method=int(input("Enter Method: (1.Read/2.Write): "))

r = redis.Redis(host="ip", port=6379,db=0)


if (method == 1):
    key=str(input("enter key name: "))
    value=r.get(key)
    if value == None:
        print("Undefined Key")
        exit
    else:
        print(value.decode('utf-8'))
elif (method == 2):
    key=str(input("enter key name: "))
    value=str(input("enter value: "))
    r.set(key,value)
else:
    print("Incorrect Input")
    exit