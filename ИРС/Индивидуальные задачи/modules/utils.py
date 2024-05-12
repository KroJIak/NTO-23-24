import json

DB_FILE_PATH = 'sampleData.json'

def getSampleData(index):
    with open(DB_FILE_PATH) as file:
        dbData = json.load(file)
    return dbData[index].values()

def setSampleData(data):
    with open(DB_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# https://www.linuxcapable.com/install-python-3-8-on-ubuntu-linux