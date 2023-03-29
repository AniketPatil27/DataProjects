from flask import Flask, escape, request, render_template
import pickle
import numpy as np
app = Flask(__name__)
model=pickle.load(open('model.pkl','rb'))


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        gender=request.form['Gender']
        married=request.form['Married']
        dependents=request.form['Dependents']
        education=request.form['Education']
        selfemployed=request.form['Self_Employed']
        propertyarea=request.form['Property_Area']
        credithistory=float(request.form['Credit_History'])
        loanstatus=request.form['Loan_Status']
        applicantincome=float(request.form['Applicant Income'])
        coapplicantincome=float(request.form['Coapplicant Income'])
        loanamount=float(request.form['Loan Amount'])
        loanamountterm=float(request.form['Loan Amount Term'])
        
        if (gender == "Male"):
            male=1
        else:
            male=0
        
        # married
        if(married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # dependents
        if(dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif(dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif(dependents=="3+"):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0  

        # education
        if (education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

        # employed
        if (selfemployed == "Yes"):
            employed_yes=1
        else:
            employed_yes=0

        # property area

        if(propertyarea=="Semiurban"):
            semiurban=1
            urban=0
        elif(propertyarea=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0


        ApplicantIncomelog = np.log(applicantincome)
        totalincomelog = np.log(applicantincome+coapplicantincome)
        LoanAmountlog = np.log(loanamount)
        Loan_Amount_Termlog = np.log(loanamountterm)
        
        prediction = model.predict([[credithistory, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Termlog, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes,semiurban, urban ]])

        if(prediction=="N"):
            prediction="Not Approved"
        else:
            prediction="Approved"

        return render_template("prediction.html",prediction_text="loan status is {}".format(prediction))

    else:
        return render_template("prediction.html")


if __name__=="__main__":
    app.run(debug=True)