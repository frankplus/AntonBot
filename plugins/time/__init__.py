import datetime

def get_current_time(timezone="UTC"):
    """Get current time in UTC (simplified version without timezone support)"""
    current_time = datetime.datetime.utcnow()
    return current_time.strftime("%Y-%m-%d %H:%M:%S UTC")

# OpenAI function definition
TIME_FUNCTION_DEFINITION = {
    "type": "function",
    "name": "get_current_time", 
    "description": "Get the current time in UTC. Useful for answering questions about what time it is.",
    "parameters": {
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "Timezone parameter (currently only UTC is supported)"
            }
        },
        "required": ["timezone"],
        "additionalProperties": False
    },
    "strict": True
}

def register(bot):
    # Register command for direct use
    bot.register_command('time', lambda _channel, _sender, query: get_current_time(query if query else "UTC"))
    bot.register_help('time', '!time [timezone] - Get current time in specified timezone (default: UTC)')
    
    # Register function for OpenAI function calling
    bot.register_function(get_current_time, TIME_FUNCTION_DEFINITION)
