import time
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
import transformers




def generate_with_time(model, inputs, **kwargs):
    start_time = time.time()
    outputs = model.generate(**inputs, **kwargs)
    generation_time = time.time() - start_time
    return outputs, generation_time

def assisted_generate_with_time(model, assistant_model, inputs, **kwargs):
    start_time = time.time()
    # outputs = model.generate(**inputs, assistant_model=assistant_model, do_sample=True, temperature=0.5, **kwargs)
    outputs = model.generate(**inputs, assistant_model=assistant_model, **kwargs)
    generation_time = time.time() - start_time
    return outputs, generation_time

def staged_assisted_generate_with_time(model, assistant_model_1, assistant_model_2, inputs, **kwargs):
    start_time = time.time()
    # outputs = model.generate(**inputs, assistant_model=assistant_model, do_sample=True, temperature=0.5, **kwargs)
    outputs = model.generate(**inputs, assistant_model=assistant_model_1, secondary_assistant_model=assistant_model_2, **kwargs)
    generation_time = time.time() - start_time
    return outputs, generation_time

if __name__ == "__main__":
    from transformers.utils import logging
    logging.set_verbosity_info()
    logger = logging.get_logger("transformers")
    
    
    import logging as py_logging
    import os
    import torch
    file_handler = py_logging.FileHandler("test.log")
    logging.add_handler(file_handler)
    logger.info("Starting the test")
    
    prompt = "Say a short sentance."
    # checkpoint = "EleutherAI/pythia-1.4b-deduped"
    checkpoint = "EleutherAI/pythia-2.8b-deduped"
    assistant_checkpoint_1 = "EleutherAI/pythia-160m-deduped"
    assistant_checkpoint_2 = "EleutherAI/pythia-1.4b-deduped"
    assistant_model = "EleutherAI/pythia-160m-deduped"
    
    # checkpoint = "meta-llama/Llama-2-7b-chat-hf"
    # assistant_checkpoint = "PY007/TinyLlama-1.1B-Chat-v0.1"
    
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    inputs = tokenizer(prompt, return_tensors="pt")
    model = AutoModelForCausalLM.from_pretrained(checkpoint)
    # assistant_model_1 = AutoModelForCausalLM.from_pretrained(assistant_checkpoint_1)
    # assistant_model_2 = AutoModelForCausalLM.from_pretrained(assistant_checkpoint_2)
    assistant_model = AutoModelForCausalLM.from_pretrained(assistant_model)
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(device)
    


    inputs.to(device)
    model.to(device)
    
    # assistant_model_1.to(device)

    # assistant_model_2.to(device)
    # assisted_time_2 = staged_assisted_generate_with_time(model, assistant_model_1, assistant_model_2, inputs)
    
    assistant_model.to(device)

    assisted_time_1 = assisted_generate_with_time(model, assistant_model, inputs)
    
    # raw_time = generate_with_time(model, inputs)
    # logger.info(f"raw generation time: {raw_time[1]}")
    logger.info(f"Assisted generation time: {assisted_time_1[1]}")
    # log decoded outputs by tokenizers
    # logger.info(tokenizer.decode(raw_time[0][0]))
    # logger.info(tokenizer.decode(assisted_time_2[0][0]))
    
    # use tokenizers to decode the outputs
    # logger.info(tokenizer.decode(raw_time[0][0]))