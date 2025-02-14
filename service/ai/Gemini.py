import google.generativeai as genai
import json

class Gemini:
    def __init__(self, key, model):
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel(model)
    

    def generate_content(self, prompt, data, schema):
        result = self.model.generate_content(
            [prompt, data],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.7
            )
        )
        return json.loads(result.candidates[0].content.parts[0].text)
