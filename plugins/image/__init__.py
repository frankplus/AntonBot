from openai import OpenAI
import config

def generate_image(prompt):

    client = OpenAI(api_key=config.CHATGPT_KEY)

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return response.data[0].url

def register(bot):
    bot.register_command('image', lambda channel, sender, query: generate_image(query) if query else None)
    bot.register_help('image', '!image <prompt> to generate an image.')
