from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI

from utils.template import template


from dotenv import load_dotenv
load_dotenv()

class RagPipeline:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.1)
        self.chain = self.init_chain()

    def init_chain(self):
        prompt = PromptTemplate.from_template(template)
        rag_chain = prompt | self.llm | StrOutputParser()
        return rag_chain

    def generate_answer(self, question: str):
        # chain에 입력을 전달하여 RAG 모델에서 답변 생성
        
        inputs = {
            "question": question
        }

        response = self.chain.invoke(inputs)
        return response
