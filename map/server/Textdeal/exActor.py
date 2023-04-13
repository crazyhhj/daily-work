

import re
import json
from copy import deepcopy
# film script file

def extract_scene_headings(film_script_txtfile_path, mode=1):
    # A couple options on regex patterns, depending on script format. Might need tweaks per script
    film_scene_heading_regexp_1 = "(?<=INT. |EXT. ).*(?=,)"
    film_scene_heading_regexp_2 = "(?<=INT. |EXT. ).*(?= -)"

    if mode == 1:
        regexp = film_scene_heading_regexp_1
    elif mode == 2:
        regexp = film_scene_heading_regexp_2

    # Open film script .txt file
    with open(film_script_txtfile_path, "r", encoding='utf-8') as f:
        film_string = f.readlines()

    places = [
        re.findall(regexp, line)
        for line in film_string
        if re.findall(regexp, line)
    ]

    return [place[0] for place in places] if places else None


#得到场景 screenplay的片段名
def screenplay(film_script_txtfile_path):
    slug_lines = r'^\d+.*[EXT|INT].*\n'
    # slug_lines = "EXT.*|INT.*"
    # slug_lines = ".*(?=:\n"
    with open(film_script_txtfile_path, "r", encoding='utf-8') as f:
        film_string = f.readlines()
    senceplay = []
    for line in film_string:

        valid = re.findall(slug_lines, line)
        if valid:
            # print(line)
            # print(valid[0])
            senceplay.append(valid[0])
    return senceplay

#提取 slug lines 中信息的函数 并打包成列表【INT/ENT】【PLEACE】【TIMEING】
# 提取 电影 转场(TRANSITIONS) 词段  并且 提取转场到哪一幕
def transitions_ex(film_script_txtfile_path):
    transitions = r'.*(?=:\n)'
    slug_lines = "^\d+.*[EXT|INT].*"
    #get file list
    with open(film_script_txtfile_path, "r", encoding='utf-8') as f:
        film_string = f.readlines()
    transitions_list = []
    info_tran = []
    i = 0
    j = 0
    for line in film_string:
        temp = []
        tran_span = re.findall(transitions, line)
        #get [CUT TO][FADE IN] like this
        if tran_span:
            transitions_list.append(tran_span)
            temp.append(tran_span)
            #当找到 转场词 开始搜寻接下来的 动作 直到 找到下一个slug line
            j = i+1
            while len(film_string)-j:
                if(film_string[j]!='\n'):
                    temp.append(film_string[j])
                    v = re.findall(slug_lines, film_string[j])
                    if v:
                        break
                j=j+1
            info_tran.append(temp)
        i = i + 1
    print(transitions_list, info_tran)
    return transitions_list, info_tran
# 对相机 信息 的提取
# (.*(?=:\n)

#抽取对话人物
def PERSON(film_script_txtfile_path):
    per1=r'^[\s]+[A-Z]+\n'
    per2=r'(?<=\s)+[A-Z]+\n'
    per3=r'(?<=\s)+[A-Z]+.*[A-Z]+\n'
    with open(film_script_txtfile_path, "r", encoding='utf-8') as f:
        film_string = f.readlines()
    person = []
    supper = []
    for line in film_string:
        valid = re.findall(per3, line)

        if valid:
            if line.isupper():
                if not ('EXT.' in line or 'INT.' in line):
                    # person.append(valid[0])
                    person.append(line)
        if line.isupper():
            if not ('EXT.' in line or 'INT.' in line):
                # print(line)

                if '(' in line or '#' in line:
                    # print(line)
                    person.append(line)
    #此处返回的是未处理过格式的person
    return person


#格式化 person
def format_person(person):
    result = []
    org_name = []

    for line in person:
        a = re.findall(r'(?<=\s)+[A-Z]+.*(?=\n)', line)
        if a:
            result.append(a[0])
            org_name.append(line)

    return result, org_name

