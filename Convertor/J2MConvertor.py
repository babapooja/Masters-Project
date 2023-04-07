
from LexYacc.MProjectParser import parser
from pymongo import MongoClient
from itertools import product
from Configuration.Config import config_data
from Constants.ConsoleColors import cColors


class J2MConvertor(object):
    for_clauses = []
    return_clause = ''
    where_clauses = []
    input_query = ''

    def __init__(self, prompt) -> None:
        self.input_query = self.read_input(prompt)
        self.config = config_data
        # try:
        parsed_query = parser.parse(self.input_query)
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
                self.return_clause = clause

    # prepare the connection string based on the configuration for the MongoDB connection
    def prepare_connection_string(self):
        connString = 'mongodb://'
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

    # check condition value
    def check_condition(self, lhs_data, lhs_key, condition, rhs_data, rhs_key, join=False):
        final_res = []
        if condition == '$eq':
            if not join:
                for i in lhs_data:
                    if i.get(lhs_key):
                        if i[lhs_key] == rhs_key:
                            final_res.append(i)
            else:
                for i in lhs_data:
                    for j in rhs_data:
                        if i.get(lhs_key) and j.get(rhs_key):
                            if i[lhs_key] == j[rhs_key]:
                                final_res.append(
                                    self.cross_product([[i], [j]])[0])
        elif condition == '$gt':
            if not join:
                for i in lhs_data:
                    if i.get(lhs_key):
                        if i[lhs_key] > rhs_key:
                            final_res.append(i)
            else:
                for i in lhs_data:
                    for j in rhs_data:
                        if i.get(lhs_key) and j.get(rhs_key):
                            if i[lhs_key] > j[rhs_key]:
                                final_res.append(
                                    self.cross_product([[i], [j]])[0])
        elif condition == '$gte':
            if not join:
                for i in lhs_data:
                    if i.get(lhs_key):
                        if i[lhs_key] >= rhs_key:
                            final_res.append(i)
            else:
                for i in lhs_data:
                    for j in rhs_data:
                        if i.get(lhs_key) and j.get(rhs_key):
                            if i[lhs_key] >= j[rhs_key]:
                                final_res.append(
                                    self.cross_product([[i], [j]])[0])
        elif condition == '$lt':
            if not join:
                for i in lhs_data:
                    if i.get(lhs_key):
                        if i[lhs_key] <= rhs_key:
                            final_res.append(i)
            else:
                for i in lhs_data:
                    for j in rhs_data:
                        if i.get(lhs_key) and j.get(rhs_key):
                            if i[lhs_key] <= j[rhs_key]:
                                final_res.append(
                                    self.cross_product([[i], [j]])[0])
        elif condition == '$lte':
            if not join:
                for i in lhs_data:
                    if i.get(lhs_key):
                        if i[lhs_key] <= rhs_key:
                            final_res.append(i)
            else:
                for i in lhs_data:
                    for j in rhs_data:
                        if i.get(lhs_key) and j.get(rhs_key):
                            if i[lhs_key] <= j[rhs_key]:
                                final_res.append(
                                    self.cross_product([[i], [j]])[0])
        elif condition == '$ne':
            if not join:
                for i in lhs_data:
                    if i.get(lhs_key):
                        if i[lhs_key] != rhs_key:
                            final_res.append(i)
            else:
                for i in lhs_data:
                    for j in rhs_data:
                        if i.get(lhs_key) and j.get(rhs_key):
                            if i[lhs_key] != j[rhs_key]:
                                final_res.append(
                                    self.cross_product([[i], [j]])[0])

        return final_res
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
        # check for variables in the where clauses
        if self.where_clauses:
            exprs = self.where_clauses[1]
            for expr in exprs:
                if expr[1][0][0] not in declared_variables:
                    res['is_valid'] = False
                    res['message'] = f"Variable '{expr[1][0][0]}' is not declared."

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

    # wrapper function that calls all the checks listed above
    def check_semantic_errors(self) -> dict:
        validities = {
            'variables_check': self.check_for_variables()
        }
        print(f'{cColors.UNDERLINE}\nChecking for semantic errors{cColors.ENDC}')
        print(
            f'Variables validity: {validities["variables_check"]["message"]}')

        return (validities['variables_check']['is_valid'])
    ######################################### SEMANTIC ERRORS CHECK #########################################

    ######################################### Generate MONGODB query and fetch results #########################################
    def generate_mongoDB_query(self):
        # connection to mongodb database
        client = MongoClient(self.prepare_connection_string())
        db = client[self.config['database_name']]
        result = []

        # work on the WHERE calause if the where_clauses have been specified
        if len(self.where_clauses) >= 1:
            updated_query_response = self.handle_multiple_where_clauses(
                self.where_clauses[1], self.for_clauses[1], db)

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
                    if _ not in result:
                        result.append(_)

        return result
    ######################################### Generate MONGODB query and fetch results #########################################

    ######################################### HANDLE QUERY CLAUSES - FOR, WHERE, RETURN #########################################
    def handle_for_clauses(self, db):
        updated_query_response = []
        expressions = self.for_clauses[1]

        for expression in expressions:
            collection_name = expression[1][1].split('.')[0]
            collection = db[collection_name]
            query_response = list(collection.find({}))
            path_expressions = expression[1][2] if len(
                expression[1]) == 3 else []
            if len(path_expressions):
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
            else:
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
        elif type(return_clauses).__name__ == 'list':
            if type(query_data).__name__ == 'list':
                for qd in query_data:
                    # temp = []
                    return_data = None
                    if len(return_clauses) > 1:
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
                    else:
                        return_data = qd
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
        # return variable
        else:
            result = query_data
        return result

    def handle_multiple_where_clauses(self, where_clauses, expressions, db):
        all_data = result = {}
        last = ''
        for expression in expressions:
            collection_name = expression[1][1].split('.')[0]
            temp = list(db[collection_name].find({}))
            all_data[expression[1][0]] = temp

        # for data in all_data:
        for where_expression in where_clauses:
            if where_expression[0] == 'wexpr':
                tempr, templ = {}, {}
                exp = where_expression[1]
                lhs = exp[0]
                last = lhs_variable = lhs[0]

                condition = exp[1]
                rhs = exp[2]
                rhs_variable = rhs[0] if type(rhs).__name__ == 'list' else rhs
                # handle RHS of the expression
                if type(rhs).__name__ == 'list':
                    for x in rhs[1]:
                        if type(x).__name__ == 'str' and rhs[-1][-1] != x:
                            if not tempr:
                                if not result.get(rhs_variable):
                                    tempr = [data[x]
                                             for data in all_data[rhs_variable]]
                                elif result.get(rhs_variable):
                                    for data in result[rhs_variable]:
                                        tempr.append(data[x])
                            else:
                                tempr = tempr[x]

                # handle LHS of the expression
                for x in lhs[1]:
                    if type(x).__name__ == 'str' and lhs[-1][-1] != x:
                        if not templ:
                            if not result.get(lhs_variable):
                                templ = [data[x]
                                         for data in all_data[lhs_variable]]
                            elif result.get(lhs_variable):
                                for data in result[lhs_variable]:
                                    templ.append(data[x])
                        else:
                            templ = templ[x]
                if not templ:
                    templ = all_data[lhs_variable] if not result or not result.get(
                        lhs_variable) else result[lhs_variable]
                    if not result or not result.get(lhs_variable):
                        templ = all_data[lhs_variable]
                    else:
                        templ = result[lhs_variable]
                if not tempr:
                    if not result or not result.get(rhs_variable):
                        if type(rhs_variable).__name__ == 'str':
                            if '$' in rhs_variable:
                                tempr = all_data[rhs_variable]
                        else:
                            tempr = all_data[lhs_variable]
                    else:
                        tempr = result[rhs_variable]
                if type(rhs).__name__ == 'list':
                    rhs_key = rhs[-1][-1]
                    join = True
                else:
                    rhs_key = rhs
                    join = False

                result[lhs_variable] = self.check_condition(
                    templ, lhs[-1][-1], condition, tempr, rhs_key, join)

            elif where_expression[0] == 'contains':
                exp = where_expression[1]
                lhs, rhs, temp = exp[0], exp[1], []
                last = lhs[0]
                for x in lhs[1]:
                    if type(x).__name__ == 'str':
                        if not result.get(lhs[0]):
                            for data in all_data[lhs[0]]:
                                if type(data).__name__ == 'list':
                                    if rhs in data[x]:
                                        temp.append(data)
                                else:
                                    if rhs in data[x]:
                                        temp.append(data)
                        else:
                            for data in result[lhs[0]]:
                                if rhs in data[x]:
                                    temp.append(data)
                result[lhs[0]] = temp
        return result[last] if last else result


