import pandas as pd
import os
# import preparation.translator as translator
import preparation.translator as translator
import preparation.chassis_model as chassis_model
from sklearn.utils import shuffle

def LoadData():
    dirname = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_dir = os.path.join(dirname, 'data')
    raw_dir = os.path.join(dirname, 'rawdata')
    excel_data = pd.read_excel(os.path.join(raw_dir, "data.xlsx"), nrows = 20000, sheet_name='Sheet1')
    #print(excel_data['Sheet1'])
    df = pd.DataFrame(excel_data)
    #data = df['sheet1']
    data = []
    parts = []
    DATs = []
    STDs = []
    sentences = []
    targets = []
    data_from = []
    data_to = []
    i = 0
    '''
    df = shuffle(df)
    for row in df.itertuples():
        text = row[3]
        line_details = str(row[4]) + ', ' + str(row[5]) + ', ' + str(row[6]) + ', ' + str(row[7])  + ', ' + str(row[8])
        filtered_text = str(text).replace(',',' ').replace('nan','').strip()
        line_details_text = line_details.replace('nan','').strip()
        if(len(filtered_text) > 0 and len(line_details_text) > 0):
            parts.append(str(row[4]))
            DATs.append(str(row[5]))
            STDs.append(str(row[6]))
            sentences.append(text)
            target = str(row[4]) + ', ' + str(row[5]) + ', ' + str(row[6])
            if(int(row[7]) > 0): 
                target = target + ', Straight'
            if(int(row[8]) > 0):
                target = target + ', TextAmount'
            targets.append(target)
    '''
            #data.append((filtered_text, line_details_text))
    #vocab_to = CreateVocabTo(parts, DATs, STDs)
    #print(len(vocab_to))
    #print(vocab_to)
    ##################################
    #### Read from temp file #########
    with open('{}/{}'.format(data_dir, "data.raw.from"), 'r',
        encoding='utf-8', buffering=131072) as data_raw_from_in:
        lines = data_raw_from_in.readlines()
        for line in lines:
            data_from.append(line)
    with open('{}/{}'.format(data_dir, "data.from"), 'r',
        encoding='utf-8', buffering=131072) as data_from_in:
        lines_read = data_from_in.readlines()
    print(len(lines_read))
    data_from = data_from[len(lines_read):]
    data_from = FilterText(data_from)
    i = len(lines_read)
    ##################################
    #split text to translate because web api does not accept so long text
    '''
    data_from = FilterText(sentences)
    data_to = FilterTarget(targets)
    with open('{}/{}'.format(data_dir, "data.raw.from"), 'w', 
            encoding='utf-8', buffering=131072) as data_raw_from_file:
        data_raw_from_file.write("\n".join(data_from))

    new_lines = []
    for line in data_to:
        new_line = line.strip()
        new_lines.append(new_line)
    with open('{}/{}'.format(data_dir, "data.to"), 'w', 
            encoding='utf-8', buffering=131072) as data_to_file:
        data_to_file.write("\n".join(new_lines))
    '''
    data_from_en = []
    
    for item in data_from:
        print(i)
        print(item)
        translated_item = translator.translate([item])
        #print(translated_item)
        with open('{}/{}'.format(data_dir, "data.from"), 'a', 
            encoding='utf-8', buffering=131072) as data_from_file:
            data_from_file.write(translated_item[0])
            data_from_file.write("\n")
        data_from_en.extend(translated_item)
        i = i + 1
    ##################################
    #### Read from temp file #########
    # with open('{}/{}'.format(data_dir, "data.raw.to"), 'r',
    #     encoding='utf-8', buffering=131072) as data_raw_to_in:
    #     lines = data_raw_to_in.readlines()
    #     for line in lines:
    #         data_to.append(line)
    ##################################
    
    
    # count_data = len(sentences)
    # count_train = int(count_data * 0.7) # 70% to train
    # count_test = int(count_data * 0.2) # 20% to test
    # count_eval = count_data - count_train - count_test # 10% to eval
    # print(count_data, count_train, count_test, count_eval)
    # #Create train_from
    # train_from = data_from_en[:count_train]
    # train_from_filename = 'train.from'
    # with open('{}/{}'.format(data_dir, train_from_filename), 'w', 
    #         encoding='utf-8', buffering=131072) as train_from_file:
    #     train_from_file.write("\n".join(train_from))
    # #Create train_to
    # train_to = data_to[:count_train]
    # train_to_filename = 'train.to'
    # with open('{}/{}'.format(data_dir, train_to_filename), 'w', 
    #         encoding='utf-8', buffering=131072) as train_to_filename:
    #     train_to_filename.write("\n".join(train_to))
    
    # #Create test_from
    # test_from = data_from_en[count_train:count_train + count_test]
    # test_from_filename = 'test.from'
    # with open('{}/{}'.format(data_dir, test_from_filename), 'w', 
    #         encoding='utf-8', buffering=131072) as test_from_file:
    #     test_from_file.write("\n".join(test_from))
    # #Create test_to
    # test_to = data_to[count_train:count_train + count_test]
    # test_to_filename = 'test.to'
    # with open('{}/{}'.format(data_dir, test_to_filename), 'w', 
    #         encoding='utf-8', buffering=131072) as test_to_filename:
    #    test_to_filename.write("\n".join(test_to))
    # #Create eval_from
    # eval_from = data_from_en[count_train + count_test:]
    # eval_from_filename = 'eval.from'
    # with open('{}/{}'.format(data_dir, eval_from_filename), 'w', 
    #         encoding='utf-8', buffering=131072) as eval_from_file:
    #     eval_from_file.write("\n".join(eval_from))
    # #Create eval_to
    # eval_to = data_to[count_train + count_test:]
    # eval_to_filename = 'eval.to'
    # with open('{}/{}'.format(data_dir, eval_to_filename), 'w', 
    #         encoding='utf-8', buffering=131072) as eval_to_filename:
    #    eval_to_filename.write("\n".join(eval_to))
    print('Complete!')

