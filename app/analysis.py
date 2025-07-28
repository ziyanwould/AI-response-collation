import pandas as pd
import io

def analyze_data(data):
    """
    Analyzes the provided CSV data.
    """
    df = pd.read_csv(io.StringIO(data))

    # Problem 1: New Category
    df['optimization_category'] = df['用户问题'].apply(categorize_question)

    # Problem 2: Sentiment Analysis (Simulated)
    df['sentiment'] = df['用户问题'].apply(sentiment_analysis)

    # Problem 3: Question Summary
    category_counts = df['问题分类'].value_counts().to_dict()

    # Problem 4: Effective Replies
    df['is_effective_reply'] = df['Bot 回复'].apply(is_effective)
    effective_reply_counts = df['is_effective_reply'].value_counts().to_dict()

    return {
        'optimization_category_counts': df['optimization_category'].value_counts().to_dict(),
        'sentiment_counts': df['sentiment'].value_counts().to_dict(),
        'category_counts': category_counts,
        'effective_reply_counts': effective_reply_counts,
        'dataframe': df.to_html()
    }

def categorize_question(question):
    """
    Categorizes a question into optimization categories.
    """
    question = str(question).lower()
    if '转人工' in question or '客服' in question:
        return 'System Issue'
    elif '界面' in question or '显示' in question:
        return 'UI Issue'
    elif '不知道' in question or '不明白' in question or '什么意思' in question:
        return 'Unclear Answer'
    else:
        return 'General Inquiry'

def sentiment_analysis(question):
    """
    Simulates sentiment analysis based on keywords.
    """
    question = str(question).lower()
    if '没有回复' in question or '不行' in question or '失败' in question:
        return 'Negative'
    elif '谢谢' in question or '感谢' in question or '好的' in question:
        return 'Positive'
    else:
        return 'Neutral'

def is_effective(reply):
    """
    Determines if a bot reply is effective.
    """
    reply = str(reply)
    if '问题小桂还在学习中' in reply or '换个问法试试' in reply:
        return False
    return True
