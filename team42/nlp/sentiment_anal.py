from subprocess import Popen
from subprocess import PIPE
import re
from instaTrack.fetch_data import JUNK_RE

class SentimentAnalysis:

    class __SentimentAnalysis:
        """Class for comments' sentiment analysis
        On creation the class runs the Java command for CoreNLP and everytime get_sentiments_for_comments(comments) is called
        it returns the corresponding sentiments.
        After usage please call self.close() method. Usage:
            sent = SentimentAnalysis()
            comments_with_sentiments = sent.get_sentiments_for_comments(my_comments)
            sent.close()
        """
        def __init__(self):

            print('######################################################################')
            print('DEBUG: singleton class CREATED....')
            print('######################################################################')

            COMMAND = "java -cp \"./nlp/lib/*\" -mx5g edu.stanford.nlp.sentiment.SentimentPipeline -stdin"
            self.process = Popen(COMMAND,
                                 stdout=PIPE,
                                 stdin=PIPE,
                                 bufsize=1,
                                 universal_newlines=True,
                                 shell=True)

        def close(self):
            """Closes the CoreNLP process"""
            self.process.stdin.close()

        def get_sentiments_for_comments(self, comments):
            """Returns the sentiments for each of the comments
        
            :param comments: Can be both list of strings, or list of dict as defined in fetch_data(). 
            When List of strings. Each string is the a raw comment extracted from Instagram.
            :return: List of pairs (comment, sentiment): comment is the same as given as input (either string or a dict), 
            sentiment is a string either 'Neutral', 'Positive' or 'Negative'.
            """
            if( not comments):
                return []

            if(isinstance(comments[0], dict)):
                comment_list = []
                for comment in comments:
                    comment_list.append(comment['text'])
            else:
                comment_list = comments

            comment_str, nb = self._make_string(self._clean_comments(comment_list))
            sentiments = self._feed_coreNLP(comment_str, nb)
            pairs = self._merge_sentiments_and_comments(comments, sentiments)
            return pairs


        def _clean_comments(self, comments):
            """ preprocessing comments to prepare them for sentiment analysis
        
            :param comments: List of strings. Each string is the a raw comment extracted from Instagram.
            :return: List of strings. Each string is the cleaned version of the comment. Please see clean_comment() below.
            """
            comments = list(map(lambda comment: self._clean_comment(comment), comments))
            return comments


        def _clean_comment(self, comment):
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


        def _merge_sentiments_and_comments(self, comments, sentiments):
            """ Prepares the output by putting together comments and their corresponding sentiments
            
            :param comments: List of stringor list of dict, each of which a comment
            :param sentiments: List of string, each of which denoting the corresponding sentiment of a comment
            :return: List of pairs (comment, sentiment)
            """
            pairs = []
            if(isinstance(comments[0], dict)):
                for i, comment in enumerate(comments):
                    comment['sentiment'] = sentiments[i]
                    pairs.append(comment)
            else:
                for i, comment in enumerate(comments):
                    pairs.append((comment, sentiments[i]))
            return pairs


        def _make_string(self, comments):
            """Makes a string out of the list of comments. The string contains each of the comments on a new line. It also 
            returns the total number of lines(=comments) as it's needed in self._feed_coreNLP"""
            comments_str = ''
            for comment in comments:
                comments_str += comment + '\n'
            return comments_str, len(comments)


        def _clean_coreNLP_output(self, sentiments):
            """Clear the output of the CoreNLP"""
            sentiments = [sentiment.strip().lower().replace(" ", "") for sentiment in sentiments]
            sentiments = ['neutral' if (sentiment == '') else sentiment for sentiment in sentiments]
            return sentiments


        def _feed_coreNLP(self, comments, nb):
            """ Fills the stdin of the open process CoreNLP to get sentiments in stdout. 
        
            :param comments: String containing comments on each line 
            :param nb: Number of total lines(=comments)
            :return: List of sentiments received in stdout.
            """
            self.process.stdin.write(comments);
            sentiments = []
            for lines in range(nb):
                sentiments.append(self.process.stdout.readline())
            return self._clean_coreNLP_output(sentiments)

    instance = None

    def __init__(self):
        if not SentimentAnalysis.instance:
            SentimentAnalysis.instance = SentimentAnalysis.__SentimentAnalysis()

    def get_sentiments_for_comments(self, comments):
        return SentimentAnalysis.instance.get_sentiments_for_comments(comments)

    def close(self):
        # dont do this because we dont want to close the file
        #SentimentAnalysis.instance.close()
        pass    

    def close_and_kill(self):
        # dont do this because we dont want to close the file
        print('######################################################################')
        print('Closing and killing SentimentAnalysis!')
        print('######################################################################')
        if SentimentAnalysis.instance:
            SentimentAnalysis.instance.close()
            SentimentAnalysis.instance = None
               