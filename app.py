from flask import Flask, render_template_string, request
import joblib

app = Flask(__name__)

model = joblib.load("train/model.pkl")
vectorizer = joblib.load("train/tfidf_vectorizer.pkl")

class_labels = {
    0: "✅ Güvenli (Benign)",
    1: "❌ Phishing (Oltalama)",
    2: "❌ Defacement (Tahrifat)",
    3: "⚠️ Malware / Other"
}

HTML = """
<!doctype html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>🔍 URL Güvenlik Analizi</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      text-align: center;
      padding: 50px;
      background: #f8f9fa;
    }
    h2 {
      font-size: 28px;
      margin-bottom: 20px;
    }
    input[type=text] {
      width: 400px;
      padding: 12px;
      border: 2px solid #aaa;
      border-radius: 10px;
      font-size: 16px;
    }
    input[type=submit] {
      padding: 12px 20px;
      font-size: 16px;
      margin-left: 10px;
      border: none;
      border-radius: 10px;
      background-color: #007bff;
      color: white;
      cursor: pointer;
    }
    .result {
      margin-top: 30px;
      padding: 20px;
      border-radius: 10px;
      display: inline-block;
      background-color: white;
      box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }
    code {
      background: #e9ecef;
      padding: 4px 6px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <h2>🔍 URL Güvenli mi?</h2>
  <form method="post">
    <input type="text" name="url" placeholder="Örn: http://example.com" required>
    <input type="submit" value="Analiz Et">
  </form>

  {% if url %}
  <div class="result">
    <h3>🔗 URL: <code>{{ url }}</code></h3>
    <h3>🔎 Sonuç: <b>{{ result }}</b></h3>
  </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    url = None
    if request.method == "POST":
        url = request.form["url"]
        vect = vectorizer.transform([url])
        prediction = model.predict(vect)[0]
        result = class_labels.get(prediction, "Bilinmeyen")
    return render_template_string(HTML, result=result, url=url)

if __name__ == "__main__":
    app.run(debug=True)
