import os
import pandas as pd
import time
import numpy as np


def list_files(directory, extension):
    return_files = []

    for f in os.listdir(directory):
        if f.endswith('.' + extension):
            return_files.append(f)
    return return_files


def readJSON_batch(directory):
    files = list_files(directory, 'json')
    df_list = []

    print('Total: ', len(files), ' batches')

    for (sno, fileName) in enumerate(files, 1):
        print('Appending batch ', sno)
        df = pd.read_json(directory + '/' + fileName)
        df_list.append(df)
    allItems = pd.concat(df_list, ignore_index=True)

    return allItems


def splitSave(df, directory, batchSize=500000):
    # Make sure directory exists
    if (not os.path.isdir(directory)):
        os.mkdir(directory)

    # Check if data needs to use batch
    dataLength = df.shape[0]

    if dataLength < batchSize:
        # Congrats, you don't need to use batch
        name = 'batch'
        fileSave = directory + '/' + name + '.json'

        isExisted = os.path.exists(fileSave)

        if (isExisted):
            addTime = int(np.ceil(time.time()))
            fileSave = directory + '/' + name + "-" + str(addTime) + '.json'

        print('Saving to file: ', fileSave)

        with open(fileSave, 'w', encoding='utf-8') as f:
            df.to_json(f, orient='records', force_ascii=False)

        print('Done saving')
    else:
        # Save to batches
        numberOfFiles = int(np.ceil(df.shape[0]/batchSize))

        print('Saving to ', numberOfFiles, 'files')

        for i in range(0, numberOfFiles):
            batch = df.iloc[batchSize*i:(i+1)*batchSize] if i != numberOfFiles - \
                1 else df[batchSize*(numberOfFiles-1):]

            name = 'batch' + str(i+1)
            fileSave = directory + '/' + name + '.json'

            isExisted = os.path.exists(fileSave)

            if (isExisted):
                addTime = int(np.ceil(time.time()))
                fileSave = directory + "/" + name + \
                    "-" + str(addTime) + '.json'

            print(fileSave)

            with open(fileSave, 'w', encoding='utf-8') as f:
                batch.to_json(f, orient='records', force_ascii=False)
        print('Done saving')
