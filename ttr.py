###########################################################
# Type/Token Ratio (TTR) analysis of dialogues
#
# Syntax:
#    python ttr.py <path to source file>
#
# Author: Erik Billing, University of Skovde
# Created: April 2024. 
# License: MIT
###########################################################

import re, argparse, os
import nltk
import logreader
import pandas as pd

# Test nltk dependency:
try:
    nltk.word_tokenize("hello world")
except LookupError:
    print('Downloading missing nltk dependency: "punkt".')
    nltk.download('punkt')

def ttri(iterable):
    """Returns TTR analysis over an iterable. Each element returned by the iterable should be on the form (agent,uterance). For each item, TTR returns (agent,ttr-value).
    """
    tokens = {}

    for agent,s in iterable:
        if agent not in tokens: 
            tokens[agent] = []
        agentTokens = tokens[agent]
        agentTokens.extend(tokenise(s))
        yield agent,ttr(agentTokens),s

def ttr(tokens):
    types = nltk.Counter(tokens)
    return len(types)/len(tokens)*100

def tokenise(s):
    s = re.sub(r'[^\w]', ' ', s) # Clean special characters
    s = s.lower()
    return nltk.word_tokenize(s)
    
def printTTR(sourcefile,skipFirstN=1):
    for a,v,s in ttri(logreader.readPepperChat(sourcefile,skipFirstN)):
        print('%s: (ttr=%.2f) %s'%(('R' if a=='robot' else 'H'),v,s.replace('\n',' ')))

def ttrToDf(sourcefile,destfile,skipFirstN=1):
    df = pd.DataFrame(list(ttri(logreader.readPepperChat(sourcefile,skipFirstN))),columns=('Agent','TTR','Phrase'))
    df.to_excel(destfile)
    print('Analysis saved as',destfile)

def ttrDir(src,target=None,skipFirstN=1):
    srcFiles = [os.path.splitext(f) for f in os.listdir(src) if f.endswith('.log')]

    for f,ext in srcFiles:
        print('Analysing TTR for',f+ext)
        if target:
            ttrToDf(os.path.join(src,f+ext),os.path.join(target,f+'.xlsx'),skipFirstN)

def main():
    parser = argparse.ArgumentParser(
        prog='ttr',
        description='Type/Token Ration (TTR) analysis of dialogues.',
        epilog='By Erik Billing, University of Skövde')
    
    parser.add_argument('source',help='The log file or folder containing the dialogue or dialogues to be analsed.')
    parser.add_argument('save',help='Target directory for output files.')

    args = parser.parse_args()

    if os.path.isdir(args.source):
        ttrDir(args.source,args.save)
    elif args.save:
        ttrToDf(args.sourcefile,args.save)
    else:
        printTTR(args.sourcefile)
    

if __name__ == '__main__':
    main()