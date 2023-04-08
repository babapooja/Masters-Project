from Constants.ConsoleColors import cColors
from Converter.J2MConverter import J2MConverter
import pprint
if __name__ == '__main__':
    print(f'''{cColors.OKBLUE}
-----------------------------------------------------------------------------------------------------------------------
Enter the input query in JSONiq starting from the next line. To mark the end of the input query, add ';' at the end.
To run the query, press enter.
-----------------------------------------------------------------------------------------------------------------------{cColors.ENDC}
    ''')
    mainObj = J2MConverter("Enter an input query")
    try:
        if mainObj.check_semantic_errors():
            print(f'{cColors.UNDERLINE}\nResults for above query{cColors.ENDC}')
            pprint.pprint(mainObj.generate_mongoDB_query())
            print(f'{cColors.OKGREEN}\nFetched data successfully...\n\n{cColors.ENDC}')
        else:
            print(
                f'{cColors.FAIL}\n\nError(s) found in the input query. Please check your query for the above errors.\n\n{cColors.ENDC}')
    except:
        print(
                f'{cColors.FAIL}\n\nError(s) found in the input query. Please check your query for the above errors.\n\n{cColors.ENDC}')