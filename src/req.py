import requests


api_url = "http://127.0.0.1:8000/api/postview/7/"


image_path = "C:\\Users\\kurin\\Documents\\Instagrams\\media\\image\\image1.jpg"

json_data = {"user": 3, "caption": "hhde"}
response = requests.patch(api_url, data=json_data)


# with open(image_path, "rb") as file:

#     files = {"image": file}

#     json_data = {"user": 1}
#     response = requests.post(api_url, files=files, data=json_data)

# print(response.content)
