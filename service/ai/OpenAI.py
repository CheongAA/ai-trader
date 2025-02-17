from openai import OpenAI as openai
import base64
import json

class OpenAI:
    def __init__(self, key, model):
        self.key = key
        self.model = openai(api_key=key)

    def generate_content(self, prompt, data, schema):
        content = [{"type": "text", "text": prompt}]
        
        # 이미지 파일인 경우 base64로 인코딩
        if isinstance(data, str) and data.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                with open(data, 'rb') as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    })
            except Exception as e:
                print(f"이미지 처리 중 오류 발생: {e}")
                return None
        else:
            # 텍스트 데이터인 경우
            content.append({"type": "text", "text": str(data)})

        try:
            response = self.model.beta.chat.completions.parse(
                model="gpt-4o", 
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": content}
                ],
                response_format=schema
            )
            
            result = json.loads(response.choices[0].message.content)
            print('응답:', result)
            
            return result
            
        except Exception as e:
            print(f"API 호출 중 오류 발생: {e}")
            return None

