import fitz
import re
from tqdm import tqdm
import openai
import urllib
import os
import requests
import urllib.request
from moviepy.editor import *
from moviepy.audio.io.AudioFileClip import AudioFileClip
from glob import glob

book_path='C:/Git/PDF_TO_VIDEO/main/pdf/oldmansea.pdf'

doc = fitz.open(book_path)
text = doc.get_page_text(3)

print(text)

# chat gpt 4 maximum tokens 8192 token
# chat gpt 3.5 maximum tokens 4,096 token
# calculate tokens : https://platform.openai.com/tokenizer
# page 4 tokens : 758
# about 5.4 tokens (gpt 3.5)
# standard 4

openai.organization = "org-7uWFzLJQRf3Zd7qG0v8K7c8n"
openai.api_key = 'my key'

start_pno =2
summarize_every = 4
summary_list = [{
    'role': 'system',
    'content': 'You are a helpful assistant for summarizing books.'
}]

count = 0
content = ''

for pno in tqdm(range(start_pno, doc.page_count)):
    text = doc.get_page_text(pno=pno)

    # Preprocess text
    text = re.sub(r"\s+", " ", text)
    text = text.replace('Asiaing.com', '').strip()
    text = text.replace('www.', '').strip()

    # Remove page number
    text = ' '.join(text.split(' ')[:-1])

    if count == summarize_every:
        messages = [{
            'role': 'system',
            'content': 'You are a helpful assistant for summarizing books.'
        }, {
            'role': 'user',
            "content": f"Summarize this: {content}",
        }]

        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        msg = res['choices'][0]['message']['content']

        summary_list.append({
            'role': 'user',
            'content': msg
        })

        count = 0
        content = ''
    else:
        content += text + ' '
        count += 1


os.makedirs('temp', exist_ok=True)

for i, summary in tqdm(enumerate(summary_list)):
    if summary['role'] != 'user':
        continue
    print("prompt text::")
    print({summary["content"][-350:]})

    res_img = openai.Image.create(
        prompt=f'book illustration, {summary["content"][-350:]}',
        n=1,
        size='512x512'
    )

    img_url = res_img['data'][0]['url']
    img_path = f'temp/{str(i).zfill(3)}.png'

    urllib.request.urlretrieve(img_url, img_path)

summary_list.append({
    'role': 'user',
    'content': '위 문장들을 60초 발표 분량으로 요약해줘'
})

res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=summary_list
)

script = res['choices'][0]['message']['content']

print(script)


messages = [{
    'role': 'system',
    'content': 'You are a helpful assistant for summarizing and translating books.'
}, {
    'role': 'user',
    'content': f'한국어로 번역해줘: {script}'
}]

res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

script_ko = res['choices'][0]['message']['content']

print(script_ko)

# script_ko =" \"The Old Man and the Sea\"은 낚시꾼인 노인이 물고기를 잡기 위해 투쟁하는 이야기입니다. 그는 드디어 거대한 말린을 낚지만, 상어들의 공격 으로 인해 바다로 돌아가기 전에 말린은 파괴됩니다. 노인은 그의 여정 과 삶의 단순함에 대해 생각하며, 물고기의 머리를 남기고 제자에게 미 래의 낚시 여행을 위한 좋은 살육 창을 가져오도록 지시합니다. 책은 관광객들이 항구에서 말린의 시체를 발견하는 장면으로 끝납니다."
url = "https://api.d-id.com/talks"

