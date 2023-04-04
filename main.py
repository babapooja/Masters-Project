'''
QUERY:
    1. '
            FOR $x in json-lines('collection-answers.json').answers[]
            return
                {
                    "answer_id" : $x.answer_id,
                    "q_id" : $x.question_id
                };

        '
    2. '
            for $x in json-lines('collection-faq.json').faqs[]
            return $x.tags[1];

        '
    3. '
            for $question in json-lines('collection-faq.json').faqs[],
                $answer in json-lines(collection-answers.json').answers[]
            return
            {
                "question":$question.title,
                "answer_score":$answer.score
            };

        '
    4. ' 
            for $question in json-lines('collection-faq.json').faqs[],
                $answer in json-lines(collection-answers.json').answers[]
            where $question.question_id eq $answer.question_id
            return
            {
                "question":$question.title,
                "answer_score":$answer.score
            };

        '
    5. '    
            for $question in json-lines('collection-faq.json').faqs[],
                $answer in json-lines(collection-answers.json').answers[]
            where $question.question_id eq $answer.question_id and 
                $answer.answer_id eq $answer.answer_id
                $answer.answer_id eq $answer.answer_id
            return
            {
                "question":$question.title,
                "answer_score":$answer.score
            };

        '
    6. '
            for $answer in json-lines(collection-answers.json').answers[]
            where $answer.score ge 4
            return $answer.question_id;

        '
    7. '
            for $faq in json-lines('collection-faq.json').faqs[]
            where $faq.title eq "Databases"
            return $faq.tags;

        '
    8. '
            for $question in json-lines('collection-faq.json').faqs[]
            where contains($question.title, "MySQL")
            return
            {
                "question":$question.title
            };

    '
'''

from MProjectParser import parser
import json
import os
from pymongo import MongoClient
import pprint
from itertools import product
from Config import config_data
from ConsoleColors import cColors


