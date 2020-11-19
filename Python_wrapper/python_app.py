from wrapper import query_1, query_2, query_3, query_4, query_5, query_6, query_7, \
initialize_database, add_funda_data, write_own_sql_query, add_tourist_info_to_database, \
correlation_housing_data_sellingprice_sellingtime, correlation_analysis_nlp, \
correlation_tourist_info_analysis, text_search
from NLP_Python import fundaNlpAnalysisFunc

# This is the script to interact with all the functions we created
# © Robin Kratschmayr

print('WELCOME TO YOUR FUNDA ANALYSIS APPLICATION')
print('What do you want to do?')

userinput = 'started'

while str(userinput)!='stop':
    print('####################################################################################################')
    print('Please type a number from the menu below or type "stop" to exit')
    print('1. Initialize database')
    print('2. Add more funda data')
    print('3. Run analysis querys')
    print('4. Run NLP analysis')
    print('5. Show correlations')
    print('6. Plot some results')
    print('7. Write your own SQL Query')
    print('8. Do some text search')
    userinput = input("Please type a number from the menu above or type 'stop' to exit")
    print('####################################################################################################')

    if userinput == 'started':
        print('')
    elif userinput == '1':
        initialize_database()
    elif userinput == '2':
        add_funda_data()
    elif userinput == '3':
        print('Which Query do you want to run?')
        print('1. Average asking Price per month for each of the municipalitys')
        print('2. Average asking Price per Agegroupcategory')
        print('3. Average asking Price per month for each of the municipalitys')
        print('4. Percentage increase/decrease per gemeente per month')
        print('5. Average asking Price per month for each of the municipalitys')
        print('6. Average asking Price per month for each of the municipalitys')
        print('7. Average asking Price per month for each of the municipalitys')
        print('8. Average asking Price per month for each of the municipalitys')
        other_userinput = input('Type the number here: ')
        print('################## RESULTS #################')
        if other_userinput == '1':
            query_1()
        elif other_userinput == '2':
            query_2()
        elif other_userinput == '3':
            query_3()
        elif other_userinput == '4':
            query_4()
        elif other_userinput == '5':
            query_5()
        elif other_userinput == '6':
            query_6()
        elif other_userinput == '7':
            query_7()
        elif other_userinput == '8':
            query_8()
        input('Type anything to go back to main menu: ')
    elif userinput == '4':
        fundaNlpAnalysisFunc()
    elif userinput == '5':
        print('Which correletaion do you want to see?')
        print('1. Correlations within the Funda data')
        print('2. Correlations between sellingtime/price and the tourist_data')
        print('3. Correlations between sellingtime/price and the crime_data')
        print('4. Correlations between sellingtime/price and the labour_data')
        print('5. Correlations between sellingtime/price and the NLP analysis')
        other_userinput = input('Type the number here: ')
        if other_userinput == '1':
            correlation_housing_data_sellingprice_sellingtime()
        elif other_userinput == '2':
            correlation_tourist_info_analysis()
        elif other_userinput == '3':
            query_3()
        elif other_userinput == '4':
            query_4()
        elif other_userinput == '5':
            correlation_analysis_nlp()
        input('Type anything to go back to main menu: ')
    elif userinput == '6':
        print('6')
    elif userinput == '7':
        write_own_sql_query()
    elif userinput == '8':
        text_search()
    elif userinput == 'stop':
        print('Stopped')
    else:
        print('Invalid Input')