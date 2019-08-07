import numpy as np
import json
import os
import csv

source_path='RawData/'
output_file = 'metricResults.csv'

sourceCriteria = []
outputList = []
outputList.append(['matter','tag','fp','tp','tn','fn','pos_prec','neg_prec','pos_recall','neg_recall','f_pos', 'f_neg',
                                                   'weighted_precision','accuracy','timeStamp','pos_sig','tag_count'])

def loadData():
    global sourceCriteria
    global outputList

    beta = 0.5

    for subdir, dirs, files in os.walk(source_path):
        for file in files:
            if file != '.DS_Store':
                path = os.path.join(subdir, file)
                with open(path) as json_file:
                    data = json.load(json_file)
                listOfMatters = data['matters']
                for crit in sourceCriteria:
                    if crit[0] in listOfMatters.keys():
                        singleMatter = listOfMatters[crit[0]]
                        timeStamp = singleMatter['timestamp']
                        if 'perceived_acc' in singleMatter:
                            pa = singleMatter['perceived_acc']
                            if 'raw_data' in pa:
                                raw = pa['raw_data']
                                tag_count = raw['tags_included']
                        if 'latest_perceived_accuracies' in singleMatter:
                            lpa = singleMatter['latest_perceived_accuracies']
                            if crit[1] in lpa.keys():
                                tag = lpa[crit[1]]
                                fp = tag['fp']
                                tp = tag['tp']
                                tn = tag['tn']
                                fn = tag['fn']
                                pos_sig = tag['pos_signals']
                                tp_fp = tp + fp
                                tn_fp = tn + fp
                                tp_fn = tp + fn
                                tn_fn = tn + fn
                                tp_fp_fn_tn = fp + tp + tn + fn


                                if tp_fp == 0:
                                    pos_prec = 0
                                else:
                                    pos_prec = tp / tp_fp

                                if tn_fn == 0:
                                    neg_prec = 0
                                else:
                                    neg_prec = tn / tn_fn

                                if tp_fn == 0:
                                    pos_recall = 0
                                else:
                                    pos_recall = tp / tp_fn

                                if tn_fp == 0:
                                    neg_recall = 0
                                else:
                                    neg_recall = tn / tn_fp

                                f_denominator_pos = beta * beta * pos_prec + pos_recall
                                f_demoninator_neg = beta * beta * neg_prec + neg_recall

                                if f_denominator_pos == 0:
                                    f_pos = 0
                                else:
                                    f_pos = ((1 + beta * beta) * pos_prec * pos_recall) / f_denominator_pos

                                if f_demoninator_neg == 0:
                                    f_neg = 0
                                else:
                                    f_neg = ((1 + beta * beta) * neg_prec * neg_recall) / f_demoninator_neg

                                weighted_precision = 0.5 * (pos_prec + neg_prec)

                                if tp_fp_fn_tn == 0:
                                    accuracy = 0
                                else:
                                    accuracy = (tp + tn) / (tp_fp_fn_tn)

                                outputList.append([crit[0],crit[1],fp,tp,tn,fn,pos_prec,neg_prec,pos_recall,neg_recall,f_pos, f_neg,
                                                   weighted_precision,accuracy,timeStamp,pos_sig,tag_count])


def prepTarget():
    global sourceCriteria

    sourceCriteria.append(['330786289fa648f1b3dffc9ebd4faabd','Contracts'])
    sourceCriteria.append(['b7944ee16664495b93ae0e782f0bc2b8', 'Contract'])
    sourceCriteria.append(['48021eed5017445c9309b3a8444c830c', 'CV Contracts'])
    sourceCriteria.append(['361efa2d569943a187b5f30b9b5edcad', 'Contract'])
    sourceCriteria.append(['361efa2d569943a187b5f30b9b5edcad', 'Franchise Agreements and Franchise Disclosure Documents'])
    sourceCriteria.append(['361efa2d569943a187b5f30b9b5edcad', 'Employee Confidentiality or Non-Compete Agreement'])
    sourceCriteria.append(['361efa2d569943a187b5f30b9b5edcad', 'Franchise Agreements and Franchise Disclosure Documents'])
    sourceCriteria.append(['c53083e255874282875de28b29e71fae', 'License Agreement'])
    sourceCriteria.append(['5e1c4907e88b4b44a86e23a77106b730', 'Contracts'])
    sourceCriteria.append(['5e1c4907e88b4b44a86e23a77106b730', 'Sutter Contracts'])
    sourceCriteria.append(['5e1c4907e88b4b44a86e23a77106b730', 'Other Provider Contracts'])

def exportFile():
    with open(output_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(outputList)



def main():
    prepTarget()
    loadData()
    exportFile()

main()