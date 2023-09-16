import requests


def instagram_photos_context(request):
    access_token = 'Замените на ваш access token'  

    api_url = f'https://graph.instagram.com/me/media?fields=media_url,thumbnail_url,caption&access_token={access_token}&limit=6'
    response = requests.get(api_url)
    data = response.json()

    # Отфильтровать данные, чтобы получить только фотографии
    instagram_photos = [post for post in data.get('data', [])
                        if 'media_url' in post and not post['media_url'].endswith('.mp4')]

    return {'instagram_photos': instagram_photos}
