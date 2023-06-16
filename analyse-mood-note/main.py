import json
from transformers import pipeline


def analyze_mood_note(text):
    """Analyze Mood Note"""
    classifier = pipeline("sentiment-analysis")
    res = classifier(text)
    # Return the emotions as a JSON string
    return json.dumps(res)


def main(req, res):
    payload = json.loads(req.payload)
    result = analyze_mood_note(payload['text'])

    return res.json({
        json.dumps(result)
    })
