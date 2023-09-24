import requests

# POST метод должен создавать объявление
# response = requests.post("http://127.0.0.1:5000/advertisement",
#                          json={"article": "Фантастика нам только снится.",
#                                "description": "Статья о интересном "
#                                               "приключении одного героя",
#                                "owner": "Arhimed"})
# print(response.json())

# GET - получать объявление
# response = requests.get("http://127.0.0.1:5000/advertisement/1")
# print(response.json())

# PUT - обновить объявление
# response = requests.patch("http://127.0.0.1:5000/advertisement/1",
#                           json={
#                               "description": "Отважный герой борется с главным "
#                                              "врагом - Временем, отвоевывая у "
#                                              "него все новые и новые "
#                                              "способности. Он мечтает все "
#                                              "успеть."})
# print(response.json())
#
# # DELETE - удалять объявление.
response = requests.delete("http://127.0.0.1:5000/advertisement/1")
print(response.json())
