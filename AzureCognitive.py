from google.oauth2 import service_account
from googleapiclient.discovery import build

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


# Get data from Google Sheets
SERVICE_ACCOUNT_FILE = 'service_account_key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
sheets_api = build('sheets', 'v4', credentials=creds)

spreadsheet_id = "10AMUaG_Yg6Ka4k8VnPnOh5z-Bo5mDrgL00iDGWTzK9M"
range_name = "Form Responses 1!B2:E"
result = sheets_api.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
responses = result.get("values", [])

# Get sentiment analysis from Azure Cognitive Services
azure_api_key = "0e57acbbb0f54f169f104dfb06f80ca9"
azure_endpoint = "https://project2cognitiveemployeereview.cognitiveservices.azure.com/"
text_analytics_client = TextAnalyticsClient(endpoint=azure_endpoint, credential=AzureKeyCredential(azure_api_key))

sentiments_by_date = []

for response in responses:
    feedbacks = response[:-1]
    date = response[-1]

    documents = [{"id": str(i + 1), "text": text}
                 for i, text in enumerate(feedbacks)]
    sentiment_analysis = text_analytics_client.analyze_sentiment(documents=documents)

    sentiments = []
    for doc in sentiment_analysis:
        sentiment_scores = doc.confidence_scores
        sentiment_positive = sentiment_scores.positive
        sentiment_neutral = sentiment_scores.neutral
        sentiment_negative = sentiment_scores.negative
        sentiments.append((f"Employee {doc.id}", {"positive": sentiment_positive, "neutral": sentiment_neutral, "negative": sentiment_negative}))

    sentiments_by_date.append((date, sentiments))

for date_sentiments in sentiments_by_date:
    date = date_sentiments[0]
    sentiments = date_sentiments[1]
    print(f"Date: {date}")
    for sentiment in sentiments:
        print(f"{sentiment[0]}: positive {sentiment[1]['positive']}, neutral {sentiment[1]['neutral']}, negative {sentiment[1]['negative']}")
    print("\n")

# Write to CSV file
with open("sentiments.csv", "w") as f:
    f.write("Date,Employee,Positive,Neutral,Negative\n")
    for date_sentiments in sentiments_by_date:
        date = date_sentiments[0]
        sentiments = date_sentiments[1]
        for sentiment in sentiments:
            f.write(f"{date},{sentiment[0]},{sentiment[1]['positive']},{sentiment[1]['neutral']},{sentiment[1]['negative']}\n")
