from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/apology")
def sorry():
     return {
        "message": "I sincerely apologize for violating the rules by posting a foreign link in the hng space. This is a result of my ignorance of not going through the rules and I promise will never happen again.",
        "recipient": "Shully"
        }

if __name__ == "__main__":
     app.run()
