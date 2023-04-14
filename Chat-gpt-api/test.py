from config.chatgpt_config import config_dict
from src.openai_request import OpenAI_Request
import time
from tools.cfg_wrapper import load_config
from tools.context import ContextHandler
from tools.tokennizer import Tokennizer
import json
answer = []

def chat_test(keys,model_name,request_address,context_handler,tokenizer,question,log_time=False,context_max=3200):

    requestor = OpenAI_Request(keys, model_name,request_address)

    while 1:
        # input_s = input('\nuser input : ')
        input_s = question
        if input_s == "clear":
            context_handler.clear()
            print('start a new session')
            continue
        else:
            inputs_length = tokenizer.num_tokens_from_string(input_s)
            context_handler.append_cur_to_context(input_s,inputs_length)

        st_time = time.time()

        res = requestor.post_request(context_handler.context)
        ed_time = time.time()

        if res.status_code == 200:

            response = res.json()['choices'][0]['message']['content']
            # cut \n for show
            response = response.lstrip("\n")
            # answer.append(response)
            return response
            completion_length = res.json()['usage']['completion_tokens']
            total_length = res.json()['usage']['total_tokens']
            print(f"\nresponse : {response}")

            context_handler.append_cur_to_context(response,completion_length,tag=1)
            if total_length > context_max:
                context_handler.cut_context(total_length,tokenizer)

        if log_time:
            print(f'time cost : {ed_time - st_time}')


if __name__ == '__main__':
    with open('data/clear_text.json', 'r') as f:
        information = json.load(f)
    # load config
    config = load_config(config_dict)
    keys = config.Acess_config.authorization
    model_name = config.Model_config.model_name
    request_address = config.Model_config.request_address

    # load context
    context_manage_config = config.Context_manage_config
    del_config = context_manage_config.del_config
    max_context = context_manage_config.max_context
    context = ContextHandler(max_context=max_context,context_del_config=del_config)

    # load tokenizer
    tokenizer = Tokennizer(model_name)

    # for test
    prefix = 'Extract person, pleace, the primary behavior from this text,action verb by one word ,If none must return NULL:\n\n '

    # a = chat_test(keys,model_name,request_address,context,tokenizer,'Extract person, pleace, behavior from this text,and given a  action verb ,If none must return NULL:\n\n\"JOKER TEARS OPEN THE PRESCRIPTION BAG... A FLURRY OF PILL:\\\" BOTTLES TUMBLE OUT ONTO THE COUNTER.\\\"\"')


    sluglines = []
    for line in information:
        sluglines = []
        for i in line:
            input = prefix + '‘' + i + '‘'
            print(input)
            gpt_result = chat_test(keys, model_name, request_address, context, tokenizer,
                      prefix)
            print(gpt_result)
            sluglines.append(gpt_result)
            continue
        answer.append(sluglines)
        break
    print(answer)

    jstring = json.dumps(answer)
    jsonFile = open("data/gpt_result.json", "w")
    jsonFile.write(jstring)
    jsonFile.close()