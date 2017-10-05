def output_newlines(file_in, file_out):
    import json
    
    # load json file
    with open('/Users/saraszczepanski/workspace/insight_project/data/{}'.format(file_in)) as f:
        data = json.load(f)

    with open('/Users/saraszczepanski/workspace/insight_project/data/{}'.format(file_out), 'w') as out:
        for line in data:
            json.dump(line, out)
            out.write(',\n')