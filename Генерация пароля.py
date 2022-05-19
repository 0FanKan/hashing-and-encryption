import secrets, string

a = string.ascii_letters + string.digits
while True:
    password = "".join(secrets.choice(a) for i in range(10))
    if (any(c.islower() for c in password) and
        any(c.isupper() for c in password) and
        sum(c.isdigit() for c in password) > 2):
        break

print(password)