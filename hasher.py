from werkzeug.security import generate_password_hash

# Generate the hashed password
password = "mysecurepw"
hashed_password = generate_password_hash(password)

print("Hashed password:", hashed_password)