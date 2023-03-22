'''
QUERY:
    1. '
            for $x in json-lines("collection-answers.json").answers[]
            return
                {
                    "answer_id" : $x.answer_id,
                    "q_id" : $x.question_id
                };

        '
    2. '
            for $x in json-lines("collection-faq.json").faqs[]
            return $x.tags[1];

        '
    3. '
            for $question in json-lines("collection-faq.json").faqs[],
                $answer in json-lines("collection-answers.json").answers[]
            return
            {
                "question":$question.title,
                "answer_score":$answer.score
            };

        '
'''

'''
Questions to ask:
1. How to deteremine which database to choose in mongodb?
2. How to determine if the filename given inside json-lines exists or not? Or should it be there when user runs the program?
'''


from MProjectParser import parser
import json
import os
from pymongo import MongoClient
import pprint
from itertools import product
class Main(object):
    def __init__(self, prompt) -> None:
        self.input_query = self.read_input(prompt)
        self.parsed_query = parser.parse(self.input_query)
        self.collection_name = ''

    # Helper functions
    def readFile(self, filename):
        with open(filename, 'r') as f:
            file_content = json.load(f)
        return file_content

    # for multiple expressions in for, perform corss multiplication of the data
    def cross_product(self, data):
        final_result = []
        result = [list(tup) for tup in product(*data)]
        for res in result:
            temp = {}
            for item in res:
                temp.update(item)
            final_result.append(temp)
        return final_result

    # reading the query from the user
    def read_input(self, prompt):
        result = ''
        while True:
            data = ''
            if result == '':
                data = input(prompt+': ').strip()
            else:
                data = input('>>> ').strip()
            if ';' in data:
                i = data.index(';')
                result += data[0:i+1]
                break
            else:
                result += data + ' '
        return result[:-1]

    # file existance check
    def check_for_file(self):
        res = dict({"is_valid": True, "message": "File(s) found."})
        expressions = self.parsed_query[0][1]
        for expression in expressions:
            filename = expression[1][1]
            self.collection_name = filename.split('.')[0]
            # check if the file exists
            if not os.path.isfile(filename):
                res['is_valid'] = False
                res['message'] = f"File '{filename}' does not exist in the current directory."
                break
        return res

    # check for valid variables
    def check_for_variables(self):
        res = dict({"is_valid": True, "message": "Variables are valid"})
        expressions = self.parsed_query[0][1]
        return_expression = self.parsed_query[1][1]
        declared_variables = []
        # fetch the declared variables from the first part of the parsed query
        for expression in expressions:
            declared_variables.append(expression[1][0])
        # check for the variables in the return expression if present or not
        # if return expression is a variable and not a dictionary
        if return_expression[0] != '{':
            if return_expression[0] not in declared_variables:
                res['is_valid'] = False
                res['message'] = f"Variable '{return_expression[0]}' is not declared. Please check your query."
        # if the return expression is a dictionary
        elif return_expression[0] == '{':
            dict_values = return_expression[1]
            for value in dict_values:
                variable = value[1][0]
                if variable not in declared_variables:
                    res['is_valid'] = False
                    res['message'] = f"Variable '{variable}' is not declared. Please check your query."

        return res

    # check for valid file contents
    '''
    def check_for_file_contents(self):
        res = dict({"is_valid": True, "message": "File content(s) are valid."})
        expressions = self.parsed_query[0][1]
        # iterate over all the expressions
        for expression in expressions:
            filename = expression[1][1]
            file_contents = self.readFile(filename)
            path_expressions = expression[1][2]
            # iterate through the path expressions
            for path_expression in path_expressions:
                content_type = type(path_expression).__name__
                # if token is a string
                if content_type == 'str':
                    try:
                        file_contents = file_contents[path_expression]
                    except:
                        res['is_valid'] = False
                        res['message'] = f"'{path_expression}' is invalid. Please check your query."
                        break
                elif content_type == 'list':
                    try:
                        file_contents = file_contents[path_expression[0]]
                        if type(file_contents).__name__ == 'list':
                            # only if the index is a number else the contents remain as is
                            if path_expression[1] != '':
                                file_contents = file_contents[path_expression[1]]
                        else:
                            res['is_valid'] = False
                            res['message'] = f"'{path_expression[0]}' is not an array in {filename}"
                            break
                    except:
                        res['is_valid'] = False
                        res['message'] = f"'{path_expression}' is invalid. Please check your query."
                        break
        return res
        '''

    # wrapper function that calls all the checks listed above
    def check_semantic_errors(self) -> dict:
        print('Checking for semantic errors...')
        print('--------------------------------')
        print(f'File validity: {self.check_for_file()["message"]}')
        print(
            f'File content(s) validity: {self.check_for_file_contents()["message"]}')
        print(f'Variables validity: {self.check_for_variables()["message"]}')

    # generate mongodb query
    def generate_mongoDB_query(self):
        # connection to mongodb database
        client = MongoClient()
        # how will we understand which database to use??
        db = client.jsoniq
        expressions = self.parsed_query[0][1]
        result = []
        updated_query_response = []
        for expression in expressions:
            collection_name = expression[1][1].split('.')[0]
            collection = db[collection_name]
            query_response = list(collection.find({}))
            path_expressions = expression[1][2]
            for path_expression in path_expressions:
                if type(path_expression).__name__ == 'list':
                    if query_response[0].__contains__(path_expression[0]):
                        if type(query_response[0][path_expression[0]]).__name__ == 'list':
                            if path_expression[1] != '':
                                query_response = query_response[0][path_expression[0]
                                                                   ][path_expression[1]]
                            else:
                                query_response = query_response[0][path_expression[0]]
                    if path_expression[1] != '':
                        query_response = query_response[path_expression[1]]
                else:
                    # for qr in query_response:
                    #     temp.append(qr[path_expression])
                    query_response = query_response[path_expression]
            updated_query_response.append(query_response)

        if len(updated_query_response) > 1:
            updated_query_response = self.cross_product(updated_query_response)


        # generating the answer
        if type(updated_query_response).__name__ == 'list':
            for qr in updated_query_response:
                return_data = self.generate_return_data(qr)
                for _ in return_data:
                    result.append(_)
        # else:
        #     return_data = self.generate_return_data(updated_query_response['value'], updated_query_response['var'])
        #     for _ in return_data:
        #         result.append(_)

        return result

    # form the return data
    def generate_return_data(self, query_data):
        result = []
        return_clauses = self.parsed_query[1][1]
        # returning a dictionary
        if return_clauses[0] == '{':
            if type(query_data).__name__ == 'list':
                for qd in query_data:
                    temp = {}
                    for return_clause in return_clauses[1]:
                        # print(return_clause)
                        data = None
                        for x in return_clause[1][1]:
                            if not data:
                                data = qd[x]
                            else:
                                data = data[x]
                        temp[return_clause[0]] = data
                    result.append(temp)
            else:
                temp = {}
                for return_clause in return_clauses[1]:
                    data = None
                    for x in return_clause[1][1]:
                        if not data:
                            data = query_data[x]
                        else:
                            data = data[x]
                    temp[return_clause[0]] = data
                result.append(temp)
        # returning a list
        else:
            if type(query_data).__name__ == 'list':
                for qd in query_data:
                    # temp = []
                    return_data = None
                    for return_clause in return_clauses[1]:
                        if type(return_clause).__name__ == 'list':
                            if not return_data:
                                return_data = qd[return_clause[0]][return_clause[1]]
                            else:
                                return_data = return_data[rc]
                        else:
                            if not return_data:
                                return_data = qd[return_clause]
                            else:
                                return_data = return_data[return_clause]
                    result.append(return_data)
            else:
                return_data = None
                for return_clause in return_clauses[1]:
                    if type(return_clause).__name__ == 'list':
                        for rc in return_clause[1]:
                            if not return_data:
                                return_data = query_data[rc]
                            else:
                                return_data = return_data[rc]
                    else:
                        if not return_data:
                            return_data = query_data[return_clause]
                        else:
                            return_data = return_data[return_clause]

                result.append(return_data)
        return result


mainObj = Main("Enter an input query")
mainObj.check_for_file()
# mainObj.check_semantic_errors()
print('Fetched Data...')
pprint.pprint(mainObj.generate_mongoDB_query())
