# AntonBot

Welcome to AntonBot, a versatile and interactive chatbot designed to work seamlessly on both IRC and Telegram platforms. AntonBot is equipped with a wide array of features to provide users with real-time information, entertainment, and utilities through simple commands. Whether you're looking to stay updated on the latest news, check the weather, or just have some fun, AntonBot has something for everyone.

## Features

AntonBot supports a range of commands, each tailored to bring specific functionalities to your fingertips. Here's a quick rundown of what AntonBot can do for you:

- `!corona <location>`: Get the latest coronavirus report for the specified location.
- `!news <query>`: Search for the latest news related to your query.
- `!weather <location>`: Receive a weather report for your specified location.
- `!youtube <query>`: Search YouTube for videos matching your query.
- `!image <prompt>`: Generate an image based on your prompt.
- `!music <query>`: Look up music videos on YouTube based on your query.
- `!latex <query>`: Compile LaTeX code into a PNG image.
- `!tex <query>`: Compile LaTeX code into Unicode text.
- `!game`: Get help with various game commands.
- `!chess`: Access help for engaging with the chessbot.
- `!wolfram <query>`: Calculate or ask any question, with answers powered by Wolfram Alpha.
- `!plot <query>`: Plot any mathematical function.
- `!tweet <message>`: Tweet a message directly from the chat.
- `!fortune`: Discover your fortune with this fun command.
- `!shush`: Silence the chatbot if it's being too chatty.
- `!talk`: Encourage the chatbot to participate in conversations.
- `!tell <recipient> <message>`: Have the chatbot deliver a message to a recipient when they join the channel.

Additionally, AntonBot is designed to engage in group chats like a friend. Simply ping (mention) the chatbot, and it will respond, participating in conversations with the flair of a human companion.

### Additional Capabilities

- **URL Content Preview**: AntonBot automatically scans messages for URLs and provides a concise summary or preview of the content, helping users get a quick understanding of the linked material without needing to click through.
  
- **RSS Feed Updates**: Leveraging Miniflux, AntonBot seamlessly integrates the latest updates from your favorite RSS feeds directly into the chat. Stay informed with real-time news and content from a wide range of sources, all curated and delivered by AntonBot for your convenience.

## Getting Started 

Follow the detailed steps below to install and run AntonBot on your preferred platform. Whether you're aiming to engage with users on IRC or to enhance your Telegram chat experiences, AntonBot is equipped to deliver.

### Installation Steps

To install AntonBot, execute the following commands in your terminal. These steps will clone the repository, set up a virtual environment, and install all necessary dependencies to get AntonBot up and running.

```bash
git clone https://github.com/frankplus/AntonBot.git
cd AntonBot
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

**Configuration:** Before launching AntonBot, make sure to configure it according to your needs. Open `config.py` to set up your IRC configurations and enter the required API keys. This step is crucial for ensuring that AntonBot functions correctly on your platform and can access all its features.

### Running AntonBot

Depending on where you want to deploy AntonBot, follow the corresponding instructions below:

- **For IRC**: Launch the IRC version of AntonBot by running:
  ```bash
  python3 ircbot.py
  ```
- **For Telegram**: Start the Telegram bot with the following command:
  ```bash
  python3 telegrambot.py
  ```
- **Testing**: If you'd like to test AntonBot's functionalities before deploying, run:
  ```bash
  python3 test.py
  ```

This will initiate the bot in a test environment where you can verify its operations and ensure everything is set up correctly.

Congratulations! You've successfully set up AntonBot. It's now ready to assist, entertain, and inform your chat members across IRC and Telegram. Should you encounter any issues or have questions during the setup process, refer to the documentation or reach out for support.

## Usage

Using AntonBot is as simple as typing a command in the chat window. Commands should be prefixed with `!` and followed by the specific command you wish to use, along with any necessary arguments. For example, to get a weather report, you would type `!weather New York`.

## Feedback and Support

We're always looking to improve AntonBot and add more features based on user feedback. If you have suggestions, feedback, or need support, please reach out to us through our support channel or GitHub repository.

## Contribute

Interested in contributing to AntonBot? We welcome contributions of all kinds, from code improvements to documentation. Visit our GitHub repository to see how you can contribute and become part of the AntonBot development community.

Thank you for choosing AntonBot. We hope you enjoy using it as much as we enjoyed creating it!


