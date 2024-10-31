import os
import google.generativeai as genai
from google.api_core import retry


class GeminiClient:
    def __init__(self, model_name: str, instructions_file: str):
        """
        Initialize the GeminiClient with model configuration and system instructions.

        Args:
            model_name: Name of the Gemini model to use.
            instructions_file: Path to the instructions file.
        """
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model_name = model_name

        with open(instructions_file, "r") as f:
            instruction = f.read().strip()

        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=instruction,
        )

    def generate_content(self, prompt: list, tools=None):
        """
        Generate content from the Gemini model based on the provided prompt.

        Args:
            prompt: The prompt to send to the model.
            tools: Optional tools or functions the model can use.

        Returns:
            The model's response.
        """
        try:
            if tools and tools != "code_execution":
                tool_config={"function_calling_config": {"mode": "ANY"}}
            else:
                tool_config = None

            response = self.model.generate_content(
                prompt,
                tools=tools,
                request_options={"retry": retry.Retry()},
                tool_config=tool_config,
            )
            return response
        except Exception as e:
            # Handle exceptions as needed
            raise e
