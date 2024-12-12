import praw
import json
import re
from datetime import datetime, timezone

class RedditCrawler():
    def __init__(self,
                subreddits=['uspolitics', 'PoliticalDiscussion', 'republican', 'democrats'],
                keywords=[['donald', 'trump', 'donald trump'], ['kamala', 'harris', 'kamala harris']]
                ):
        self.reddit_read_only = praw.Reddit(
            client_id="n5gAGsyr-4s7yArEWI9Etw",
            client_secret="hRzimC2WjrW1zNBUjz6e3I6aFJC9rg",
            user_agent="johndoehornet"
        )
        self.candidate_1_posts = []
        self.candidate_2_posts = []
        
        self.search_id = 0
        self.submissions_info = []
        
        self.subreddits = subreddits
        self.keywords = keywords[0] + keywords[1]
        self.candidate_1_keywords = keywords[0]
        self.candidate_2_keywords = keywords[1]
        
        self.start_date = datetime(2021, 1, 1).replace(tzinfo=timezone.utc).timestamp()
        self.end_date = datetime(2024, 12, 31).replace(tzinfo=timezone.utc).timestamp()

    def crawl(self):
        for sub in self.subreddits:
            subreddit = self.reddit_read_only.subreddit(sub)
            print(f"Crawling subreddit: {sub}")
            
            for keyword in self.keywords:
                print(f"Searching for keyword: {keyword}")
                try:
                    for submission in subreddit.search(query=keyword, sort="new", limit=100):
                        # Filter submissions by date
                        if not (self.start_date <= submission.created_utc <= self.end_date):
                            continue

                        # Fetch submission details
                        submission.comments.replace_more(limit=0)  # Flatten comments
                        all_comments = submission.comments.list()
                        comments = [comment.body for comment in all_comments[:5]]  # Limit to the first 5 comments

                        submission_info = {
                            'ID': f"{self.search_id}_{submission.id}",
                            'Subreddit': sub,
                            'Keyword': keyword,
                            'Title': submission.title,
                            'Text': submission.selftext,  # Post content
                            'Upvotes': submission.score,
                            'Comments_Count': submission.num_comments,
                            'Comments': comments,  # Add all comments
                            'Date': datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                            'URL': submission.url
                        }
                        self.submissions_info.append(submission_info)
                        print(f"Added submission: {submission.title}")
                        
                        if keyword in self.candidate_1_keywords:
                            self.candidate_1_posts.append(submission.title)
                        else:
                            self.candidate_2_posts.append(submission.title)
                    
                    self.search_id += 1
                except Exception as e:
                    print(f"Error while searching in subreddit {sub}: {e}")

    def save_results(self, filename="results.json"):
        with open(filename, "w") as outfile:
            json.dump(self.submissions_info, outfile, indent=4)
        
        with open("results_1.json", "w") as outfile:
            json.dump(self.candidate_1_posts, outfile, indent=4)
        
        with open("results_2.json", "w") as outfile:
            json.dump(self.candidate_2_posts, outfile, indent=4)
             
        print(f"Results saved to {filename}")

    def clean_data(self, filename="results", filext='.json'):
        def clean_text(text):
            text = re.sub(r'[^A-Za-z0-9\s]', '', text)  # Remove special characters
            text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
            text = re.sub(r'[\U00010000-\U0010FFFF]', '', text, flags=re.UNICODE)  # Remove emojis
            text = re.sub(r'[\u2018\u2019\u201c\u201d\u2026\u2014\u201d\u201c\'\"]', '', text) # Remove quotes
            return text.lower().strip()  # Convert to lowercase and strip whitespace
        
        with open("results_1.json", "r") as infile:
            c1_data = json.load(infile)
            
        with open("results_2.json", "r") as infile:
            c2_data = json.load(infile)
            
        clean_1 = [clean_text(text) for text in c1_data]
        clean_2 = [clean_text(text) for text in c2_data]
        
        with open("clean_1.json", 'w') as outfile:
            json.dump(clean_1, outfile, indent=4)
            
        with open('clean_2.json', 'w') as outfile:
            json.dump(clean_2, outfile, indent=4)
            
        print('Clean data saved')
        

if __name__ == "__main__":
    crawler = RedditCrawler()
    crawler.crawl()
    crawler.save_results()
    crawler.clean_data()