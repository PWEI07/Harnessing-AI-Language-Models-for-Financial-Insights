from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoModelForSeq2SeqLM

model_id = 'google/flan-t5-large'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

from transformers import GPT2Tokenizer, GPT2Model
tokenizer1 = GPT2Tokenizer.from_pretrained('gpt2')
model1 = GPT2Model.from_pretrained('gpt2')

pipe = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer,
    max_length=1000
)

pipe1 = pipeline(
    "text2text-generation",
    model=model1,
    tokenizer=tokenizer1,
    max_length=1000
)

local_llm = HuggingFacePipeline(pipeline=pipe)

print(local_llm("analyze the impact for ZIM based on the news: "+ text))

local_llm1 = HuggingFacePipeline(pipeline=pipe1)

print(local_llm1("analyze the impact for ZIM based on this link https://seekingalpha.com/news/4041014-us-warning-evolving-threats-ships-red-sea-trade-route"))


"analyze the impact for ZIM based on this link https://seekingalpha.com/news/4041014-us-warning-evolving-threats-ships-red-sea-trade-route"


template = """Question: {question} Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])

llm_chain = LLMChain(prompt=prompt, llm=local_llm)
question = "What is the population of the richest city in Europe?"
print(llm_chain.run(question))











