# Handle-Retriever
Retrieves handles (Facebook, Twitter, iOS App, Google Play Store App) from a webpage given a csv of URLs and returns the handles in a JSON string.

Input: input_urls.csv
Output: result.json

Given a url (https://nextdoor.com/), it will parse the webpage for any handles and return it in a format as such:

{
        "facebook": "nextdoor",
        "google": "id=com.nextdoor",
        "twitter": "nextdoor"
}

External libraries used: FuzzyWuzzy (for fuzzy matching of strings), BeautifulSoup (for parsing meta content of source HTML)
