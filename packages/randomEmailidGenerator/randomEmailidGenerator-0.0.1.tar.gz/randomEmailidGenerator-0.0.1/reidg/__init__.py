import random, string, sys

'''
  Author: Pranay Bankar
  Version: 0.0.1

'''

''' 
  This library will help you to generate ramdom email ids on the basis of 
  numbers you provide as arguments to the script.
  Syntax:
    python ./reidg/__init__.py number emailProvider
  For example: 
  Input: python ./reidg/__init__.py 898 yopmail.com
  Output: 
    Number of emails to generate: 3
    wmNQxNIGyopmail.com
    FnkYCKdVYyopmail.com
    dYEcEygoyopmail.com
'''

'''
  Get the list of integers from provided number argument.
'''
def convert_to_list(number):
    try:
       return [int(x) for x in str(number)]
    except Exception as e:
        print(e)

'''
  Print the randomly generated email id for the count of number argument and email provider.
'''
def random_char(num_list, email_provider):
    try:
        for num in num_list:
            print(''.join(random.choice(string.ascii_letters) for x in range(num)) +email_provider)
    except Exception as e:
        print(e)

'''
  Entry method
'''
def main():
  argument = sys.argv
  email_provider = argument[2]
  numb = argument[1]
  print("Number of emails to generate: " + str(len(str((numb)))))
  
  
  list_of_num = convert_to_list(numb)
  random_char(list_of_num, email_provider)

'''
  Entry point
'''
if __name__ == "__main__":
	main()