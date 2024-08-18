import io
from flask import Flask, redirect, render_template, url_for, request, session, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as plt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'letsorihdjd'
app.config['SQLACLHEMY_DATABASE_URI'] = 'sqlite:///expense.db'

db = SQLAlchemy(app)

expenses = []

@app.route("/", methods=['GET', 'POST'])
def index():
     return render_template('index.jinja', expenses=expenses)

@app.route("/category_chart")
def category_chart():
    # Sample data - Replace this with your database query
    categories = ['Food', 'Travel', 'Bills', 'Entertainment']
    expenses = [120, 450, 320, 150]

    # Create a bar chart
    fig, ax = plt.subplots()
    ax.bar(categories, expenses)
    ax.set_xlabel('Category')
    ax.set_ylabel('Expenses')
    ax.set_title('Expenses by Category')

    # Save it to a BytesIO object
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)  # Close the figure to prevent resource leaks

    return send_file(img, mimetype='image/png')



@app.route("/add", methods=['GET','POST'])
def addExpense():
    if request.method == 'POST':
        expense = request.form['expense']
        if expense:
            expenses.append(expense)
            return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/summary_report')
def summary_report():
    # Sample data - Replace this with your database query
    categories = ['Food', 'Travel', 'Bills', 'Entertainment']
    expenses = [120, 450, 320, 150]
    totalofexpenses = sum(expenses)
    
    # You can add more calculations and pass them to the template
    
    return render_template('summary_report.html', categories=categories, expenses=expenses, totalofexpenses=totalofexpenses)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)