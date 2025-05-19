import os
import sys
from abc import ABC, abstractmethod

class BaseClient(ABC):
    """Base class for all clients"""

    api_type: str = None
    system_prompt = "You are a zsh shell expert, please help me complete the following command, you should only output the completed command, no need to include any other explanation. Do not put completed command in a code block."

    @abstractmethod
    def get_completion(self, full_command: str) -> str:
        pass


class OpenAIClient(BaseClient):
    """
    Reads configuration from environment variables:
        - OPENAI_API_KEY (required)
        - OPENAI_BASE_URL (optional): defaults to "https://api.openai.com/v1".
        - OPENAI_ORGANIZATION (optional): defaults to None
        - OPENAI_MODEL (optional): defaults to "gpt-4o-mini"
        - OPENAI_TEMPERATURE (optional): defaults to 0.
    """

    api_type = "openai"

    def __init__(self):
        try:
            from openai import OpenAI
        except ImportError:
            print(
                "OpenAI library is not installed. Please install it using 'pip install openai'"
            )
            sys.exit(1)

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("OPENAI_API_KEY environment variable not set.")
            sys.exit(1)

        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0"))
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            organization=os.getenv("OPENAI_ORGANIZATION"),
        )

    def get_completion(self, full_command: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_command},
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content


class GoogleGenAIClient(BaseClient):
    """
    Reads configuration from environment variables:
        - GEMINI_API_KEY (required)
        - GEMINI_MODEL (optional): defaults to "gemma-3-27b-it"
    """

    api_type = "gemini"

    def __init__(self):
        try:
            import google.generativeai as genai
        except ImportError:
            print(
                "Google Generative AI library is not installed. Please install it using 'pip install google-generativeai'"
            )
            sys.exit(1)

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("GEMINI_API_KEY environment variable not set.")
            sys.exit(1)
            
        genai.configure(api_key=api_key)
        self.model_name = os.getenv("GEMINI_MODEL", "gemma-3-27b-it")
        self.generative_model = genai.GenerativeModel(self.model_name)

    def get_completion(self, full_command: str) -> str:
        chat = self.generative_model.start_chat(history=[])
        prompt = f"{self.system_prompt}\\n\\n{full_command}" # Escaped newline for the diff
        response = chat.send_message(prompt)
        return response.text


class GroqClient(BaseClient):
    """
    Reads configuration from environment variables:
        - GROQ_API_KEY (required)
        - GROQ_MODEL (optional): defaults to "llama-3.2-11b-text-preview"
        - GROQ_TEMPERATURE (optional): defaults to 0.
    """
    
    api_type = "groq"
    
    def __init__(self):
        try:
            from groq import Groq
        except ImportError:
            print(
                "Groq library is not installed. Please install it using 'pip install groq'"
            )
            sys.exit(1)

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("GROQ_API_KEY environment variable not set.")
            sys.exit(1)
            
        self.model = os.getenv("GROQ_MODEL", "llama-3.2-11b-text-preview")
        self.temperature = float(os.getenv("GROQ_TEMPERATURE", "0"))
        
        self.client = Groq(api_key=api_key)
    
    def get_completion(self, full_command: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_command},
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content


class MistralClient(BaseClient):
    """
    Reads configuration from environment variables:
        - MISTRAL_API_KEY (required)
        - MISTRAL_MODEL (optional): defaults to "codestral-latest"
        - MISTRAL_TEMPERATURE (optional): defaults to 0.
    """
    
    api_type = "mistral"
    
    def __init__(self):
        try:
            from mistralai import Mistral # Assuming this is the correct class as per original
        except ImportError:
            print(
                "Mistral AI library is not installed. Please install it using 'pip install mistralai'"
            )
            sys.exit(1)
        
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            print("MISTRAL_API_KEY environment variable not set.")
            sys.exit(1)

        self.model = os.getenv("MISTRAL_MODEL", "codestral-latest")
        self.temperature = float(os.getenv("MISTRAL_TEMPERATURE", "0"))
        
        self.client = Mistral(api_key=api_key)
        
    def get_completion(self, full_command: str) -> str:
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_command},
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content

