import os
import openai
import urllib
import urllib.request
openai.organization = "org-7uWFzLJQRf3Zd7qG0v8K7c8n"
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = 'my key'
# print(openai.Model.list())

# openai.api_key = 'my key'

# messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "hi who are you?"},
# ]

# res = openai.ChatCompletion.create(
#     engine="gpt-3.5-turbo",
#     messages=messages,
#     max_tokens=50
# )

# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=messages
# )

# print(completion.choices[0].message)
num = 0
texts = ["Dear my 17-year-old self, I know you are now struggling with your new freshman year. You sometimes feel stressed out because you wake up early every morning and take tough classes. You may occasionally feel that you are not important. However, everything will get better. Here are some ways to live more positively through this year. You will have realized by the time you are 27 that the following tips were really important to you. I can remember you are a huge fan of some soccer players and singers. Following their lives is okay if it helps you relax. But you also need to become a fan of yourself. It doesn't mean your favorite celebrities aren't important. But someday you will suddenly feel that focusing on yourself is more important than focusing on them. So I suggest that you keep a healthy life balance. Become a bigger fan of yourself than people on TV or the Internet.","Yesterday, I recommended that your brother not care too much about how many friends he has. Not having many friends doesn't mean anything is wrong. Friends are about quality, not quantity. Do not care about the number of your friends or SNS friends. If you care too much about that, you will end up wasting time with negative friendships. True friends help you understand and love yourself. They focus on your strengths and try to help you with your problems. I know it's hard to believe, but not all your friends at 17 will be your friends at 27. Thankfully, your \"true\" friends will still be with you. So spend more time with them and be the best friend you can be to them.","There's something else. Stop thinking so much about the future! In your classes, you have trouble focusing, don't you? Your mind is in the future, worrying about the next exam or your future job. Thinking about the future is important, but you also need to focus on the present moment. You are wasting your precious present time! A Chinese proverb says, \"If you want to know your past, look into your present conditions, and if you want to know your future, look into your present actions.\" To achieve your goals, you need to do more than just dream about them. So take action now, and in ten years you will have achieved your goals.","Lastly, don't just go through your high school days with a negative attitude. Stay positive. Having a good attitude will help you keep your spirits up when things don't go your way in life. Live and enjoy every moment. I can tell you that right now is not only a very challenging time for you, but it is also a very fun time. Thank you and I look forward to writing you another letter when you are 27.Love always, your future self P.S. Please tell your family you love them. And don't forget that your parents' advice comes from their love for you."," From the bottom of my heart, I welcome you to your new school. On behalf of the entire school faculty, I'd like to congratulate every one of you and share with you some words that I think are important for students who've just started their high school life. First, try to live a healthy school life and work hard to build up your physical and mental strength. A healthy body and mind will give you confidence and self-esteem. Second, work on improving your social skills. Specifically, I'd like to emphasize the importance of language skills. I believe conveying your ideas to others in a clear, effective way is really important, and that's something you should focus on developing during your high school period. Third, learn the value of respecting other people's views. Every one of you is unique and has a special perspective on life. Understand that somebody may think differently than you, but that doesn't mean that they're wrong. Try to see things from different perspectives to help broaden your own view. You will have incredible experiences for the next three years. Some of them will be sweet, but some of them will be bitter. But I believe all those experiences will be a great asset for your future. Teachers, friends, and family will always be by your side. I wish you the best. Thank you."]
os.makedirs('temp1', exist_ok=True)
for i in texts:
    print("\n\n\n")
    print(i)
    res_img = openai.Image.create(
        prompt=f'book illustration, {i}',
        n=1,
        size='512x512'
    )

    img_url = res_img['data'][0]['url']
    img_path = f'temp1/{num}.png'
    num = num+1
    urllib.request.urlretrieve(img_url, img_path)



