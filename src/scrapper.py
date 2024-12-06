import praw
import json
from datetime import datetime, timezone
  
class RedditCrawler():
    def __init__(self):
        self.reddit_read_only = praw.Reddit(
            client_id="n5gAGsyr-4s7yArEWI9Etw",
            client_secret="hRzimC2WjrW1zNBUjz6e3I6aFJC9rg",
            user_agent="johndoehornet"
        )
        self.search_id = 0
        self.submissions_info = []
        self.subreddits = ['uspolitics', 'AmericanPolitics']
        self.keywords = ['donald', 'trump', 'donald trump', 'kamala', 'harris', 'kamala harris']
        self.start_date = datetime(2022, 1, 1).replace(tzinfo=timezone.utc).timestamp()
        self.end_date = datetime(2024, 12, 31).replace(tzinfo=timezone.utc).timestamp()

    def crawl(self):
        for sub in self.subreddits:
            subreddit = self.reddit_read_only.subreddit(sub)
            print(f"Crawling subreddit: {sub}")
            
            for keyword in self.keywords:
                print(f"Searching for keyword: {keyword}")
                try:
                    for submission in subreddit.search(query=keyword, sort="new", limit=1000):
                        # Filter submissions by date
                        if not (self.start_date <= submission.created_utc <= self.end_date):
                            continue

                        submission_info = {
                            'ID': f"{self.search_id}_{submission.id}",
                            'Title': submission.title,
                            'Upvotes': submission.score,
                            'Comments': submission.num_comments,
                            'Date': datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                            'URL': submission.url
                        }
                        self.submissions_info.append(submission_info)
                        print(f"Added submission: {submission.title}")
                    
                    self.search_id += 1
                except Exception as e:
                    print(f"Error while searching in subreddit {sub}: {e}")

    def save_results(self, filename="results.json"):
        with open(filename, "w") as outfile:
            json.dump(self.submissions_info, outfile, indent=4)
        print(f"Results saved to {filename}")


if __name__ == "__main__":
    crawler = RedditCrawler()
    crawler.crawl()
    crawler.save_results()
