from flask import Flask, request, render_template, jsonify
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client with your API key
client = OpenAI(api_key="use open api key ")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
       
        project_name = request.form.get("project_name")
        project_idea = request.form.get("project_idea")
        target_size = request.form.get("target_size")
        target_market = request.form.get("target_market")
        project_working = request.form.get("project_working")

       
        prompt = f"""
        I have a project with the following details:
        - Project Name: {project_name}
        - Project Idea: {project_idea}
        - Target Size: {target_size}
        - Target Market: {target_market}
        - Working Details: {project_working}

        Suggest:
        1. The best front-end and back-end technologies.
        2. Database or storage methods.
        3. Deployment platforms and scaling strategies.
        4. Estimated costs and security considerations.
        """

        try:
           
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a technical advisor providing project development suggestions."},
                          {"role": "user", "content": prompt}]
            )
            
            output = completion.choices[0].message.content.strip()
        except Exception as e:
            output = f"Error: {str(e)}"

        
        return render_template("index.html", result=output)

    return render_template("index.html", result=None)


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    try:
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_message}]
        )
        
        bot_message = completion.choices[0].message.content.strip()
        return jsonify({"response": bot_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