def dividBySluglines(text_path, sluglines, person, per):
    #format
    #{id:'num',sluglines:'EXT',dialogue:'string',person:[person1,person2]} id sluglines
    with open(text_path, "r",encoding='utf-8') as f:
        script = f.readlines()
    #dict
    info_sum = []

    screen_sum = []
    count = 0
    time = 0
    for i in range(len(script)):
        count = i+1
        if script[i] in sluglines:
            # print(script[i])
            # print('{')
            screen_sum.append([script[i]])
            for j in range(count, len(script)):
                if script[j] in person:
                    index = person.index(script[j])
                    # print(script[j])
                    tmp = per[index]
                    if len(tmp) >= 25:
                        break
                    screen_sum[-1].append([per[index]])
                    screen_sum[-1][-1].append([])

                    tempdialogue = []
                    tempstr = ""
                    for k in range(j+1, len(script)):
                        #\n区分

                        if script[k] == '\n':
                            break
                        # print(script[k])
                        tempdialogue.append(script[k])
                    for line in tempdialogue:
                        tempstr = tempstr + ' ' + line.strip()

                    screen_sum[-1][-1][-1].append(tempstr)

                if script[j] in sluglines:
                    break
            # print('}')


    for slugline in sluglines:
        # print(slugline)
        info_dict = {}

        id = re.findall(r'^\d+', slugline)
        info_dict['id'] = id[0]
        slug = re.findall(r'[A-Z]+.*[A-Z]', slugline)
        info_dict['slug']=slug

        # print(info_dict)
        info_sum.append(info_dict)
    # print(info_sum)
    return screen_sum

def divid_launch(script_path):
    sluglines = screenplay(script_path)
    person = PERSON(script_path)

    per,org_name = format_person(person)
    # print(org_name)
    screen_sum = dividBySluglines(script_path, sluglines, org_name, per)
    # jstring = json.dumps(screen_sum)
    # jsonFile = open("data.json", "w")
    # jsonFile.write(jstring)
    # jsonFile.close()
    # print(screen_sum)
    return screen_sum

def dialogue(script_path):
    sluglines = screenplay(script_path)
    person = PERSON(script_path)

    per, org_name = format_person(person)

    with open(script_path, "r",encoding='utf-8') as f:
        script = f.readlines()
    slugdia = []
    dict = {}
    sent = ''

    start = script.index(sluglines[0])

    slugline = script[start]
    i = start
    for i in range(start, len(script)):
        if i == len(script) - 1:
            dict['screen'] = slugline

            slugline = script[i]
            dict['content'] = sent
            slugdia.append(dict)

        if not script[i] in sluglines:
            sent = sent + script[i].strip() + '\n'
        else:
            dict['screen'] = slugline

            slugline = script[i]
            dict['content'] = sent
            slugdia.append(dict)
            sent = ''
            dict = {}
    slugdia.pop(0)
    return slugdia
# dialogue('../Joker.txt')

def format_information(script_path):
    screen_sum = divid_launch(script_path)
    # sluglines = screenplay(script_path)
    ul=[]
    # slug_info={}
    i=0;index=0
    # 每一幕
    for group in screen_sum:
        # tempslug=''
        slug_info={}
        index=index+1
        door,time,place='','',''
        door = re.findall(r'(EXT|INT)', group[0])

        #提取 slugline 中的时间信息
        time1 = re.findall(r'(?<=- ).*(?=\W+)',group[0])
        time = re.findall(r'(?<=- ).*',time1[0])
        if len(time)>0:
            time_of_day = time[0].strip(' 0123456789')
        else:
            time_of_day= time1[0].strip(' 0123456789')

        if time_of_day =='CONTINUOUS':
            time_of_day=temp_time
        temp_time = time_of_day
        # print(index,time_of_day)
        #place
        place = re.findall(r'(?<=[EXT.|INT.]\s).*(?=[-])', group[0])
        place1 = re.findall(r'([,|-].*[,|-])',group[0])
        slug_info['id']=index;slug_info['door']=door[0];slug_info['time']=time_of_day;slug_info['place']=place[0];slug_info['slug']=group[0]
        # tempslug=slug_info
        # print(ul)
        ul.append(slug_info)
        print(place)
        print(place1)

        if len(group)>1:
            i=i+1
            #get [NAME[dialgoe]],NAME[dialgoe],NAME[dialgoe],NAME[dialgoe]
            namedict={}
            namelist=[]
            person = []
            for num in range(1,len(group)):
                # print(group[num][0])
                name = group[num][0]
                #得到人名列表
                person.append(name)
            sum = 0
            for human in person:
                namedict[human]=person.count(human)
            #{'JOKER': 17, 'SOCIAL WORKER': 17, "JOKER (CONT'D)": 1} 得到了人名 次数字典
            for i in namedict.values():
                sum = sum + i
            # print(sum)
            # print(namedict)
            # print(person)
                # print(name,len(group))
            # print(group)
        # else:
            # 加入空值
        # print(li) eqq

    return ul
