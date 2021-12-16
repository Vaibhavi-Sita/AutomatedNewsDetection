# **Automated News Detection**

  The news that you have just read on your feed may or may not be entirely true. 
  This application helps you to check whether the news is **REAL** or **FAKE** using *ML/AI*!
  
## Prerequisites:

	Angular CLI : 6.0.x
	Node JS: 8.9.x
	Python 3
	
## Initial Steps:

1. Install Nltk, Flask and TextBlob
```
pip install nltk
pip install flask
pip install textblob
```
 
2. In Python shell 
```python
>>> import nltk
>>> nltk.download('punkt')
```
	
3. Clone this project into your local
	
4. Open the project in a desired IDE (ex: VScode)
	
**navigate to backend**
```node
node .\server.js
```
prompts *"connected to mongo"*
		
**navigate to frontend**
```
npm install
ng serve
```   
must compile successfully 
Angular server should listening on http://localhost:4200
	
**navigate to news-detection**
```python
python -m flask run
```
it will be running on http://127.0.0.1:5000/
	
		
## Use the Application

	open localhost:4200 on your browser
	
	register as a user
	
	you will be logged in automatically
	
	Click on Fake News Detection
	
	Enter a news string and click on "Check News"
	
	You will be shown whether the news is Real or Fake
	