class Main(object):
    for_clauses = []
    return_clause = ''
    where_clauses = []
    input_query = ''

    def __init__(self, prompt) -> None:
        self.input_query = self.read_input(prompt)
        self.config = config_data
        # try:
        parsed_query = parser.parse(self.input_query)
        # print(parsed_query)
        # segregate the for clauses, where clauses, and the return clause
        self.segregate_clauses(parsed_query)
        # except:
        #     print('There is syntax error. Please resolve it and try again.\n')

    ######################################### HELPER FUNCTIONS #########################################
    # segregate clauses
    def segregate_clauses(self, parsed_query):
        for clause in parsed_query:
            if clause[0] == 'for':
                self.for_clauses = clause
            elif clause[0] == 'where':
                self.where_clauses = clause
            elif clause[0] == 'return':
                self.return_clauses = clause

    # prepare the connection string based on the configuration for the MongoDB connection
    def prepare_connection_string(self):
        connString = 'mongodb://'
        print(self.config)
        if self.config['username'] != '' and self.config['password'] != '':
            connString += self.config['username'] + \
                ":" + self.config['password'] + "@"
        if self.config['hostname'] != '':
            connString += self.config['hostname']
            if self.config['port'] != '':
                connString += ":" + self.config['port']
        return connString

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

    ######################################### HELPER FUNCTIONS #########################################

    ######################################### SEMANTIC ERRORS CHECK #########################################

    # check if variables are declared earlier
    def check_for_variables(self):
        res = dict({"is_valid": True, "message": "Variables are valid"})
        expressions = self.for_clauses[1]
        return_expression = self.return_clause[1]
        declared_variables = []
        # fetch the declared variables from the first part of the parsed query
        for expression in expressions:
            declared_variables.append(expression[1][0])
        # check for the variables in the return expression if present or not
        # if return expression is a variable and not a dictionary
        if return_expression[0] != '{':
            if return_expression[0] not in declared_variables:
                res['is_valid'] = False
                res['message'] = f"Variable '{return_expression[0]}' is not declared."
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
        expressions = self.for_clauses[1]
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
        validities = {
            # 'file_check': self.check_for_file(),
            'variables_check': self.check_for_variables()
        }
        print(f'{cColors.UNDERLINE}\nChecking for semantic errors{cColors.ENDC}')
        # print(f'File validity: {validities["file_check"]["message"]}')
        # print(
        #     f'File content(s) validity: {self.check_for_file_contents()["message"]}')
        print(
            f'Variables validity: {validities["variables_check"]["message"]}')

        return (validities['variables_check']['is_valid'])
        # and validities['file_check']['is_valid'] )
    ######################################### SEMANTIC ERRORS CHECK #########################################

    ######################################### Generate MONGODB query and fetch results #########################################
    def generate_mongoDB_query(self):
        # connection to mongodb database
        client = MongoClient(self.prepare_connection_string())
        db = client[self.config['database_name']]
        result = []

        # work on the WHERE calause if the where_clauses have been specified
        if len(self.where_clauses) >= 1:
            updated_query_response = self.handle_where_clause(db)

        # work on the FOR clause
        if not len(self.where_clauses):
            updated_query_response = self.handle_for_clauses(db)

        if len(updated_query_response) > 1 and not len(self.where_clauses):
            updated_query_response = self.cross_product(updated_query_response)

        # work on the RETURN clause
        if type(updated_query_response).__name__ == 'list':
            for qr in updated_query_response:
                return_data = self.handle_return_clause(qr)
                for _ in return_data:
                    result.append(_)
        # else:
        #     return_data = self.generate_return_data(updated_query_response['value'], updated_query_response['var'])
        #     for _ in return_data:
        #         result.append(_)

        return result
    ######################################### Generate MONGODB query and fetch results #########################################

    ######################################### HANDLE QUERY CLAUSES - FOR, WHERE, RETURN #########################################
    def handle_for_clauses(self, db):
        updated_query_response = []
        expressions = self.for_clauses[1]

        for expression in expressions:
            collection_name = expression[1][1].split('.')[0]
            collection = db[collection_name]
            # if len(self.where_clauses):
            #     query = self.handle_where_clause(expressions)
            #     updated_query_response = list(collection.find(query))
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
                    query_response = query_response[path_expression]
            updated_query_response.append(query_response)
        return updated_query_response

    def handle_return_clause(self, query_data):
        result = []
        return_clauses = self.return_clause[1]
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
                                return_data = qd[return_clause[0]
                                                 ][return_clause[1]]
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

    def handle_multiple_where_clauses(self, where_clauses, expressions, db):
        query_response = []

        return query_response

    def handle_where_clause(self, db):
        where_clauses = self.where_clauses[1]
        expressions = self.for_clauses[1]
        mongoCollection = {}
        query_response = []
        for expression in expressions:
            collection_name = expression[1][1].split('.')[0]
            variable = expression[1][0]
            mongoCollection[collection_name] = []

            if len(where_clauses) == 1:
                where_clause = where_clauses[0]
                if where_clause[0] == 'wexpr':
                    lhs_query_str = ''
                    rhs_query_str = ''
                    lhs = where_clause[1][0]
                    condition = where_clause[1][1]
                    rhs = where_clause[1][2]
                    for x in lhs[1]:
                        if type(x).__name__ == 'str':
                            lhs_query_str += x
                        else:
                            lhs_query_str += x[0]
                    if where_clause[1][0][0] == variable:
                        mongoCollection[collection_name] = lhs_query_str

                    if type(rhs).__name__ == 'str' or type(rhs).__name__ == 'int':
                        query = {lhs_query_str: {condition: rhs}}
                        query_response = list(db[collection_name].find(query))
                        break
                    elif type(rhs).__name__ == 'list':
                        for x in rhs[1]:
                            if type(x).__name__ == 'str':
                                rhs_query_str += x
                            else:
                                rhs_query_str += x[0]
                        if where_clause[1][2][0] == variable:
                            mongoCollection[collection_name] = rhs_query_str

                elif where_clause[0] == 'contains':
                    lhs = where_clause[1][0]
                    rhs = where_clause[1][1]
                    for x in lhs[1]:
                        if type(x).__name__ == 'str':
                            query_str += x
                        else:
                            query_str += x[0]
                    query = {query_str: {'$regex': rhs.replace('"', '')}}
                    query_response = list(db[collection_name].find(query))

        if len(where_clauses) == 1 and where_clauses[0][0] != 'contains' and type(where_clauses[0][1][2]).__name__ not in ('str', 'int'):
            _keys = list(mongoCollection.keys())
            if len(_keys) > 1:
                q = {
                    '$lookup': {
                        'from': _keys[1],
                        'localField': mongoCollection[_keys[0]],
                        'foreignField': mongoCollection[_keys[1]],
                        'as': 'joinedResult'
                    }
                }
                query_response = list(db[_keys[0]].aggregate([q]))
            else:
                q = {
                    '$lookup': {
                        'from': _keys[0],
                        'localField': mongoCollection[_keys[0]],
                        'foreignField': mongoCollection[_keys[0]],
                        'as': 'joinedResult'
                    }
                }
                query_response = list(db[_keys[0]].aggregate([q]))
        else:
            query_response = self.handle_multiple_where_clauses(
                where_clauses, expressions, db)

        return query_response

    ######################################### HANDLE QUERY CLAUSES - FOR, WHERE, RETURN #########################################


######################################### ENTRY POINT #########################################
if __name__ == '__main__':
    print(f'''{cColors.OKBLUE}
    -----------------------------------------------------------------------------------------------------------------------
    Enter the input query in JSONiq starting from the next line. To mark the end of the input query, add ';' at the end.
    To run the query, press enter.
    -----------------------------------------------------------------------------------------------------------------------{cColors.ENDC}
    ''')
    mainObj = Main("Enter an input query")
    # mainObj.check_for_file()
    pprint.pprint(mainObj.generate_mongoDB_query())
    # if mainObj.check_semantic_errors():
    #     print(f'{cColors.UNDERLINE}\nResults for above query{cColors.ENDC}')
    #     pprint.pprint(mainObj.generate_mongoDB_query())
    #     print(f'{cColors.OKGREEN}\nFetched data successfully...\n\n{cColors.ENDC}')
    # else:
    #     print(
    #         f'{cColors.FAIL}\n\nError(s) found in the input query. Please check your query for the above errors.\n\n{cColors.ENDC}')