#写一个 统计 person 中人物 出场的
def clear(script_path):
    person = PERSON(script_path)

    per, org_name = format_person(person)
    # print(len(per))
    namelist=[]
    fredict={}
    for name in per:
        temp = re.findall(r'.*(?=\()', name)
        # print(name)
        print(temp)
        if temp:
            talker = temp[0].strip()
            # print(talker)
            namelist.append(talker)
        else:
            if len(name) > 25:
                # print(name)
                continue
            talker = name.strip()
            namelist.append(talker)
    for line in namelist:
        name=line
        count = namelist.count(line)
        fredict[name]=count
    return fredict

def fre(script_path):
    info = format_information(script_path)
    timeall=[]
    timefre={}
    for line in info:
        time = line['time']
        timeall.append(time)
        print(time)
    for i in timeall:
        timefre[i]=timeall.index(i)

    return timefre
# a = fre('../Joker.txt') ; print(a)

def performance_distribution(script_path):
    person = PERSON(script_path)

    per, org_name = format_person(person)
    name = per
    per_dict = {}
    while name:
        if len(name[0]) < 25:
            per_dict[per[0]] = []
        name.pop(0)
    # print(per_dict, len(per_dict))
    old = divid_launch(script_path)

    for i in range(len(old)):
        actor_sum = old[i]
        if len(actor_sum) > 1:
            for j in range(1, len(actor_sum)):
                people = actor_sum[j][0]
                per_dict[people].append(i+1)
                if len(per_dict[people]) > 1:
                    if per_dict[people][-1] == per_dict[people][-2]:
                        per_dict[people].pop(-1)
    print(per_dict)
    li = []
    for item in per_dict:
        temp = {}
        temp['name'] = item
        temp['range'] = per_dict[item]
        temp['sign'] = len(per_dict[item])
        li.append(temp)
    del li[0]
    return li
# li = performance_distribution('../Joker.txt')
# print(li)
# # clear('../Joker.txt')

def emotion():
    person = PERSON('../Joker.txt')

    per, org_name = format_person(person)
    name = per
    per_dict = {}
    while name:
        if len(name[0]) < 25:
            per_dict[name[0]] = ''
        name.pop(0)
    name_list = [key for key in per_dict]
    name_list.pop(0)
    # print(name_list, len(name_list))
    with open('../data/emotion.json', 'r') as f:
        information = json.load(f)

    emo_info = []
    cont_dict = []
    for slug in information:
        slug_act_emo: dict = {}
        name_count_dict = {}
        if len(slug) == 1:
            slug_act_emo['slugline'] = slug[0]
            emo_info.append(slug_act_emo)

            name_count_dict['slug'] = slug[0]
            cont_dict.append(name_count_dict)
            continue
        for i in range(1, len(slug)):
            slug_act_emo = {}
            slug_act_emo['slugline'] = slug[0]
            name = slug[i][0]
            sentence = slug[i][1]
            # print(sentence[0])
            feel = slug[i][-1]
            slug_act_emo['name'] = name
            slug_act_emo['sentence'] = sentence
            slug_act_emo['feel'] = feel
            # print(slug_act_emo)

            emo_info.append(slug_act_emo)
            name_count_dict[name] = []
            name_count_dict['slug'] = slug[0]
        cont_dict.append(name_count_dict)
    # print(emo_info)

    for j in range(len(information)):
        slug = information[j]
        if len(slug) == 1:

            continue
        for k in range(1, len(slug)):
            name = slug[k][0]
            feel = slug[k][-1]
            cont_dict[j][name].append(feel)
            # print(cont_dict[j])
            # print(slug[k])
        print(cont_dict[j])
    # print(cont_dict)

    final_list = {}
    for name in name_list:
        temp = []
        for i in range(len(cont_dict)):
            # print(cont_dict[i])
            slug_name = {}
            slug_name['slug'] = cont_dict[i]['slug']
            for key, value in cont_dict[i].items():
                if key == name:
                    slug_name['name'] = name
                    slug_name['emotion'] = value
                    slug_name['fre'] = len(value)
                    temp.append(slug_name)
                    break

            # temp.append({})
        final_list[name] = temp

    # print(final_list)
    # print(len(final_list))
    # print(final_list['JOKER'])

    # jstring = json.dumps(final_list)
    # jsonFile = open("../data/emo_final.json", "w")
    # jsonFile.write(jstring)
    # jsonFile.close()

    return emo_info
# aa = emotion()

