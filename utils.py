import os
import PyPDF2
import json
from werkzeug.utils import secure_filename
import re

# Try to load spaCy (optional for enhanced key points)
nlp = None
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    print("✓ spaCy model loaded successfully")
except Exception as e:
    print(f"⚠ spaCy not available (optional): {e}")

# Try to load transformers (optional for AI features)
summarizer = None
sentiment_analyzer = None
try:
    from transformers import pipeline
    import ssl
    import certifi
    
    # Disable SSL verification (temporary workaround for SSL errors)
    # Note: Only use this for development/testing
    ssl._create_default_https_context = ssl._create_unverified_context
    
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    print("✓ AI models loaded successfully")
except Exception as e:
    print(f"⚠ AI models not available - using fallback methods: {str(e)[:100]}")
    print("  The app will still work with basic text analysis!")


def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading text file: {str(e)}")


def extract_text(file_path, file_type):
    """Extract text based on file type"""
    if file_type == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_type == 'txt':
        return extract_text_from_txt(file_path)
    else:
        raise Exception(f"Unsupported file type: {file_type}")


def generate_summary(text, max_length=150, min_length=50):
    """Generate summary using AI or fallback method"""
    if summarizer:
        try:
            # Limit text length for summarization (BART has a token limit)
            max_input_length = 1024
            if len(text.split()) > max_input_length:
                text = ' '.join(text.split()[:max_input_length])
            
            # Generate summary
            summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"AI summarization failed, using fallback: {e}")
    
    # Fallback: Smart extraction method
    return generate_fallback_summary(text)


def generate_fallback_summary(text):
    """Generate summary using basic text analysis (no AI required)"""
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if not sentences:
        return "Document is too short to summarize."
    
    # Take first sentence, middle sentence, and last sentence for variety
    summary_sentences = []
    
    if len(sentences) >= 1:
        summary_sentences.append(sentences[0])
    
    if len(sentences) >= 3:
        summary_sentences.append(sentences[len(sentences) // 2])
    
    if len(sentences) >= 2:
        summary_sentences.append(sentences[-1])
    
    summary = '. '.join(summary_sentences[:3])
    
    # Ensure it ends with punctuation
    if summary and summary[-1] not in '.!?':
        summary += '.'
    
    return summary if summary else "Unable to generate summary from this document."


def extract_key_points(text):
    """Extract key points using NLP or fallback method"""
    if nlp:
        try:
            doc = nlp(text[:100000])  # Limit text length
            
            # Extract sentences with important entities or noun chunks
            key_points = []
            sentences = list(doc.sents)
            
            # Get sentences with named entities
            for sent in sentences[:20]:  # Limit to first 20 sentences
                if any(ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'PRODUCT'] for ent in sent.ents):
                    key_points.append(sent.text.strip())
                    if len(key_points) >= 5:
                        break
            
            # If not enough, add sentences with important noun chunks
            if len(key_points) < 5:
                for sent in sentences[:30]:
                    if len(list(sent.noun_chunks)) >= 2 and sent.text.strip() not in key_points:
                        key_points.append(sent.text.strip())
                        if len(key_points) >= 5:
                            break
            
            return key_points[:5]
        except Exception as e:
            print(f"spaCy extraction failed, using fallback: {e}")
    
    # Fallback: Basic key point extraction
    return extract_fallback_key_points(text)


def extract_fallback_key_points(text):
    """Extract key points using basic text analysis (no AI required)"""
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    
    if not sentences:
        return []
    
    key_points = []
    
    # Look for sentences with keywords indicating importance
    important_keywords = [
        'important', 'significant', 'key', 'main', 'primary', 'essential',
        'critical', 'major', 'crucial', 'fundamental', 'conclusion',
        'summary', 'result', 'finding', 'shows', 'demonstrates', 'reveals'
    ]
    
    for sentence in sentences[:30]:  # Check first 30 sentences
        sentence_lower = sentence.lower()
        
        # Check for important keywords
        if any(keyword in sentence_lower for keyword in important_keywords):
            key_points.append(sentence)
            if len(key_points) >= 5:
                break
    
    # If we don't have enough, add sentences that are not too short
    if len(key_points) < 5:
        for sentence in sentences[:15]:
            if sentence not in key_points and len(sentence.split()) >= 8:
                key_points.append(sentence)
                if len(key_points) >= 5:
                    break
    
    return key_points[:5]


def analyze_sentiment(text):
    """Analyze sentiment using AI or fallback method"""
    if sentiment_analyzer:
        try:
            # Limit text length for sentiment analysis
            max_length = 512
            text_sample = ' '.join(text.split()[:max_length])
            
            result = sentiment_analyzer(text_sample)[0]
            label = result['label'].lower()
            score = result['score']
            
            # Convert to sentiment score (-1 to 1)
            if label == 'positive':
                sentiment_score = score
            else:  # negative
                sentiment_score = -score
            
            return label, round(sentiment_score, 3)
        except Exception as e:
            print(f"AI sentiment failed, using fallback: {e}")
    
    # Fallback: Basic sentiment analysis
    return analyze_fallback_sentiment(text)


def analyze_fallback_sentiment(text):
    """Analyze sentiment using basic keyword matching (no AI required)"""
    text_lower = text.lower()
    
    # Positive and negative word lists
    positive_words = [
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
        'positive', 'success', 'beneficial', 'advantage', 'improve', 'better',
        'best', 'happy', 'pleased', 'satisfied', 'effective', 'efficient',
        'innovative', 'breakthrough', 'achievement', 'progress', 'growth'
    ]
    
    negative_words = [
        'bad', 'terrible', 'awful', 'poor', 'negative', 'failure', 'problem',
        'issue', 'concern', 'risk', 'threat', 'worse', 'worst', 'difficult',
        'challenge', 'crisis', 'decline', 'decrease', 'loss', 'damage',
        'harmful', 'dangerous', 'critical', 'severe'
    ]
    
    # Count occurrences
    positive_count = sum(text_lower.count(word) for word in positive_words)
    negative_count = sum(text_lower.count(word) for word in negative_words)
    
    total = positive_count + negative_count
    
    if total == 0:
        return "neutral", 0.0
    
    # Calculate sentiment
    positive_ratio = positive_count / total
    
    if positive_ratio > 0.6:
        sentiment = "positive"
        score = round(positive_ratio, 3)
    elif positive_ratio < 0.4:
        sentiment = "negative"
        score = -round(1 - positive_ratio, 3)
    else:
        sentiment = "neutral"
        score = 0.0
    
    return sentiment, score


def analyze_document(file_path, file_type):
    """Perform complete document analysis"""
    # Extract text
    extracted_text = extract_text(file_path, file_type)
    
    if not extracted_text:
        raise Exception("No text could be extracted from the document")
    
    # Generate summary
    summary = generate_summary(extracted_text)
    
    # Extract key points
    key_points = extract_key_points(extracted_text)
    
    # Analyze sentiment
    sentiment, sentiment_score = analyze_sentiment(extracted_text)
    
    # Count words
    word_count = len(extracted_text.split())
    
    return {
        'extracted_text': extracted_text,
        'summary': summary,
        'key_points': json.dumps(key_points),
        'sentiment': sentiment,
        'sentiment_score': sentiment_score,
        'word_count': word_count
    }
