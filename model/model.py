from key_load.Key_get import load_key
from langchain_community.chat_models.tongyi import ChatTongyi

llm = ChatTongyi(
    model="qwen-max",
    dashscope_api_key=load_key("Qianwen_API_KEY"),
    temperature=0,
)