def slug_emotion():
    person = PERSON('../Joker.txt')

    per, org_name = format_person(person)
    name = per
    per_dict = {}
    while name:
        if len(name[0]) < 25:
            per_dict[name[0]] = ''
        name.pop(0)
    name_list = [key for key in per_dict]
    name_list.pop(0)
    # print(name_list, len(name_list))
    with open('../data/emotion.json', 'r') as f:
        information = json.load(f)

    emo_info = []
    cont_dict = []
    for slug in information:
        slug_act_emo: dict = {}
        name_count_dict = {}
        if len(slug) == 1:
            slug_act_emo['slugline'] = slug[0]
            emo_info.append(slug_act_emo)

            name_count_dict['slug'] = slug[0]
            cont_dict.append(name_count_dict)
            continue
        for i in range(1, len(slug)):
            slug_act_emo = {}
            slug_act_emo['slugline'] = slug[0]
            name = slug[i][0]
            sentence = slug[i][1]
            # print(sentence[0])
            feel = slug[i][-1]
            slug_act_emo['name'] = name
            slug_act_emo['sentence'] = sentence
            slug_act_emo['feel'] = feel
            # print(slug_act_emo)

            emo_info.append(slug_act_emo)
            name_count_dict[name] = []
            name_count_dict['slug'] = slug[0]
        cont_dict.append(name_count_dict)
    # print(emo_info)

    for j in range(len(information)):
        slug = information[j]
        if len(slug) == 1:
            continue
        for k in range(1, len(slug)):
            name = slug[k][0]
            feel = slug[k][-1]
            cont_dict[j][name].append(feel)
            # print(cont_dict[j])
            # print(slug[k])
        # print(cont_dict[j])
    # print(cont_dict)

    actor_emotion_slug: list = []
    screen: list = []
    actor: dict = {}
    blank_l = []
    blank_d = {}
    for slug in cont_dict:
        screen = deepcopy(blank_l)
        for key, value in slug.items():
            actor = deepcopy(blank_d)
            if not key == 'slug':
                actor['name'] = key
                actor['emotion'] = value
                screen.append(actor)
        # print(screen)
        actor_emotion_slug.append(screen)
#     jstring = json.dumps(actor_emotion_slug)
#     jsonFile = open("../data/actor_emotion_slug.json", "w")
#     jsonFile.write(jstring)
#     jsonFile.close()
#
#
# slug_emotion()

def digraph():
    with open('../data/emotion.json', 'r') as f:
        file = json.load(f)

    unit = []

    for slug in file:
        lite = []
        if len(slug) > 0:
            for i in range(1, len(slug)):
                lite.append(slug[i][0])
        else:
            continue
        unit.append(lite)


    sequential_dialogue: list = []
    for group in unit:
        slug = []
        if len(group) >= 2:
            for i in range(len(group)-1):
                dia = {}
                dia['source'] = group[i]
                dia['target'] = group[i+1]
                slug.append(dia)
        elif len(group) == 1:
            slug.append({'source': group[0],'target':group[0]})
        sequential_dialogue.append(slug)

    a = []
    for g in sequential_dialogue:
        b = []
        for i in range(len(g)):
            value = g.count(g[i])
            c = deepcopy(g[i])
            c['value'] = value
            c['type'] = 'defult'
            b.append(c)
        a.append(b)

    fre_relation = []
    for g in a:
        res = []
        for i in g:
            if i not in res:
                res.append(i)
        fre_relation.append(res)

#     jstring = json.dumps(fre_relation)
#     jsonFile = open("../data/freRealtion", "w")
#     jsonFile.write(jstring)
#     jsonFile.close()
#
# digraph()

def place():
    with open('../data/slugInfo.json', 'r') as f:
        information = json.load(f)
    place_list: list = []
    for slug in information:
        divide_place = slug['place'].replace('-',',').split(',')
        place_list.append(divide_place)
    flat_list = sum(place_list, [])
    loc_set = set(flat_list)
    all_loc: list = []
    for slug in place_list:
        unit_loc: list = []
        for i in slug:
            if i in loc_set:
                unit_loc.append(i)
        all_loc.append(unit_loc)
    result = {'data':all_loc, 'class':list(loc_set)}
    # jstring = json.dumps(result)
    # jsonFile = open("../data/location.json", "w")
    # jsonFile.write(jstring)
    # jsonFile.close()
def words_count(path):
    words_info: list = []
    info = dialogue(path)
    # print(info)
    count = 1
    for i in info:
        id = str(count)
        count = count + 1
        slug_group: dict = {}
        tmp = re.sub('^\d+', '', i['screen'])
        tmp = re.sub('\d+$', '', tmp)
        final = id + ' ' + tmp.strip()
        slug_group['screen'] = final
        slug_group['content'] = len(i['content'])
        words_info.append(slug_group)
    return words_info
