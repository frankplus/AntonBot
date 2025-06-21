# Improved Function Calling Architecture

## Overview

The bot has been enhanced with a more scalable and readable function calling system that leverages the existing PluginBot infrastructure. This improvement separates concerns and makes it easier to add new OpenAI function calling capabilities.

## Key Improvements

### 1. Centralized Function Management
- All function registrations are now handled through the `PluginBot` class
- Functions are registered alongside commands in the same plugin registration process
- No need to manually import and register functions in `apis.py`

### 2. Plugin-Based Function Registration
Each plugin can now register both commands and OpenAI functions:

```python
def register(bot):
    # Register command for direct use
    bot.register_command('mycommand', handler_function)
    bot.register_help('mycommand', 'Help text for mycommand')
    
    # Register function for OpenAI function calling
    bot.register_function(my_function, MY_FUNCTION_DEFINITION)
```

### 3. Backward Compatibility
The system maintains backward compatibility with existing code through:
- Legacy function loading method as fallback
- Optional plugin_bot parameter in Chatbot constructor

## Architecture Changes

### PluginBot Class Enhancements
- Added `available_functions` dictionary to store function handlers
- Added `function_definitions` list to store OpenAI function definitions
- Added `register_function()` method for plugins to register functions
- Added getter methods for function definitions and handlers

### Chatbot Class Updates
- Constructor now accepts optional `plugin_bot` parameter
- Uses plugin_bot's functions when available, falls back to legacy loading
- Cleaner separation between chat logic and function management

### Plugin Registration
Plugins now register functions using:
```python
bot.register_function(function_handler, function_definition)
```

## Example Plugin Structure

```python
def my_api_function(param1, param2):
    """Function that can be called by OpenAI"""
    return "result"

# OpenAI function definition
MY_FUNCTION_DEFINITION = {
    "type": "function",
    "name": "my_api_function",
    "description": "Description of what the function does",
    "parameters": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Description of param1"
            },
            "param2": {
                "type": "string", 
                "description": "Description of param2"
            }
        },
        "required": ["param1", "param2"],
        "additionalProperties": False
    },
    "strict": True
}

def register(bot):
    # Register both command and function
    bot.register_command('mycommand', lambda c, s, q: my_api_function(q, "default"))
    bot.register_help('mycommand', '!mycommand <param> - Does something useful')
    bot.register_function(my_api_function, MY_FUNCTION_DEFINITION)
```

## Benefits

1. **Scalability**: Easy to add new functions without modifying core files
2. **Readability**: Function definitions are co-located with their implementations
3. **Maintainability**: Single registration point per plugin
4. **Consistency**: Same pattern for all plugins
5. **Flexibility**: Plugins can register commands, functions, or both

## Migration Guide

For existing plugins that want to add OpenAI function calling:

1. Define your function and its OpenAI definition in the plugin
2. Add `bot.register_function(handler, definition)` to your register() function
3. The function will automatically be available for OpenAI function calling

The legacy manual registration in `apis.py` is still supported but deprecated for new functions.