def LoadChassisLineMatrix():
    dirname = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    raw_dir = os.path.join(dirname, 'rawdata')
    excel_data = pd.read_excel(os.path.join(raw_dir, "chassis_matrix.xlsx"), nrows = 20000, sheet_name='Sheet1')
    #print(excel_data['Sheet1'])
    df = pd.DataFrame(excel_data)
    chasis_list = []

    def populate_chassis_entity(parts, dats, stds, amount_count, straight_count,  chassis_entity):
            for part in parts:
                if(len(part.strip()) > 0):
                    chassis_entity.parts.append(part)
            for dat in dats:
                if(len(dat.strip()) > 0):
                    chassis_entity.dats.append(dat)
            for std in stds:
                if(len(std.strip()) > 0):
                    chassis_entity.stds.append(std)
            chassis_entity.amount += amount_count
            chassis_entity.straight += straight_count
            return chassis_entity

    for row in df.itertuples():
        chassis_number = str(row[3]).strip()
        #chassis_entity.chassis_number = str(row[3]).strip()
        chassis_model_number = chassis_number.split('-')[0]
        #chassis_model_number = chassis_number
        part_line = str(row[4]).replace('nan','').strip()
        dat_line = str(row[5]).replace('nan','').strip()
        std_line = str(row[6]).replace('nan','').strip()
        amount_count = int(row[7])
        straight_count = int(row[8])
        parts = part_line.split(',')
        dats = dat_line.split(',')
        stds = std_line.split(',')
        chassis_entity_list = list(filter(lambda x: x.chassis_model == chassis_model_number, chasis_list))
        if(len(chassis_entity_list) > 0):
            chassis_entity = chassis_entity_list[0]
            chasis_list.remove(chassis_entity)
            chassis_entity = populate_chassis_entity(parts, dats, stds, amount_count, straight_count, chassis_entity)
        else:
            chassis_entity = chassis_model.ChassisModel(chassis_model_number)
            chassis_entity = populate_chassis_entity(parts, dats, stds, amount_count, straight_count, chassis_entity)
        chasis_list.append(chassis_entity)

    return chasis_list

