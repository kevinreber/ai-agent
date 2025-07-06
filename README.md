# AI Code Assistant

An AI-powered coding assistant that can help you with file operations, code execution, and development tasks using Google's Gemini AI model. Features an interactive conversation mode that maintains context across multiple prompts.

## Features

- **Interactive Conversations**: Chat with the AI agent with full context awareness
- **File Operations**: List files, read file contents, write files
- **Code Execution**: Run Python files with proper output capture
- **Security**: All operations are constrained to a working directory for safety
- **Context Memory**: The agent remembers your conversation history and can reference previous actions
- **Conversation Limits**: Configurable prompt limit (default: 20) to manage resource usage

## Requirements

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Dependencies

- `google-genai` - Google's Gemini AI client
- `python-dotenv` - Environment variable management

## Installation

### Option 1: Using uv (Recommended)

1. **Install uv** (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

3. **Install dependencies**:

   ```bash
   uv sync
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

### Option 2: Using Python/pip

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

## Configuration

1. **Get a Gemini API key**:

   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key

2. **Configure environment variables**:
   Create a `.env` file in the project root:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Optional: Adjust conversation limits**:
   Edit `config.py` to change:
   ```python
   MAX_ITERS = 20  # Maximum prompts per conversation
   MAX_CHARS = 10000  # Maximum characters to read from files
   WORKING_DIR = "./calculator"  # Working directory
   ```

## Usage

### Interactive Mode (Recommended)

Start an interactive conversation:

```bash
# Using uv
uv run main.py

# Using python
python main.py
```

This starts an interactive chat where you can:

- Ask questions and get responses
- Make follow-up requests that build on previous context
- Use special commands to manage the conversation

### Single Command Mode

Run a single command and exit:

```bash
# Using uv
uv run main.py "your prompt here"

# Using python
python main.py "your prompt here"
```

### Interactive Commands

When in interactive mode, you can use these special commands:

- `quit`, `exit`, or `bye` - End the conversation
- `clear` - Start a new conversation (clears context)
- `help` - Show help information

### Examples

#### Interactive Conversation

```bash
$ uv run main.py

🤖 AI Code Assistant
Type 'quit', 'exit', or 'bye' to end the conversation
Type 'clear' to start a new conversation
Type 'help' for usage information
--------------------------------------------------

You: What files are in the calculator directory?
Assistant: Let me check what files are in the calculator directory...

You: Can you read the contents of main.py?
Assistant: I'll read the contents of main.py for you...

You: What was the output when we ran the tests?
Assistant: Based on our previous conversation, when we ran the tests, the output was...
```

#### Single Commands

```bash
# List files
uv run main.py "what files are in the calculator directory?"

# Read file contents
uv run main.py "get the contents of main.py"

# Run a Python file
uv run main.py "run tests.py"

# Write a new file
uv run main.py "create a new README.md file with the contents '# My Project'"

# Verbose mode (for debugging)
uv run main.py "run tests.py" --verbose
```

### Working Directory

The application operates within a `calculator` directory by default. All file operations are constrained to this directory for security.

## Conversation Features

### Context Awareness

- The agent remembers all previous interactions in a conversation
- You can ask follow-up questions like "What was the output of the last command?"
- The agent can reference files you've read, commands you've run, or files you've created
- You can build on previous work - create a file, then read or modify it

### Conversation Management

- **Automatic limit**: Conversations are limited to 20 prompts by default
- **Manual clearing**: Use `clear` command to start fresh
- **Graceful exit**: Use `quit`, `exit`, or `bye` to end conversations
- **Auto-restart**: When the limit is reached, a new conversation starts automatically

### Example Conversation Flow

```
You: What files are in the directory?
Assistant: [Lists files]

You: Read the main.py file
Assistant: [Shows file contents]

You: What was in that file again?
Assistant: [References previous file read]

You: Run the tests
Assistant: [Executes tests]

You: What was the test output?
Assistant: [References previous test execution]
```

## Testing

### Run the test suite

```bash
# Using uv
uv run tests.py

# Using python
python tests.py
```

### Test individual functions

```bash
# Test file listing
uv run main.py "list files in the current directory"

# Test file reading
uv run main.py "read the contents of lorem.txt"

# Test Python execution
uv run main.py "run main.py"
```

## Project Structure

```
ai-agent/
├── main.py                 # Main application entry point
├── functions/              # Function implementations
│   ├── get_files_info.py   # List files and directories
│   ├── get_file_content.py # Read file contents
│   ├── run_python_file.py  # Execute Python files
│   └── write_file.py       # Write files
├── calculator/             # Working directory
│   ├── main.py            # Calculator application
│   ├── tests.py           # Test suite
│   ├── lorem.txt          # Sample text file
│   └── pkg/               # Package directory
├── config.py              # Configuration constants
├── prompts.py             # System prompts
├── call_function.py       # Function calling utilities
├── pyproject.toml         # Project configuration (uv)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Function Capabilities

### get_files_info

Lists files in a directory with size and type information.

- **Parameters**: `directory` (optional)
- **Returns**: Formatted list of files with metadata

### get_file_content

Reads file contents with truncation for large files.

- **Parameters**: `file_path`
- **Returns**: File content (truncated at 10,000 characters if needed)

### run_python_file

Executes Python files with output capture.

- **Parameters**: `file_path`, `args` (optional)
- **Returns**: STDOUT, STDERR, and exit code information

### write_file

Writes content to files within the working directory.

- **Parameters**: `file_path`, `content`
- **Returns**: Success/error message

## Security Features

- **Path validation**: All file operations are constrained to the working directory
- **Directory traversal protection**: Prevents access to files outside the permitted area
- **File type validation**: Ensures only appropriate files are accessed
- **Timeout protection**: Prevents infinite execution loops
- **Conversation limits**: Prevents resource exhaustion from long conversations

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not found"**

   - Ensure your `.env` file exists and contains the API key
   - Check that the key is valid and has proper permissions

2. **"Function not found"**

   - Verify all function files are present in the `functions/` directory
   - Check that function schemas are properly defined

3. **"Permission denied"**

   - Ensure the working directory has proper read/write permissions
   - Check that files aren't locked by other processes

4. **"Timeout error"**

   - Python file execution is limited to 30 seconds
   - Check for infinite loops in your Python code

5. **"Maximum conversation length reached"**
   - The conversation limit (20 prompts) has been reached
   - A new conversation will start automatically, or use `clear` to start fresh

### Debug Mode

Use the `--verbose` flag to see detailed information about function calls and responses:

```bash
uv run main.py "your prompt" --verbose
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
