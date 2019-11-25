import pandas as pd
# import tensorflow as tf
import os
import sys
#import argparse
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
from config import hparams, out_dir
from model import argument_parser
from inference import *
from data_access.order_repository import *
from data_access.part_repository import PartRepository
from data_access.package_repository import PackageRepository
from data_access.vehicle_repository import VehicleRepository
# from preparation.prepare_data import Prepare
from preparation.process_rawdata import LoadChassisLineMatrix, CalculateConfidenceMarginByChassis
# from utils.tokenizer import tokenize, detokenize
# from utils.sentence import score_answers, replace_in_answers
# import nltk
# from nltk.tokenize import WordPunctTokenizer
# from nltk.tokenize import TweetTokenizer
# from nltk.corpus import wordnet as wn
# from nltk.stem.wordnet import WordNetLemmatizer
app = Flask(__name__)
CORS(app)

@app.route('/getorderlines', methods=['POST'])
def getorderlines():
    data = request.data
    param_str = data.decode()
    params = param_str.split('&')
    part_connector = PartRepository()
    package_connector = PackageRepository()
    vehicle_connector = VehicleRepository()
    real_params = []
    for param in params:
        tmp = param.split('=')
        real_params.append(tmp[1])
    print(real_params)
    note = real_params[0]
    chassis = real_params[1]
    note = note.replace('%20', ' ')
    answers = inference([note])
    # print(note)
    answers = rank(answers["answers"])
    # print(answers)
    results = []
    parts, dats, stds = CreateLineIndex()
    chassis_list = LoadChassisLineMatrix()
    for answer in answers:
        linetype = 0
        description = ""
        if str(answer[0]) in parts:
            linetype = 1
            try:
                description = part_connector.GetPartDetail(str(answer[0]))[0]
                elastic_confidence = CalculateConfidenceMarginByChassis(
                    chassis_list, chassis, str(answer[0]), linetype)
            except:
                pass
        elif str(answer[0]) in dats:
            linetype = 2
            try:
                description = package_connector.GetDATDetail(str(answer[0]))[0]
                elastic_confidence = CalculateConfidenceMarginByChassis(
                    chassis_list, chassis, str(answer[0]), linetype)
            except:
                pass
        elif str(answer[0]) in stds:
            linetype = 3
            try:
                description = vehicle_connector.GetSTDDetail(str(answer[0]))[0]
                elastic_confidence = CalculateConfidenceMarginByChassis(
                    chassis_list, chassis, str(answer[0]), linetype)
            except:
                pass
        elif str(answer[0]) == "Straight":
            linetype = 4
            description = 'Straight'
            elastic_confidence = CalculateConfidenceMarginByChassis(
                chassis_list, chassis, description, linetype)
        elif str(answer[0]) == "TextAmount":
            linetype = 7
            description = 'TextAmount'
            elastic_confidence = CalculateConfidenceMarginByChassis(
                chassis_list, chassis, description, linetype)
        confidence = answer[1] + elastic_confidence
        if (confidence > 100):
            confidence = 100
        results.append({
            'linetype': linetype,
            'id': answer[0],
            'description': description,
            'confidence': confidence
        })

    results = sorted(results,
                     key=lambda result: result['confidence'],
                     reverse=True)
    results = list(filter(lambda result: result['confidence'] > 0, results))
    print(results)
    # print(jsonify(results))
    return jsonify(results)


def CreateLineIndex():
    dirname = os.path.dirname(os.path.realpath(__file__))
    raw_dir = os.path.join(dirname, 'rawdata')
    excel_data = pd.read_excel(os.path.join(raw_dir, "data.xlsx"),
                               nrows=20000,
                               sheet_name='Sheet1')
    # print(excel_data['Sheet1'])
    df = pd.DataFrame(excel_data)
    # data = df['sheet1']
    parts = []
    dats = []
    stds = []

    for row in df.itertuples():
        text = row[3]
        line_details = str(row[4]) + ', ' + str(row[5]) + ', ' + str(
            row[6]) + ', ' + str(row[7]) + ', ' + str(row[8])
        filtered_text = str(text).replace(',', ' ').replace('nan', '').strip()
        line_details_text = line_details.replace('nan', '').strip()
        if (len(filtered_text) > 0 and len(line_details_text) > 0):
            parts.extend(str(row[4]).split(','))
            dats.extend(str(row[5]).split(','))
            stds.extend(str(row[6]).split(','))
    ##################################

    return parts, dats, stds


if __name__ == "__main__":
    '''
    main()
    LoadData()
    FormatToFile()
    Prepare()
    '''
    # answers = inference(["regular inspection"])
    # #print(answers["answers"])
    # answers = rank(answers["answers"])
    # for answer in answers:
    #     print('[%s] with %.2f percent' %(answer[0], answer[1]))
    # print(answers)

    app.run()
    # get_chassis_matrix()
