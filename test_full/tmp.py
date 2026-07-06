from vllm import LLM, SamplingParams
from tqdm import tqdm
from transformers import AutoTokenizer


if __name__ == "__main__":
    model_name_official = "Qwen/Qwen2.5-Coder-32B-Instruct"
    vllm_tensor_parallel_size = 4
    vllm_max_model_length = 32768

    llm = LLM(model=model_name_official, max_model_len=vllm_max_model_length,
              tensor_parallel_size=vllm_tensor_parallel_size)
    #  max_tokens is for the maximum length for generation.
    tokenizer = AutoTokenizer.from_pretrained(model_name_official)
    sampling_params = SamplingParams(n=3, temperature=0.7, top_p=0.8, top_k=20, repetition_penalty=1.05,
                                     max_tokens=8192)

    conversation = [{"role": "user", "content": "who are you?"}]
    text = tokenizer.apply_chat_template(
        conversation,
        tokenize=False,
        add_generation_prompt=True
        )
    conversation_outputs = llm.generate([text], sampling_params, use_tqdm=True)
    for conversation_output in conversation_outputs:
        # print(conversation_outputs)
        generations = []
        for tmp in conversation_output.outputs:
            print(tmp.text)
