import spacy
import pandas.io.sql as sqlio
import pandas as pd
import psycopg2
import mysql.connector
from spacy.lang.nl.stop_words import STOP_WORDS


def fundaNlpAnalysisFunc (year):
    #create connection to the databae
    #change the credentials in the db_login file before running for the first time
    with open ('db_login.txt', 'r') as myfile:
        data = myfile.read()
    conn = psycopg2.connect(data)
    cur = conn.cursor()

    # Select the first 100 rows in the funda table and fetch them to a list object
    executing_script = "SELECT globalId, fullDescription FROM funda_"+str(year)+" limit 500;"
    funda = sqlio.read_sql_query(executing_script, conn)

    nlp = spacy.load("nl")
    funda_analysis = pd.DataFrame(columns=['globalId','descriptionLength', 'NOUN', 'ADJ', 'VERB', 'ADV','REL_NOUN','REL_ADJ','REL_VERB','REL_ADV','EMAILS', 'URLS', 'NUMBERS','CURRENCY', 'AVG_SENTIMENT', 'lexeme_1','lexeme_2','lexeme_3','lexeme_4','lexeme_5','lexeme_6','lexeme_7','lexeme_8','lexeme_9','lexeme_10','lexeme_dict',])

    for idx, entry in funda.iterrows():
        document = nlp(entry['fulldescription'])

        #calculate the different parameters
        description_length = len(entry['fulldescription'].split())
        emails = []
        urls = []
        sentiment = []
        num = []
        currency = []
        NOUNS = []
        ADVS = []
        VERBS = []
        ADJS = []

        # filtering stop words
        for word in document:
            if word.is_stop==False | word.is_punct == False | word.is_space == False:
                sentiment.append(word.sentiment)
            if word.like_email==True:
                emails.append(word)
            if word.like_url==True:
                emails.append(word)
            if word.like_num==True:
                num.append(word)
            if word.is_currency==True:
                currency.append(word)
            if word.pos_=='NOUN':
                NOUNS.append(word)
            if word.pos_=='ADJ':
                ADJS.append(word)
            if word.pos_=='VERB':
                VERBS.append(word)
            if word.pos_=='ADV':
                ADVS.append(word)

        REL_NOUN = len(NOUNS)/description_length
        REL_ADJ = len(ADJS)/description_length
        REL_VERB = len(VERBS)/description_length
        REL_ADV = len(ADVS)/description_length

        # store lexemes in DF and sort lexemes by the most used one in the description
        DF = pd.DataFrame({"lexeme": [word.lemma_ for word in document if word.is_stop==False | word.is_punct == False | word.is_space == False | word.is_currency == False | word.like_email == False | word.like_num == False]})

        #safe lexem in dict with counts to store later in table 
        lexeme = DF.groupby(['lexeme']).size().reset_index(name='counts').sort_values('counts', ascending=False)
        print(lexeme)
        print(lexeme.shape[0])
        lexeme_1 = lexeme['lexeme'].iloc[0] if lexeme.shape[0] != 0 else 'NaN'
        lexeme_2 = lexeme['lexeme'].iloc[1] if lexeme.shape[0] > 1 else 'NaN'
        lexeme_3 = lexeme['lexeme'].iloc[2] if lexeme.shape[0] > 2 else 'NaN'
        lexeme_4 = lexeme['lexeme'].iloc[3] if lexeme.shape[0] > 3 else 'NaN'
        lexeme_5 = lexeme['lexeme'].iloc[4] if lexeme.shape[0] > 4 else 'NaN'
        lexeme_6 = lexeme['lexeme'].iloc[5] if lexeme.shape[0] > 5 else 'NaN'
        lexeme_7 = lexeme['lexeme'].iloc[6] if lexeme.shape[0] > 6 else 'NaN'
        lexeme_8 = lexeme['lexeme'].iloc[7] if lexeme.shape[0] > 7 else 'NaN'
        lexeme_9 = lexeme['lexeme'].iloc[8] if lexeme.shape[0] > 8 else 'NaN'
        lexeme_10 = lexeme['lexeme'].iloc[9] if lexeme.shape[0] > 9 else 'NaN'

        #save lexeme info in string to store in database
        lexeme_dict = str(lexeme.to_dict('records'))
        row_dict = {'globalId':entry['globalid'] ,'descriptionLength':description_length, 'NOUN':len(NOUNS), 'ADJ':len(ADJS), 'VERB':len(VERBS), 'ADV':len(ADVS),'REL_NOUN':REL_NOUN,'REL_ADJ':REL_ADJ,'REL_VERB':REL_VERB,'REL_ADV':REL_ADV,'EMAILS': len(emails), 'URLS':len(urls), 'NUMBERS':len(num),'CURRENCY':len(currency), 'AVG_SENTIMENT': sum(sentiment)/len(sentiment), 'lexeme_1':lexeme_1,'lexeme_2':lexeme_2,'lexeme_3':lexeme_3,'lexeme_4':lexeme_4,'lexeme_5':lexeme_5,'lexeme_6':lexeme_6,'lexeme_7':lexeme_7,'lexeme_8':lexeme_8,'lexeme_9':lexeme_9,'lexeme_10':lexeme_10,'lexeme_dict':lexeme_dict}
        funda_analysis = funda_analysis.append(row_dict, ignore_index=True)

    executing_script = "DROP TABLE IF EXISTS funda_NLP_analysis_"+str(year)+";"
    cur.execute(executing_script)
    executing_script = "CREATE TABLE IF NOT EXISTS funda_NLP_analysis_"+str(year)+" (globalId integer PRIMARY KEY, descriptionLength integer, NOUN integer, ADJ integer, VERB integer, ADV integer, REL_NOUN numeric,REL_ADJ numeric,REL_VERB numeric,REL_ADV numeric, emails integer, urls integer, numbers integer, currency integer, avg_sentiment numeric, lexeme_1 text, lexeme_2 text, lexeme_3 text, lexeme_4 text, lexeme_5 text, lexeme_6 text, lexeme_7 text, lexeme_8 text, lexeme_9 text, lexeme_10 text, lexeme_dict text);"
    cur.execute(executing_script)
    conn.commit()

    #INSERT ONE BY ONE
    # creating column list for insertion
    cols = ",".join([str(i) for i in funda_analysis.columns.tolist()])

    # Insert DataFrame recrds one by one.
    for i,row in funda_analysis.iterrows():
        sql = "INSERT INTO funda_analysis_"+str(year)+" (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cur.execute(sql, tuple(row))
        conn.commit()

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    return print('The Natural language processing has been done on the fulldescription and stored in a new table in the database')

