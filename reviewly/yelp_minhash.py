#Below is how our script should be
# This is not the final script.
"""
Script:     yelp_minhash.py
Purpose:    (a) Preprocess data as much as possible to allow us to input data into Minhash functions
            (b) Provide recommendations based on text similarities obtained from MinHashing
Input:      For this script, I am simply using the csv file which was available online. I didn't even filter our category to restuarants.
Output:     Provide recommendations based on our query.
"""

"""
Function to preprocess text
text:           Data of type pandas Series. Simply yelp['text'] would give us text variable.
RETURNS:        Returns a set of tokens or simply said bag of words.
"""


stop_words = stopwords.words('english')

# Please note that this is not the final pre processing of text data. We can further pre process it.
def preprocess(text):
    text = re.sub(r'[^\w\s]','',text)
    tokens = text.lower()
    tokens = tokens.split()
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [word for word in tokens if word.isalpha()]
    return tokens

"""
Function that builds a Minhash LSH forest that is useful to make top k queries faster
data:           This will be our text data. We will pass the yelp dataframe.
permutaions:    
RETURNS:        Returns a Min Hash LSH Forest that can used to query for top-k recommendations
"""


def build_mhLshForest(data, permutations):

    mhArray = []
    
    for text in data['text']:
        pre = preprocess(text)
        mh = MinHash(num_perm=perms)
        for word in pre:
            m.update(word.encode('utf8'))
        mhArray.append(mh)
        
    forest = MinHashLSHForest(num_perm=perms)
    
    for i,m in enumerate(minhash):
        forest.add(i,m)
        
    forest.index()
    
    return forest

"""
Function that builds a Minhash LSH forest that is useful to make top k queries faster
Parameters:     This will be our text data. We will pass the yelp dataframe.
RETURNS:        Returns a Min Hash LSH Forest that can used to query for top-k recommendations
"""

def predict(title, data, label_length, top_k_results, forest):
    
    pre = preprocess(title)
    mh = MinHash(num_perm=label_length)
    for word in pre:
        mh.update(word.encode('utf8'))
        
    idx_array = np.array(forest.query(mh, top_k_results))
    if len(idx_array) == 0:
        return None # if your query is empty, return none
    
    result = data.iloc[idx_array]['text']
    
    return result

perms = 256

#Number of Recommendations to return
num_recommendations = 1

forest = get_forest(yelp, permutations)

top_k_results = 5
title = '"My wife took me here on my birthday for breakfast and it was excellent.  The weather was perfect which made sitting outside overlooking their grounds an absolute pleasure.  Our waitress was excellent and our food arrived quickly on the semi-busy Saturday morning.  It looked like the place fills up pretty quickly so the earlier you get here the better. Do yourself a favor and get their Bloody Mary.  It was phenomenal and simply the best Ive ever had.  Im pretty sure they only use ingredients from their garden and blend them fresh when you order it.  It was amazing. While EVERYTHING on the menu looks excellent, I had the white truffle scrambled eggs vegetable skillet and it was tasty and delicious.  It came with 2 pieces of their griddled bread with was amazing and it absolutely made the meal complete.  It was the best toast Ive ever had. Anyway, I cant wait to go back!"'
result = predict(title, yelp, perms, top_k_results, forest)
print('\n Top Recommendation(s) is(are) \n', result)
