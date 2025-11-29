import requests

url = "https://api-transcriptor.vercel.app/"
file_path = r"C:\raule.mp3"  # Cambia a la ruta real de tu archivo

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Response:", response.json())
