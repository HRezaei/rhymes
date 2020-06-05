
def read_file(path):
    file = open(path, "r")
    content = file.read()
    return content


def json_write(data, path):
    import json
    file = open(path, "w+")
    json.dump(data, file, ensure_ascii=False)
    file.close()
    return True


def json_read(path):
    import json
    file = open(path, "r")
    data = json.load(file)
    file.close()
    return data