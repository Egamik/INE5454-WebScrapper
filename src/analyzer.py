import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json

class SentimentAnalyzer:
    def __init__(self, candidate_1_file="cleaned_candidate_1_titles.json", candidate_2_file="cleaned_candidate_2_titles.json"):
        nltk.download('vader_lexicon')  # Ensure VADER lexicon is downloaded
        self.analyzer = SentimentIntensityAnalyzer()
        self.candidate_1_file = candidate_1_file
        self.candidate_2_file = candidate_2_file
        self.results = {
            "candidate_1": [],
            "candidate_2": []
        }

    def analyze_sentiment(self):
        def analyze_titles(titles, candidate_key):
            for title in titles:
                sentiment_scores = self.analyzer.polarity_scores(title)
                sentiment = self.categorize_sentiment(sentiment_scores["compound"])
                self.results[candidate_key].append({
                    "title": title,
                    "sentiment": sentiment,
                    "scores": sentiment_scores
                })

        # Load data for both candidates
        with open(self.candidate_1_file, "r") as infile:
            candidate_1_data = json.load(infile)
        with open(self.candidate_2_file, "r") as infile:
            candidate_2_data = json.load(infile)

        # Analyze sentiment for both candidates
        analyze_titles(candidate_1_data, "candidate_1")
        analyze_titles(candidate_2_data, "candidate_2")

    @staticmethod
    def categorize_sentiment(compound_score):
        """Categorize sentiment based on compound score."""
        if compound_score >= 0.05:
            return "positive"
        elif compound_score <= -0.05:
            return "negative"
        else:
            return "neutral"

    def save_results(self, output_file="sentiment_results.json"):
        with open(output_file, "w") as outfile:
            json.dump(self.results, outfile, indent=4)
        print(f"Sentiment analysis results saved to {output_file}")

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    analyzer.analyze_sentiment()
    analyzer.save_results()
