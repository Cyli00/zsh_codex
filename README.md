## What is it?

This is a ZSH plugin that enables you to use AI powered code completion in the command line.

## How do I install it?

### Manual Installation

1. Install the OpenAI package, the Google package, or boto3.

```bash
pip3 install openai
```

or

```bash
pip3 install google-generativeai
```

or

```bash
pip3 install boto3
```

2. Download the ZSH plugin.

```bash
# mkdir ~/.zsh
cd ~/.zsh
git clone https://github.com/tom-doerr/zsh_codex.git
```

3. Add the following to your `.zshrc` file.

```bash
source "~/.zsh/zsh_codex/zsh_codex.plugin.zsh"
```

4. Configure the plugin by setting environment variables in your `.zshrc` file or '~/.zsh/zsh_codex/zsh_codex.plugin.zsh'.
   You need to set `CODEX_SERVICE_TYPE` to specify which AI provider to use. Then, set the required environment variables for that provider.

   **Common Environment Variables:**
    - `CODEX_SERVICE_TYPE`: Specifies the AI service to use (e.g., "openai", "gemini", "groq", "mistral", "bedrock").

   **Provider-Specific Environment Variables:**

   **OpenAI:**
   ```bash
   export CODEX_SERVICE_TYPE="openai"
   export OPENAI_API_KEY="your_openai_api_key"
   # Optional:
   # export OPENAI_MODEL="gpt-4.1-mini"
   # export OPENAI_BASE_URL="https://api.openai.com/v1" # For self-hosted or proxy
   # export OPENAI_TEMPERATURE="0"
   ```

   **Google Gemini:**
   ```bash
   export CODEX_SERVICE_TYPE="gemini"
   export GEMINI_API_KEY="your_gemini_api_key"
   # Optional:
   # export GEMINI_MODEL="gemma-3-27b-it"
   ```

   **Groq:**
   ```bash
   export CODEX_SERVICE_TYPE="groq"
   export GROQ_API_KEY="your_groq_api_key"
   # Optional:
   # export GROQ_MODEL="llama-3.2-11b-text-preview" # Check Groq for latest models
   # export GROQ_TEMPERATURE="0"
   ```

   **Mistral AI:**
   ```bash
   export CODEX_SERVICE_TYPE="mistral"
   export MISTRAL_API_KEY="your_mistral_api_key"
   # Optional:
   # export MISTRAL_MODEL="codestral-latest" # Check Mistral for latest models
   # export MISTRAL_TEMPERATURE="0"
   ```

   **Amazon Bedrock:**
   ```bash
   export CODEX_SERVICE_TYPE="bedrock"
   # All Bedrock variables are optional if your AWS CLI/SDK environment is already configured
   # (e.g., via ~/.aws/credentials, IAM roles, or other AWS environment variables).
   # export BEDROCK_AWS_REGION="your_aws_region"
   # export BEDROCK_AWS_ACCESS_KEY_ID="your_aws_access_key_id" # Only if not configured elsewhere
   # export BEDROCK_AWS_SECRET_ACCESS_KEY="your_aws_secret_access_key" # Only if not configured elsewhere
   # export BEDROCK_AWS_SESSION_TOKEN="your_aws_session_token" # If using temporary credentials
   # export BEDROCK_MODEL="anthropic.claude-3-5-sonnet-20240620-v1:0" # Example, check Bedrock for available models
   # export BEDROCK_TEMPERATURE="0"
   ```
   Add the chosen export lines to your `.zshrc` file and ensure you replace placeholder values like `<your_openai_api_key>` with your actual keys. The available models and other parameters for each `api_type` are detailed in `services/services.py`.

5. Run `source ~/.zshrc` or open a new terminal session. Start typing a command or comment and complete it using `Ctrl+X` (`^X`)!

6. If you use virtual environments you can set `ZSH_CODEX_PYTHON` in `zsh_codex.plugin.zsh` or `~/.zshrc` to python executable where `openai` or `google-generativeai` is installed.

```bash
conda activate your_env
which python3 # for windows -> where python3
export ZSH_CODEX_PYTHON=$(which python3)
```

## Passing in context

Since the current filesystem is not passed into the ai you will need to either
1. Pass in all context in your descriptive command
2. Use a command to collect the context

In order for option 2 to work you will need to first add `export ZSH_CODEX_PREEXECUTE_COMMENT="true"` to your .zshrc file to enable the feature. 

> [!WARNING]
> This will run your prompt using zsh each time before using it, which could potentially modify your system when you hit ^X.

Once you've done that and restarted your shell you can do things like this:

`# git add all files. Also commit the current changeset with a descriptive message based on $(git diff). Then git push`

[Fish Version](https://github.com/tom-doerr/codex.fish)

[Traffic Statistics](https://tom-doerr.github.io/github_repo_stats_data/tom-doerr/zsh_codex/latest-report/report.html)