def CalculateConfidenceMarginByChassis(chasis_list, chassis, lineId, lineType):
    threshold = 10
    max_margin = 20
    result = 0
    chassis_entity_list = list(filter(lambda x: x.chassis_model == chassis, chasis_list))
    if(len(chassis_entity_list) == 0):
        result = -max_margin
    else:
        # total = len(chassis_entity_list[0].parts) + \
        #         len(chassis_entity_list[0].dats) + \
        #         len(chassis_entity_list[0].stds) + \
        #         chassis_entity_list[0].amount + chassis_entity_list[0].straight
        import math
        import numpy as np
        def tanh(x):
            return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

        if(lineType == 1):
            filtered_parts = list(filter(lambda x: x == lineId,chassis_entity_list[0].parts))
            line_count = len(filtered_parts)
        elif(lineType == 2):
            filtered_dats = list(filter(lambda x: x == lineId,chassis_entity_list[0].dats))
            line_count = len(filtered_dats)
        elif(lineType == 3):
            filtered_stds = list(filter(lambda x: x == lineId,chassis_entity_list[0].stds))
            line_count = len(filtered_stds)
        elif(lineType == 7):
            line_count = chassis_entity_list[0].amount
        elif(lineType == 4):
            line_count = chassis_entity_list[0].straight
        print(line_count)
        if (line_count <= 0):
            result = -max_margin
        else:
            result = tanh(math.log(line_count/threshold, threshold)) * max_margin
    return result

def FilterText(sentences):
    local_sentences = []
    for sentence in sentences:
        local_sentence = sentence.replace('＊', '').replace('※','').replace(',',' ').replace('nan','').replace('\n', ' ').replace('\u3000',' ').replace('◆',' ').replace('★',' ').replace('---', '').replace('•','').replace('\"','').replace('***', '').replace('(', '').replace(')','').replace('/',' ').strip()
        local_sentence = local_sentence.lower().replace('-month', ' month').replace('-months', ' month').replace('-monthes', ' month').replace(' months', ' month').replace(" monthes", " month")
        local_sentence = local_sentence.replace('-', ' ')
        local_sentences.append(local_sentence)

    return local_sentences

def FilterTarget(targets):
    local_targets = []
    for target in targets:
        local_target = target.replace('nan', '').replace(',',' ')
        local_targets.append(local_target)
    
    return local_targets

def FormatToFile():
    dirname = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_dir = os.path.join(dirname, 'data')
    to_filename = 'data.to'
    from_filename = 'data.from'
    lines = []
    new_lines = []
    with open('{}/{}'.format(data_dir, to_filename), 'r', 
            encoding='utf-8', buffering=131072) as to_in:
        lines = to_in.readlines()
    for line in lines:
        new_line = line.strip()
        new_lines.append(new_line)
    with open('{}/{}'.format(data_dir, to_filename), 'w', 
            encoding='utf-8', buffering=131072) as to_out:
        to_out.write("\n".join(new_lines))
        
    lines = []
    new_lines = []
    with open('{}/{}'.format(data_dir, from_filename), 'r', 
            encoding='utf-8', buffering=131072) as from_in:
        lines = from_in.readlines()
    for line in lines:
        new_line = line.strip()
        new_lines.append(new_line)
    new_lines = FilterText(new_lines)
    with open('{}/{}'.format(data_dir, from_filename), 'w', 
            encoding='utf-8', buffering=131072) as from_out:
        from_out.write("\n".join(new_lines))

# Prepare training data set
if __name__ == "__main__":
    # prepare()
    # LoadData()
    # FormatToFile()

    chassis_list = LoadChassisLineMatrix()
    print(len(chassis_list))
    index = 63
    for chassis in chassis_list:
        print(chassis.chassis_model, len(chassis.parts),len(chassis.dats), len(chassis.stds), chassis.amount, chassis.straight)
    print(chassis_list[index].chassis_model, len(chassis_list[index].parts),len(chassis_list[index].dats), len(chassis_list[index].stds), chassis_list[index].amount, chassis_list[index].straight)
    result = CalculateConfidenceMarginByChassis(chassis_list, 'CD48ZW', chassis_list[index].parts[0], 1)
    print(result)