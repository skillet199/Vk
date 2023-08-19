import requests
import vk_api
token = 'vk1.a.vzGHXwnVgSOkUjAsWO_3q98tgAfV-u5BZv9rH2hMpwawPPw-ACEox4zobzdy2PDZcoicivaqOUPIZXl5qW0nziixivkUCkrodWGwfxU1og_ZrwVR-cYkGD_a1dOfUQFkxvSBmyz1p5nGjG_ZRPnSFa5Z2szYCtmQrM6OSGJennRmwPZ6ZSZ3Q3jNOTf0_2W-'
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
message = 'ку ку'
r = requests.post(f"https://api.vk.com/method/messages.send?peer_id=19231794&message=test&access_token={token}&v=5.82")
answer = r.json()
print(answer)
#print(vk.messages.send(user_id=19231794, message='ку ку', access_token=token))