class AmazonBedrock(BaseClient):
    """
    Reads configuration from environment variables:
        - BEDROCK_AWS_REGION (optional): defaults to environment variable AWS_REGION
        - BEDROCK_AWS_ACCESS_KEY_ID (optional): defaults to environment variable AWS_ACCESS_KEY_ID
        - BEDROCK_AWS_SECRET_ACCESS_KEY (optional): defaults to environment variable AWS_SECRET_ACCESS_KEY
        - BEDROCK_AWS_SESSION_TOKEN (optional): defaults to environment variable AWS_SESSION_TOKEN
        - BEDROCK_MODEL (optional): defaults to "anthropic.claude-3-5-sonnet-20240620-v1:0"
        - BEDROCK_TEMPERATURE (optional): defaults to 0.
    """

    api_type = "bedrock"

    def __init__(self):
        try:
            import boto3
        except ImportError:
            print(
                "Boto3 library is not installed. Please install it using 'pip install boto3'"
            )
            sys.exit(1)

        self.model = os.getenv("BEDROCK_MODEL", "anthropic.claude-3-5-sonnet-20240620-v1:0")
        self.temperature = float(os.getenv("BEDROCK_TEMPERATURE", "0"))

        session_kwargs = {}
        aws_region = os.getenv("BEDROCK_AWS_REGION")
        if aws_region:
            session_kwargs["region_name"] = aws_region
        
        aws_access_key_id = os.getenv("BEDROCK_AWS_ACCESS_KEY_ID")
        if aws_access_key_id:
            session_kwargs["aws_access_key_id"] = aws_access_key_id

        aws_secret_access_key = os.getenv("BEDROCK_AWS_SECRET_ACCESS_KEY")
        if aws_secret_access_key:
            session_kwargs["aws_secret_access_key"] = aws_secret_access_key
            
        aws_session_token = os.getenv("BEDROCK_AWS_SESSION_TOKEN")
        if aws_session_token:
            session_kwargs["aws_session_token"] = aws_session_token
        
        self.client = boto3.client("bedrock-runtime", **session_kwargs)

    def get_completion(self, full_command: str) -> str:
        import json

        messages = [
            {"role": "user", "content": full_command}
        ]

        # Format request body based on model type
        if "claude" in self.model.lower():
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "system": self.system_prompt,
                "messages": messages,
                "temperature": self.temperature
            }
        else:
            # This part might need to be expanded if supporting other Bedrock model families
            # that require different request body structures.
            raise ValueError(f"Unsupported model for Amazon Bedrock: {self.model}. Currently only Claude models are explicitly supported with this body structure.")

        response = self.client.invoke_model(
            modelId=self.model,
            body=json.dumps(body)
        )

        response_body = json.loads(response['body'].read())
        return response_body["content"][0]["text"]


class ClientFactory:
    api_types = [OpenAIClient.api_type, GoogleGenAIClient.api_type, GroqClient.api_type, MistralClient.api_type, AmazonBedrock.api_type]

    @classmethod
    def create(cls):
        service_type = os.getenv("CODEX_SERVICE_TYPE")
        if not service_type:
            print("CODEX_SERVICE_TYPE environment variable not set.")
            print(f"Please set it to one of: {', '.join(cls.api_types)}")
            sys.exit(1)
        
        match service_type.lower(): # Use lower() for case-insensitive matching
            case OpenAIClient.api_type:
                return OpenAIClient()
            case GoogleGenAIClient.api_type:
                return GoogleGenAIClient()
            case GroqClient.api_type:
                return GroqClient()
            case MistralClient.api_type:
                return MistralClient()
            case AmazonBedrock.api_type:
                return AmazonBedrock()
            case _:
                print(
                    f"Specified API type '{service_type}' is not one of the supported services: {', '.join(cls.api_types)}"
                )
                sys.exit(1)
