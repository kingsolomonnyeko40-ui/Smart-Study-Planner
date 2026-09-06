import jwt

data = {
    "id": 1,
    "name": "Solomon"
}

secret = "Solomon@2026#Secure-JWT-Key-123456789"

encoded = jwt.encode(data, secret, algorithm="HS256")
print("Encoded token:")
print(encoded)

decoded = jwt.decode(encoded, secret, algorithms=["HS256"])
print("\nDecoded data:")
print(decoded)