fundaNlpAnalysisFunc(2018)
'''
#create connection to the databae
engine = create_engine('postgresql://localhost/[Robinkratschmayr2]') #Note: if you are connecting on your RPI change credentials
conn = psycopg2.connect("dbname=Robinkratschmayr2 user=Robinkratschmayr2")
cur = conn.cursor()

# Select the first 100 rows in the funda table and fetch them to a list object
executing_script = "SELECT globalId, fullDescription FROM funda_2018 limit 1;"
funda_2018 = sqlio.read_sql_query(executing_script, conn)
#print(funda_2018)

# Make the changes to the database persistent




#print(funda_2018['fulldescription'].iloc[0])
nlp = spacy.load("nl")
funda_analysis = pd.DataFrame(columns=['globalId','descriptionLength', 'NOUN', 'ADJ', 'VERB', 'ADV','REL_NOUN','REL_ADJ','REL_VERB','REL_ADV', 'lexeme_dict','wordtype_dict'])


for idx, entry in funda_2018.iterrows():
    document = nlp(entry['fulldescription'])

    DF = pd.DataFrame({"lexeme": [word.lemma_ for word in document],
                  "Wordtype": [word.pos_ for word in document]})

    description_length = len(entry['fulldescription'].split())
    #NOUN = word_type[word_type.wordtype == 'NOUN']['counts']

    word_type = DF.groupby(['Wordtype']).size().reset_index(name='counts').sort_values('counts', ascending=False)
    word_type_dict = str(word_type.to_dict('records'))
    NOUN = word_type[word_type.Wordtype == 'NOUN']['counts'].iloc[0] if 'NOUN' in word_type.Wordtype.values else 0
    ADJ = word_type[word_type.Wordtype == 'ADJ']['counts'].iloc[0] if 'ADJ' in word_type.Wordtype.values else 0
    VERB = word_type[word_type.Wordtype == 'VERB']['counts'].iloc[0] if 'VERB' in word_type.Wordtype.values else 0
    ADV = word_type[word_type.Wordtype == 'ADV']['counts'].iloc[0] if 'ADV' in word_type.Wordtype.values else 0
    REL_NOUN = NOUN/description_length
    REL_ADJ = ADJ/description_length
    REL_VERB = VERB/description_length
    REL_ADV = ADV/description_length

    lexeme = DF.groupby(['lexeme']).size().reset_index(name='counts').sort_values('counts', ascending=False)
    lexeme_dict = str(lexeme.to_dict('records'))

    filtered_sent = []

    # filtering stop words
    for word in document:
        if word.is_stop==False:
            filtered_sent.append(word)
    print("Filtered Sentence:",filtered_sent)
    

    row_dict = {'globalId':entry['globalid'] ,'descriptionLength':description_length, 'NOUN':NOUN, 'ADJ':ADJ, 'VERB':VERB, 'ADV':ADV,'REL_NOUN':REL_NOUN,'REL_ADJ':REL_ADJ,'REL_VERB':REL_VERB,'REL_ADV':REL_ADV, 'lexeme_dict':lexeme_dict,'wordtype_dict':word_type_dict}
    #row_dict = [entry['globalid'], description_length, NOUN, ADJ, VERB, ADV, REL_NOUN, REL_ADJ, REL_VERB, REL_ADV, lexeme_dict, word_type_dict]
    funda_analysis = funda_analysis.append(row_dict, ignore_index=True)



# Select the first 100 rows in the funda table and fetch them to a list object
executing_script = "DROP TABLE IF EXISTS funda_analysis_2018;"
cur.execute(executing_script)
executing_script = "CREATE TABLE IF NOT EXISTS funda_analysis_2018 (globalId integer PRIMARY KEY, descriptionLength integer, NOUN integer, ADJ integer, VERB integer, ADV integer, REL_NOUN numeric,REL_ADJ numeric,REL_VERB numeric,REL_ADV numeric, lexeme_dict text, wordtype_dict text);"
cur.execute(executing_script)
conn.commit()
#This is the prefered way according to pandas doc but does not work
'''
#print("Table created")
#sqlio.write_frame(funda_analysis, 'funda_analysis_2018', conn, if_exists='replace')
#funda_analysis.to_sql('funda_analysis_2018',schema="schema_test", con=conn, if_exists='replace', index=False)
'''
#INSERT ONE BY ONE
# creating column list for insertion
cols = ",".join([str(i) for i in funda_analysis.columns.tolist()])

# Insert DataFrame recrds one by one.
for i,row in funda_analysis.iterrows():
    sql = "INSERT INTO funda_analysis_2018 (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cur.execute(sql, tuple(row))

    # the connection is not autocommitted by default, so we must commit to save our changes
    conn.commit()


executing_script = "SELECT * FROM funda_analysis_2018 limit 100;"
print(sqlio.read_sql_query(executing_script, con=conn))

# Make the changes to the database persistent
#conn.commit()

# Close communication with the database
cur.close()
conn.close()
'''