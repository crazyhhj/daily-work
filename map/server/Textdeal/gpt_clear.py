import re
import json

with open('../data/gpt_result.json', 'r', encoding='utf-8') as f:
    front = json.load(f)
with open('../data/gpt_result_first.json', 'r', encoding='utf-8') as w:
    end = json.load(w)

with open('../data/clear_text.json', 'r', encoding='utf-8') as z:
    film = json.load(z)

with open('../data/emotion.json', 'r', encoding='utf-8') as z:
    emo = json.load(z)


def model_judge(line):
    # line = line.strip(':')
    line = re.sub('\n|}',' $ ', line)
    line = re.sub(':|{','', line)
    sent = line.split(' ')
    guan = ['Person', 'Place', 'Behavior', 'ActionVerb', 'Verb']
    plot_dict = {'Person': '', 'Place': '', 'Behavior': '', 'ActionVerb': ''}
    for idx in range(len(sent)):
        unit = sent[idx]
        if unit in guan:
            words = ''
            for word in sent[idx+1:]:

                if word == '$' or word in guan or word == sent[-1]:
                    plot_dict['' + unit + ''] = words.strip()
                    break
                words = words + ' ' + word
    return plot_dict
    # print(sent)

plot = end + front

no_dia = []
for i in film:
    tmp = []
    for j in i:
        if j[0] == '$':
            continue
        tmp.append(j)
    no_dia.append(tmp)
no_dia = no_dia[1:]
#
for i in range(len(no_dia)):
    for j in range(len(no_dia[i])):
        plot_dict = model_judge(plot[i][j])
        if len(plot_dict) == 0:
            plot_dict['Person'] = ''
            plot_dict['Place'] = ''
            plot_dict['Behavior'] = ''
            plot_dict['ActionVerb'] = ''
        plot_dict['sentence'] = no_dia[i][j]
        plot_dict['slugIndex'] = i + 1
        plot[i][j] = plot_dict

# jstring = json.dumps(plot)
# jsFile = open('../data/film_event_data.json', 'w')
# jsFile.write(jstring)
# jsFile.close()
# for i in plot:
#     for j in i:
#         print(j['Behavior'], '--------',j['ActionVerb'])
#
mix_plot = []
slug = []
e = {}


#margin plot and emo.   emo list [1:128] but plot not have 128, plot[1:127]
film = film[1:]
emo = emo[:-1]
# for i in emo:
#     print(i[1])
for i in range(len(emo)):
    emo[i] = emo[i][1:]

for idx in range(len(film)):
    for line in film[idx]:
        if line[0] == '$':
            if len(emo[idx]) > 0:
                tmp_l = emo[idx]
                tmp_l.reverse()
                t2 = tmp_l.pop()
                e['Person'] = t2[0]
                e['emotion'] = t2[-1]
                # slug.append(e)
                tmp_l.reverse()
                emo[idx] = tmp_l
        else:
            tmp_p = plot[idx]
            tmp_p.reverse()
            t1 = tmp_p.pop()
            print(t1)
            slug.append(t1)
            tmp_p.reverse()
            plot[idx] = tmp_p
    mix_plot.append(slug)
    # break

for i in mix_plot:
    print(len(i))

