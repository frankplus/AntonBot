from lib.apis import plot_function

def register(bot):
    bot.register_command('plot', lambda channel, sender, query: plot_function(query) if query else None)
    bot.register_help('plot', '!plot <query> to plot any mathematical function.')
