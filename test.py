import os
from langchain_community.llms import Tongyi

os.environ["DASHSCOPE_API_KEY"] = 'sk-7b93e8e814104fcd9051de56186c190e'
llm = Tongyi(model_name="qwen-plus", temperature=0.7)
# text = llm.invoke("请给我写一句情人节红玫瑰的中文宣传语")
text = llm.invoke("请给我的花店起个名")
print(text)