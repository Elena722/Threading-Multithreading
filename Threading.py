'''
Simulate multiple users signing up to your application at the same time.

Create a function create_user which returns a dict of dummy user info. Every time we call this function,
it should return a different dummy user info.

Example: {“name”: “Xavier Kapastulus”, “email”: “xavier@mars.com”, “password”: “super_secret_password”}

Create another function send_welcome_email which takes a single parameter email. This function should sleep
for a random number of seconds between 1 and 5, then log “sending email to [email]”

Use a loop to create 20 users (log “Create new user with info [generated user info]“), each time sending them
a welcome email on a different thread.
*Use a thread pool of max size 3.
'''
import time
import random
import logging
import concurrent.futures

l = logging.getLogger()
l.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.INFO)
h.setFormatter(logging.Formatter('%(message)s'))
l.addHandler(h)

emails = []
user_info = []
def create_user(user_info):
    x = 1
    while x:
        user = random.choice(user_info)
        if user['email'] not in emails:
            emails.append(user['email'])
            send_welcome_email(user['email'])
            x = 0
        else:
            x = 1
        # return user

def send_welcome_email(email):
    time.sleep(random.randint(1, 5))
    logging.info(f'sending email to {email}')

if __name__=='__main__':
    for _ in range(4):
        name = input('Enter name: ')
        email = input('Enter email: ')
        password = input('Enter password: ')
        user_info.append({'name': name, 'email': email,'password': password})

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # executor.submit(send_welcome_email, emails)
        for _ in range(len(user_info)):
            executor.submit(create_user, user_info)
        # executor.map(create_user, user_info)


# OR USING RANDOMUSER
# from randomuser import RandomUser
# import time
# import random
# import concurrent.futures
#
# def create_user():
#     user = RandomUser()
#     print(user.get_full_name())
#
#     print(f'Created {user.get_first_name()}')
#
#     return {
#         'name': user.get_first_name(),
#         'email': user.get_email(),
#         'password': user.get_password()
#     }
#
# def send_welcome_email(email):
#     time.sleep(random.randint(1, 5))
#     print(f'Sending welcome email to {email}')
#
# if __name__=='__main__':
#     new_users = (create_user() for i in range(20))
#     # print(new_users)
#     for user in new_users:
#         print(user)
#
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         executor.submit(send_welcome_email, new_users)