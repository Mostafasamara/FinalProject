import bcrypt

password = input("Enter the password to hash: ")
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print("Hashed Password:", hashed.decode('utf-8'))
