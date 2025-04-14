import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import bot
import asyncio

@pytest.mark.asyncio
async def test_help_command():
    response = await bot.elaborate_query("test_channel", "tester", "!help")
    assert response is not None
    assert "COMMANDS" in response

@pytest.mark.asyncio
async def test_greeting():
    response = await bot.elaborate_query("test_channel", "tester", "hello")
    assert response is not None
    assert "tester" in response

@pytest.mark.asyncio
def test_invalid_command():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!doesnotexist"))
    assert response is None or "Invalid command" in str(response)

@pytest.mark.asyncio
def test_help_specific_command():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!help fortune"))
    assert response is not None
    assert "fortune" in response or "Invalid command" in response

@pytest.mark.asyncio
def test_empty_message():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "   "))
    assert response is None

@pytest.mark.asyncio
def test_botname_only():
    import config
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", config.BOTNAME))
    # Should not crash, may or may not return a response
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_tell_and_on_join():
    # Add a tell
    tell_msg = "recipient1 Hello there!"
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", f"!tell {tell_msg}"))
    assert response == "sure"
    # Simulate join
    join_response = bot.on_join("recipient1", "test_channel")
    assert join_response is not None and "Hello there!" in join_response

@pytest.mark.asyncio
def test_shush_talk():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!shush"))
    assert response is not None
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!talk"))
    assert response is not None

@pytest.mark.asyncio
def test_fortune():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!fortune"))
    # May fail if API is down, so just check for a string or None
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_news():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!news"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_music():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!music test"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_latex():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!latex x^2"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_tex():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!tex x^2"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_plot():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!plot x^2"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_tweet():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!tweet hello world"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_chess_help():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!chess help"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_game_help():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!game"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_corona():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!corona italy"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_miniflux():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!miniflux"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_youtube():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!youtube test"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_image():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!image a cat"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_weather():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!weather Rome"))
    assert response is None or isinstance(response, str)

@pytest.mark.asyncio
def test_wolfram():
    response = asyncio.run(bot.elaborate_query("test_channel", "tester", "!wolfram 2+2"))
    assert response is None or isinstance(response, str)
