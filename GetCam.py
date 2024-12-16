import requests
import time,os

def fetch_and_save_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check if the request was successful
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the image: {e}")

# Example usage
image_url = 'http://127.0.0.1:8000/capture'
proxies = {
    "http": "http://your_proxy_address:your_proxy_port",
    "https": "http://your_proxy_address:your_proxy_port",
}
while True:
    save_path = f'local_image_{int(time.time())}.jpg'
    fetch_and_save_image(image_url, save_path)
    image_size_kb = os.path.getsize(save_path) / 1024
    print(f"Image size: {image_size_kb:.2f} KB")
    time.sleep(1)
   