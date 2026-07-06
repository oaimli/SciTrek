from openai import OpenAI

if __name__ == "__main__":
    model_name_official = "o4-mini-2025-04-16"

    api_key = ""
    client = OpenAI(api_key=api_key)


    output_dict = client.chat.completions.create(
        model=model_name_official,
        messages=[
            {
                "role": "user",
                "content": "Who are you?"}
            ],
        n=3
        )
    # print(output_dict)
    outputs = []
    for choice in output_dict.choices:
        outputs.append(choice.message.content)
    print(outputs)