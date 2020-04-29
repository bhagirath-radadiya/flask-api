from flask import Flask, jsonify, json, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/apidb'
db = SQLAlchemy(app)


class LoginVO(db.Model):
    __tablename__ = 'login'
    loginId = db.Column('loginId', db.Integer, primary_key=True, autoincrement=True)
    loginUserName = db.Column('loginUserName', db.String(100), nullable=False)
    loginPassword = db.Column('loginPassword', db.String(100), nullable=False)

    def as_dict(self):
        return {
            'loginId': self.loginId,
            'loginUserName': self.loginUserName,
            'loginPassword': self.loginPassword
        }


db.create_all()


@app.route("/viewdata")
def viewdata():
    login_list = LoginVO.query.all()
    print(login_list)
    ls = []

    for i in login_list:
        dic = {}
        dic["loginId"] = i.loginId
        dic["loginUserName"] = i.loginUserName
        dic["loginPassword"] = i.loginPassword
        ls.append(dic)
    print(ls)
    
    #create json file 
    with open("data_file.json", "w") as write_file:
        json.dump(ls, write_file)

    return jsonify(ls)


@app.route("/insertdata/<username>/<password>")
def insertdata(username, password):
    loginvo = LoginVO()
    loginUserName = username
    loginPassword = password

    loginvo.loginUserName = loginUserName
    loginvo.loginPassword = loginPassword

    db.session.add(loginvo)
    db.session.commit()

    return redirect(url_for("viewdata"))


@app.route("/deletedata/<loginid>")
def deletedata(loginid):
    loginvo = LoginVO()
    loginId = loginid

    loginvo.loginId = loginId

    loginlist = LoginVO.query.get(loginvo.loginId)
    db.session.delete(loginlist)
    db.session.commit()

    return redirect(url_for("viewdata"))


app.run(debug=True)
