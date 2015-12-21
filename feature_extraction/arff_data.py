import arff

#list of attributes
arff_writer = arff.Writer(feature_example, relation = 'Review_sentiment',
                            header_names = ['token_number',
                                            'type_number',
                                            'overall_sentiment',
                                            'adjective_sentiment',
                                            'verb_sentiment',
                                            'noun_sentiment',
                                            'keyword_sentiment',
                                            'stars'])
                                            
arff_writer.pytypes[arff.numeric] = '{1,2,3,4,5}'
arff_writer.write([arff.nominal('stars')])


#formate data from feature_example
def write_to_list(feature_example):
    data_input = []
    arff_data = []
    with open('feature_example') as feature_example:
        for line in feature_example:
            data_input.append(line.strip().split(','))
    for lists in data_input:
        for attribute_triple in lists:
            triple_list = attribute_triple.split()
        arff_data.append(triple_list)
    return arff_data
    
arff.dump(open(feature_example, 'w'), arff_data,
                                    relation = 'Review_sentiment',
                                    header_names)
        

    
