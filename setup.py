from distutils.core import setup
setup(
    name = "CoronaBot",
    py_modules = ["JustIRC", "pypandoc", "miniflux", "timeloop"],
    version = "0.1.0",
    description = "An IRC bot for coronavirus reports, news search and other.",
    author = "Francesco Pham",
    author_email = "pham.francesco@gmail.com",
    url = "https://github.com/frankplus/coronavirus-irc-bot",
    download_url = "",
    keywords = ["irc", "event", "coronavirus", "bot"]
)
