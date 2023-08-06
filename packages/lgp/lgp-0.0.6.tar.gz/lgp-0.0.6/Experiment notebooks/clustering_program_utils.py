import pandas as pd
import matplotlib.pyplot as plt
import re

def convert_program_str_repr(model, names):
    # convert the raw string to user friendly string
    s = ''
    original_str = model.bestEffProgStr_.splitlines()
    i = 0
    indentation = False
    indentation_level = 1
    connecting_list = []
    s = s + "The default value of r0: " + str(round(model.register_[model.numberOfInput], 2)) + "\nModels:\n"
    while i < len(original_str):
        current_string = original_str[i]
        vars_in_line = re.findall(r'r\d+', current_string)
        # reformat structure
        if 'if' not in current_string:
            extract = [x.strip() for x in current_string.split(',')]
            current_string = extract[0][:3] + ' '+ extract[1] + ' = ' +  extract[2] + ' ' + extract[0][-1] + ' ' + extract[3][:-1]
        # substitute variable index
        for var in vars_in_line:
            var = var[1:]
            if var not in connecting_list: # not a connecting calculation variable
                if int(var) < model.numberOfVariable and int(var) != 0: # var is calculation variable
                    if (i+1 < len(original_str)) and var in ( [i[1:] for i in re.findall(r'r\d+', original_str[i+1])] ):
                        # a calculation variable connecting the two lines in a program
                        connecting_list.append(var)
                    else: # calculation variable is a constant
                        current_string = re.sub('r' + re.escape(var), str(round(model.register_[int(var)], 2)),
                                            current_string)
                elif int(var) >= model.numberOfVariable and int(var) != 0: # features
                    name_index = int(var) - model.numberOfVariable
                    current_string = re.sub('r' + re.escape(var), str(names[name_index]), current_string)
        # take care of indentation
        if indentation:
            current_string = current_string[:3] + indentation_level*'  ' + 'then ' + current_string[3:]
        if 'if' in current_string:
            indentation = True
            indentation_level += 1
        else:
            indentation = False
        s += current_string + '\n'
        i += 1
    s += 'Output register r[0] will then go through sigmoid transformation S \nif S(r[0]) is less or equal ' \
         'than 0.5:\n  this sample will be classified by this model as class 0, i.e. diseased. \nelse:\n' \
         '  class 1, i.e. healthy'
    return s




# draw Number of effective instructions VS num_of_eff_features graph
def eff_vs_numOfEffFeature_graph(program_length_list, num_of_eff_features, accuracy):
    d = {'Number of effective instructions': program_length_list, 'Number of effective feature': num_of_eff_features,
         'accuracy': accuracy}
    df_h = pd.DataFrame(d)
    temp = df_h.groupby(['Number of effective instructions', 'Number of effective feature']).size().reset_index(name='count')
    df_h = df_h.merge(temp,  how='left')
    # draw complete
    plt.scatter(x=df_h["Number of effective instructions"], y=df_h["Number of effective feature"], c=df_h['accuracy'].apply(lambda x: x*100),
                s=df_h['count'], cmap='Reds')
    plt.ylim((0, 10))
    plt.xlim((0, 10))
    plt.xlabel("Number of effective instructions", fontsize=12)
    plt.ylabel("Number of effective features", fontsize=12)
    plt.colorbar()
    plt.savefig('program_lengh_vs_feature.jpeg', dpi=300, format='JPEG')