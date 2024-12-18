import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import matplotlib.pyplot as plt

class SentimentAnalyzer:
    def __init__(self, candidate_1_file="clean_1.json", candidate_2_file="clean_2.json"):
        nltk.download('vader_lexicon')  # Ensure VADER lexicon is downloaded
        self.analyzer = SentimentIntensityAnalyzer()
        self.candidate_1_file = candidate_1_file
        self.candidate_2_file = candidate_2_file
        self.results = {
            "candidate_1": [],  # Trump
            "candidate_2": []   # Kamala
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

    def plot_sentiment_distribution(self):
        def count_sentiments(candidate_key):
            sentiments = [item["sentiment"] for item in self.results[candidate_key]]
            return {
                "positive": sentiments.count("positive"),
                "neutral": sentiments.count("neutral"),
                "negative": sentiments.count("negative")
            }

        candidate_1_counts = count_sentiments("candidate_1")
        candidate_2_counts = count_sentiments("candidate_2")

        # Plot for candidate 1
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.bar(candidate_1_counts.keys(), candidate_1_counts.values(), color=['green', 'blue', 'red'])
        plt.title("Sentiment Distribution for Donald Trump")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Plot for candidate 2
        plt.subplot(1, 2, 2)
        plt.bar(candidate_2_counts.keys(), candidate_2_counts.values(), color=['green', 'blue', 'red'])
        plt.title("Sentiment Distribution for Kamala Harris")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Show plots
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    analyzer.analyze_sentiment()
    analyzer.save_results()
    analyzer.plot_sentiment_distribution()
