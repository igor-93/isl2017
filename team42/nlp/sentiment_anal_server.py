import re
import asyncio
import aiohttp

from instaTrack.fetch_data import JUNK_RE


SERVER_URL = 'http://localhost:9000'
PROPERTIES = '{"annotators":"sentiment","outputFormat":"json"}'


# run the server with:
#   java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000 -ssplit.eolonly
PROPERTIES_2 = '{"annotators":"sentiment", "ssplit.eolonly":"true", "outputFormat":"json"}'


# TODO: remove this function when client starts supporting nummvric values
def sent_value_to_textual(sentiment):
    i_s = int(sentiment)
    if i_s == 0:
        return 'verynegative'
    elif i_s == 1:
        return 'negative'
    elif i_s == 2:
        return 'neutral'
    elif i_s == 3:
        return 'positive'
    elif i_s == 4:
        return 'verypositive'    
    pass


def get_sentiments_for_comments(loop, session, comments):
    #print('running get_sentiments_for_comments()...')
    """Returns the sentiments for each of the comments

    :param comments: Can be both list of strings, or list of dict as defined in fetch_data(). 
    When List of strings. Each string is the a raw comment extracted from Instagram.
    :return: List of pairs (comment, sentiment): comment is the same as given as input (either string or a dict), 
    sentiment is a string either 'Neutral', 'Positive' or 'Negative'.
    """
    if not comments:
        return []

    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    final_result = loop.run_until_complete(
        asyncio.gather(
            *(fetch_single_sentiment(session, comment) for comment in comments)
        )
    )
    #print('DONE get_sentiments_for_comments()!')
    return final_result


def _clean_comment( comment):
    """ Clean the comment to prepare it for sentiment analysis.

    :param comment: string. Raw comment extracted from instagram
    :return: string. Cleaned comment, where hashtags are removed, @users are removed, concatenated whitespaces
    are replaced by one single whitespace and finally emojis are removed
    """
    comment = comment.translate({ord(c): '' for c in '#'})  # remove hashtags
    comment = re.sub('@[a-z0-9]*\s', '', comment)  # remove anything with @
    comment = " ".join(comment.split()) # remove multiple whitespaces

    emoji_re = re.compile(r'\s*' + JUNK_RE + r'\s*', re.UNICODE) #Get rid of emojis
    comment = re.sub(emoji_re, '',comment)
    return comment


async def fetch_single_sentiment(session, comment):
    clean_comment = _clean_comment(comment['text'])

    #async with aiohttp.ClientSession() as session:
    #    async with sem:
    async with session.post(
        SERVER_URL, params={
            'properties': PROPERTIES_2
        }, data=clean_comment) as resp:     # , headers={'Connection': 'close'}


        data = await resp.json()
        
        sentences = data['sentences']
        ave_rs = 0.0
        for sent in sentences:
            ave_rs += float(sent['sentimentValue'])

        if len(sentences) != 0:
            ave_rs /= len(sentences)
        else:
            ave_rs = 2.0   # neutral
        comment['sentiment'] = sent_value_to_textual(ave_rs)
        comment['sentiment_value'] = ave_rs

    return comment
