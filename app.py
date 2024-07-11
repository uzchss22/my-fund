from flask import Flask, render_template, jsonify
import db
import crawler
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert')
def insert_data():
    total_proceeds, day_proceeds = crawler.crawling_data()
    db.insert_proceeds(total_proceeds, day_proceeds)
    return jsonify({"message": "Data inserted successfully"})

@app.route('/data')
def get_data():
    data = db.fetch_data()
    return jsonify(data)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(crawler.crawling_data, 'cron', hour="17")
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
