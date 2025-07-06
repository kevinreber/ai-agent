# AI Code Assistant

An AI-powered coding assistant that can help you with file operations, code execution, and development tasks using Google's Gemini AI model.

## Features

- **File Operations**: List files, read file contents, write files
- **Code Execution**: Run Python files with proper output capture
- **Security**: All operations are constrained to a working directory for safety
- **Interactive**: Multi-turn conversations with function calling capabilities

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

## Usage

### Basic Usage

```bash
# Using uv
uv run main.py "your prompt here"

# Using python
python main.py "your prompt here"
```

### Examples

#### List files in the working directory

```bash
uv run main.py "what files are in the calculator directory?"
```

#### Read file contents

```bash
uv run main.py "get the contents of main.py"
```

#### Run a Python file

```bash
uv run main.py "run tests.py"
```

#### Write a new file

```bash
uv run main.py "create a new README.md file with the contents '# My Project'"
```

#### Verbose mode (for debugging)

```bash
uv run main.py "run tests.py" --verbose
```

### Working Directory

The application operates within a `calculator` directory by default. All file operations are constrained to this directory for security.

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
