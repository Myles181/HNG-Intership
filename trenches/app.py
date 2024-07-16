from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/apology")
def sorry():
     return {
          "message": "Dear Shully, I sincerely apologize for violating the rules by posting a foreign link in the HNG space. I realize this mistake was due to my failure to thoroughly review the guidelines. I assure you that this will not happen again, and I will be more diligent in adhering to the rules moving forward. Thank you for your understanding.",
          "recipient": "Shully"
     }


if __name__ == "__main__":
     app.run()
