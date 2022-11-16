# save this as app.py
from flask import Flask, escape, request, render_template
import pickle
import numpy as np
app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))


@app.route('/home')
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/prediction', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # filtering the input values manually
        # gender
        if gender == "Males":
            male = 1
        else:
            male = 0

        # married
        if married == "Yes":
            married_yes = 1
        else:
            married_yes = 0

        # dependents
        if dependents == '1':
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0

        elif dependents == '2':
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif dependents == '3+':
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0

        # education
        if education == "Not Graduate":
            not_graduate = 1
        else:
            not_graduate = 0

        # employed
        if employed == "Yes":
            employed_yes = 1
        else:
            employed_yes = 0

        # property area
        if area == "Semiurban":
            semiurban = 1
            urban = 0
        elif area == "Urban":
            semiurban = 0
            urban = 0
        else:
            semiurban = 0
            urban = 0

        ApplicantIncomeLog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountLog = np.log(LoanAmount)
        Loan_Amount_TermLog = np.log(Loan_Amount_Term)

        # print(credit, ApplicantIncomeLog, LoanAmountLog, Loan_Amount_TermLog, totalincomelog,
        #                           male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes, semiurban, urban)

        prediction = model.predict([[credit, ApplicantIncomeLog, LoanAmountLog, Loan_Amount_TermLog, totalincomelog,
                                   male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes, semiurban, urban]])

        print(prediction)

        if prediction == "N":
            prediction = "NO"
        else:
            prediction = "YES"

        return render_template("prediction.html", prediction_val="Loan Status is {}".format(prediction))

    else:
        return render_template("prediction.html")
    

if __name__ == "__main__":
    app.run(debug=True)
