num1=float(input("Enter firdt number :"))
num2=float(input("Enter second number :"))
num3=float(input("Enter third number :"))
if(num1>num2 and num1>num3):
    print("greatest number num1:", num1)
elif(num2>num1 and num2>num3):
    print("greatest number is num2 :", num2)
else:
    print("greatesst number is num3 :", num3)
