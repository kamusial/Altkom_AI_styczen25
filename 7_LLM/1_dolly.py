import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "databricks/dolly-v2-12b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name,
                                             device_map="auto")

prompt = 'Dokąd nocą tupta jeż'
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=100)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
