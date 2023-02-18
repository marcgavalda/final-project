from flask import Flask, render_template, request
import openai
import re

secrets_dict={}
secrets = open('../secrets.txt')
for line in secrets:
    (key,val) = line.replace('\n','').split(';')
    secrets_dict[key] = val


openai.organization = secrets_dict['OpenAIorg']
openai.api_key = secrets_dict['OpenAI']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        device = request.form.get('device')
        if device == 'HEADPHONE':
            return render_template('headphone.html')
    return render_template('index.html')

@app.route('/headphone', methods=['POST'])
def headphone():
    brand = request.form.get('brand')
    model = request.form.get('model')
    color = request.form.get('color')
    form_factor = request.form.get('form_factor')
    free_form = request.form.get('free_form')
    connectivity = request.form.get('connectivity')

    # Generate a title and bullet points using OpenAI's GPT-3
    prompt = f"Create an objective title for a headphone, brand is {brand}, model name is {model}, color is {color}, form factor is {form_factor} and connectivity technology is {connectivity}"
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=40,
        n=1,
        stop=None,
        temperature=0.2,
    )
    title = completions.choices[0].text.strip()

    prompt = f"Create 3 very compelling Amazon bullet points for a headphone. The main topic(s) you should highlight are {free_form}. In addition, brand is {brand}, model name is {model}, color is {color}, form factor is {form_factor} and connectivity technology is {connectivity}.Start bullet-points with ·"
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    bullet_points = completions.choices[0].text.strip()
    bullet_points = [re.sub(r'^·\s*', '', s) for s in re.split(r'[\s\n]+·\s*', bullet_points)[:3]]
    bullet_points = [bp.replace("'", '"') for bp in bullet_points]

    return render_template('headphone.html', title=title, bullet_points=zip(bullet_points))

if __name__ == '__main__':
    app.run(debug=True)
