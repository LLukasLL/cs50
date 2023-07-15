import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_shares = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]
    total = float(user_cash.get('cash'))

    # write current prices into db for formatting
    if len(user_shares) != 0:
        for x in user_shares:
            Quote = lookup(x.get('symbol'))
            price = float(Quote.get('price'))
            shares = int(db.execute("SELECT shares FROM shares WHERE user_id = ? AND symbol = ?", session["user_id"], Quote.get('symbol'))[0].get('shares'))
            total_value = price * shares
            db.execute("UPDATE shares SET share_price = ? WHERE user_id = ? AND symbol = ?", Quote.get('price'), session["user_id"], Quote.get('symbol'))
            db.execute("UPDATE shares SET total_value = ? WHERE user_id = ? AND symbol = ?", total_value, session["user_id"], Quote.get('symbol'))
            total += total_value

        user_shares = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])
    return render_template("index.html", user_shares=user_shares, user_cash=user_cash.get("cash"), total=total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensure Symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide Symbol", 400)

        # Ensure Shares were submitted and positive integer
        # shares_temp = request.form.get("shares")
        elif not request.form.get("shares"):
            return apology("must provide Shares", 400)
        elif not request.form.get("shares").isnumeric():
            return apology("Shares can't be fractional, negative, and non-numeric", 400)
        elif float(request.form.get("shares")) < 1:
            return apology("Shares must be > 0", 400)

        shares_temp = float(request.form.get("shares")).is_integer()
        if not shares_temp:
            return apology("Shares must be integer", 400)

        # lookup symbol
        Quote = lookup(request.form.get("symbol"))

        # ensure symbol is valid
        if not Quote:
            return apology("invalid symbol", 400)
        if len(Quote) == 0:
            return apology("invalid symbol", 400)

        latest_price = float(Quote.get('price'))
        user_shares = int(request.form.get("shares"))

        # ensure symbol is valid
        if not Quote:
            return apology("invalid symbol", 400)
        if len(Quote) == 0:
            return apology("invalid symbol", 400)

        # Check if user has enough cash
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]
        float_user_cash = float(user_cash.get('cash'))
        if not float_user_cash > latest_price * user_shares:
            return apology("Not enough cash", 400)

        # write entry into transactions and shares
        transaction_type = 'buy'
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute("INSERT INTO transactions (user_id, transaction_type, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"],transaction_type, Quote.get('symbol'), request.form.get("shares"), latest_price, date)

        old_shares = db.execute("SELECT * FROM shares WHERE user_id = ? AND symbol = ?", session["user_id"], Quote.get('symbol'))
        if len(old_shares) == 1:
            old_shares_int = int(old_shares[0].get("shares"))
            shares_input = int(request.form.get("shares"))
            new_shares = old_shares_int + shares_input
            db.execute("UPDATE shares SET shares = ? WHERE user_id = ? AND symbol = ?", new_shares, session["user_id"], Quote.get('symbol'))
        else:
            db.execute("INSERT INTO shares (user_id, symbol, symbol_name, shares) VALUES(?, ?, ?, ?)", session["user_id"], Quote.get('symbol'), Quote.get('name'), request.form.get("shares"))

        # update user cash
        user_new_cash = float_user_cash - (latest_price * user_shares)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_new_cash, session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # get transactions from db
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])

    return render_template("history.html", transactions=transactions)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        # Ensure Symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide Symbol", 400)

        # lookup symbol
        Quote = lookup(request.form.get("symbol"))

        # ensure symbol is valid
        if not Quote:
            return apology("invalid symbol", 400)
        if len(Quote) == 0:
            return apology("invalid symbol", 400)

        # sumbit Information to user
        else:
            companyName = Quote.get('name')
            latestPrice = Quote.get('price')
            symbol = Quote.get('symbol')
            return render_template("quoted.html", companyName=companyName, latestPrice=latestPrice, symbol=symbol)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username doesn't exist already
        if len(user) != 0:
            return apology("username already exists", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmed password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmed password", 400)

        # Ensure passwords match
        elif not request.form.get("password")==request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Insert user data into database
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))

    else:
        return render_template("register.html")

    #
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Ensure Symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide Symbol", 400)

        # Ensure Shares were submitted and positive integer
        elif not request.form.get("shares"):
            return apology("must provide Shares", 400)
        elif int(request.form.get("shares")) < 1:
            return apology("Shares must be > 0", 400)

        # lookup symbol
        Quote = lookup(request.form.get("symbol"))
        latest_price = float(Quote.get('price'))
        shares_to_sell = int(request.form.get("shares"))

        # ensure symbol is valid
        if len(Quote) == 0:
            return apology("invalid symbol", 400)

        # get user cash as float
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]
        float_user_cash = float(user_cash.get('cash'))

        # get stock info from db
        shares_db = db.execute("SELECT * FROM shares WHERE user_id = ? AND symbol = ?", session["user_id"], Quote.get('symbol'))
        user_shares = float(shares_db[0].get("shares"))

        # check if user owns the stock
        if len(shares_db) != 1:
            return apology("You dno't own any shares of this stock", 400)

        # check if user has enogh shares to sell
        if user_shares < shares_to_sell:
            return apology("You don't own enough shares of that stock", 400)

        # Delete symbol from shares table
        elif user_shares == shares_to_sell:
            db.execute("DELETE FROM shares WHERE user_id = ? AND symbol = ?", session["user_id"], Quote.get('symbol'))

        # Update shares table
        else:
            new_shares = user_shares - shares_to_sell
            db.execute("UPDATE shares SET shares = ? WHERE user_id = ? AND symbol = ?", new_shares, session["user_id"], Quote.get('symbol'))

        # update user cash
        user_new_cash = float_user_cash + (latest_price * shares_to_sell)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_new_cash, session["user_id"])

        # update transactions table
        transaction_type = 'sell'
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute("INSERT INTO transactions (user_id, transaction_type, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], transaction_type,  Quote.get('symbol'), request.form.get("shares"), latest_price, date)

        return redirect("/")

    else:
        symbols = db.execute("SELECT symbol FROM shares WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", symbols=symbols)