payload = {
    "script": {
        "type": "text",
        "provider": {
            "type": "microsoft",
            "voice_id": "ko-KR-BongJinNeural", # 음성 종류
        },
        "ssml": "false",
        "input": script_ko # 스크립트
    },
    "config": {
        "fluent": "false",
        "pad_audio": "0.0"
    },
    # "source_url": "https://i.imgur.com/AkrJpZb.png" # 아바타 이미지 URL
    "source_url": "https://i.ibb.co/zrmV28v/jesus1.png" # 아바타 이미지 URL
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoidGFsa3MiLCJpc3MiOiJodHRwczovL2F1dGguZC1pZC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDU0MzAwMjg3MDg4NTQyMDEzMjgiLCJhdWQiOlsiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2ODE4MzgwMDYsImV4cCI6MTY4MTkyNDQwNiwiYXpwIjoiR3pyTkkxT3JlOUZNM0VlRFJmM20zejNUU3cwSmxSWXEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIHJlYWQ6Y3VycmVudF91c2VyIHVwZGF0ZTpjdXJyZW50X3VzZXJfbWV0YWRhdGEgb2ZmbGluZV9hY2Nlc3MifQ.E8qhrn7SO8WC09oFaGE2V9i97JgUxPyXBIycHsDLuhqirI4aVM3XG2_q-CanVmnWCa8f5ERDaiKFC5uRXL3tgIzqxVbbqePXvgyY8Ce9UHOGyVaIOm5sEzcOThcvYHLV_GmPxngYRphx5mYt87ILzGUZ-41DUaGJcwdHGiqeYdkfsebmvWwzc_2w5jIMlLntMLZQnJWCqwTjU9io7ZTWpHYTsS6A1pwT8tOEZ6sVLE0KKeUIcCRBO4Gu17d_Wi849ezMCxpSCj-Iic7dialFuCqJhEpbXQWCSOGLBxGM4qDM89KI1oSm1PxG-Nt8GP10bmqaQ5rf2NDXPiqGLnzy_Q"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

# After about 60s (debug - wait 60sec) - generating

url = f"https://api.d-id.com/talks/{response.json()['id']}"

headers = {
    "accept": "application/json",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoidGFsa3MiLCJpc3MiOiJodHRwczovL2F1dGguZC1pZC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDU0MzAwMjg3MDg4NTQyMDEzMjgiLCJhdWQiOlsiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2ODE4MzgwMDYsImV4cCI6MTY4MTkyNDQwNiwiYXpwIjoiR3pyTkkxT3JlOUZNM0VlRFJmM20zejNUU3cwSmxSWXEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIHJlYWQ6Y3VycmVudF91c2VyIHVwZGF0ZTpjdXJyZW50X3VzZXJfbWV0YWRhdGEgb2ZmbGluZV9hY2Nlc3MifQ.E8qhrn7SO8WC09oFaGE2V9i97JgUxPyXBIycHsDLuhqirI4aVM3XG2_q-CanVmnWCa8f5ERDaiKFC5uRXL3tgIzqxVbbqePXvgyY8Ce9UHOGyVaIOm5sEzcOThcvYHLV_GmPxngYRphx5mYt87ILzGUZ-41DUaGJcwdHGiqeYdkfsebmvWwzc_2w5jIMlLntMLZQnJWCqwTjU9io7ZTWpHYTsS6A1pwT8tOEZ6sVLE0KKeUIcCRBO4Gu17d_Wi849ezMCxpSCj-Iic7dialFuCqJhEpbXQWCSOGLBxGM4qDM89KI1oSm1PxG-Nt8GP10bmqaQ5rf2NDXPiqGLnzy_Q"
}

response = requests.get(url, headers=headers)

print(response.text)

urllib.request.urlretrieve(response.json()['result_url'], 'temp/avatar.mp4') 

# !ffmpeg -hide_banner -loglevel error -i temp/avatar.mp4 -s 170x170 -c:a copy temp/avatar170.mp4

avatar_clip = VideoFileClip('temp/avatar.mp4')

print(avatar_clip.duration)

# audio_clip = AudioFileClip('temp/bgm.mp3')

# audio_clip = audio_clip.volumex(0.2)
# audio_clip = audio_clip.set_duration(avatar_clip.duration)

# print(audio_clip.duration)

paper_imgs = sorted(glob('temp/*.png'))
print(len(paper_imgs))

clips = [ImageClip(m).set_duration(avatar_clip.duration / len(paper_imgs)) for m in paper_imgs]

paper_clip = concatenate_videoclips(clips, method="compose")

paper_clip = paper_clip.set_duration(avatar_clip.duration)

print(paper_clip.duration)

w, h = paper_clip.size

print('Resize avatar clip and move position to bottom right')
avatar_clip = avatar_clip.set_pos(('right', 'bottom'))

print('Text animation')
txt = TextClip("The Old Man and the Sea", color='white', fontsize=30)
txt_col = txt.on_color(
    size=(txt.w + 10, txt.h + 10),
    color=(0, 0, 0),
    pos=(6, 'center'),
    col_opacity=0.6)
txt_mov = txt_col.set_pos(('center', h / 10))
txt_mov = txt_mov.set_duration(avatar_clip.duration)

print('Composite and write the video file')
result = CompositeVideoClip([paper_clip, avatar_clip, txt_mov])
# audios = CompositeAudioClip([avatar_clip.audio, audio_clip])
# result = result.set_audio(audios)

result.write_videofile(
    'result.mp4',
    temp_audiofile='temp/audio.m4a',
    remove_temp=True,
    codec='libx264',
    audio_codec='aac',
    threads=32)