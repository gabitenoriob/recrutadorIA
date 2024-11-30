import os
from flask import Flask, jsonify, render_template, request
import fitz 
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Carregar modelo de embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(job_description, resume_text):
    """
    Calcula a similaridade entre a descrição da vaga e o texto do currículo.
    """
    # Gerar embeddings
    job_embedding = model.encode([job_description], convert_to_tensor=True)
    resume_embedding = model.encode([resume_text], convert_to_tensor=True)
    
    # Calcular similaridade coseno
    similarity_score = cosine_similarity(job_embedding.cpu().numpy(), resume_embedding.cpu().numpy())
    return similarity_score[0][0]

# Carregar o modelo spaCy
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extrai texto de um arquivo PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def process_resume(text):
    """Processa o texto do currículo com spaCy."""
    doc = nlp(text)
    filtered_tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    return {
        "filtered_tokens": filtered_tokens,
        "named_entities": named_entities,
    }

def extract_entities(text):
    """Extrai entidades específicas do texto."""
    doc = nlp(text)
    entities = {
        "Qualifications": [],
        "Experience": [],
        "Company": [],
        "Education": [],
        "Skills": [],
    }

    # Dividir texto por linhas para busca mais direcionada
    lines = text.split('\n')
    for line in lines:
        lower_line = line.lower()
        if "qualification" in lower_line:
            entities["Qualifications"].append(line.strip())
        elif "experience" in lower_line:
            entities["Experience"].append(line.strip())
        elif "company" in lower_line or "company name city" in lower_line:
            entities["Company"].append(line.strip())
        elif "education" in lower_line:
            entities["Education"].append(line.strip())
        elif "skill" in lower_line:
            entities["Skills"].append(line.strip())

    return entities

def evaluate_resume(similarity_score):
    """Avalia o currículo com base na similaridade."""
    if similarity_score > 0.85:
        return "Aprovado"
    elif similarity_score > 0.65:
        return "Aprovado parcialmente"
    else:
        return "Reprovado"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Pasta para armazenar uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
processed_results = []  # Armazena os resultados processados

# Rota só p renderizar o front
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return jsonify({"message": "Requisição POST recebida na raiz."})
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist("files")
    allowed_extensions = {'.pdf'}
    job_description = """
    Job Title: Senior IT Director

About the Role: We are seeking a highly skilled Senior IT Director to lead our technology team and participate in defining the strategic initiatives of IT within the organization. The ideal candidate will be responsible for overseeing the implementation of innovative technology solutions, ensuring the security, integrity, and efficiency of information systems at all organizational levels.

Responsibilities:

Lead and oversee the execution of IT strategies, focusing on system integration and information security.
Collaborate with internal teams to understand business needs and translate those requirements into technical solutions.
Supervise the implementation of critical systems, including secure communication networks, data management systems, and IT infrastructure.
Help the organization achieve certification and compliance in health information exchange networks and other federal and non-federal standards.
Manage large-scale IT projects using agile and lean methodologies to ensure on-time and on-budget delivery.
Coordinate the deployment of new software systems, management systems, and communication tools within the organization.
Ensure all privacy, security, and confidentiality policies are being properly followed.
Required Qualifications:

10+ years of experience in IT, with at least 5 years in leadership roles.
Proven experience in implementing IT systems in regulated environments such as healthcare or government sectors.
Expertise in secure network architecture, systems integration, and managing large volumes of data.
Experience with project management tools such as MS Project, JIRA, or other task tracking and version control systems.
Strong communication skills and the ability to work effectively with internal and external stakeholders.
Knowledge of agile frameworks and IT project management.
Preferred Skills:

Experience with cloud computing platforms such as AWS, Azure, or Google Cloud.
Familiarity with containerization technologies like Docker and Kubernetes.
Experience with database management and data analytics tools, including SQL and NoSQL.
    """  

    for file in files:
        if file:
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in allowed_extensions:
                continue
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            # Processar texto do arquivo
            if file_extension == '.pdf':
                text = extract_text_from_pdf(file_path)
            else:
                continue
            
            # Calcular a similaridade entre a descrição da vaga e o currículo
            similarity_score = calculate_similarity(job_description, text)
            
            # Avaliar o currículo com base na pontuação de similaridade
            evaluation = evaluate_resume(float(similarity_score))  # Converte a similaridade para float
            
            # Adicionar resultado processado
            processed_results.append({
                "file": file.filename,
                "similarity_score": float(similarity_score),  # Converte para float
                "evaluation": evaluation,
            })

    return jsonify({"message": "Arquivos carregados e processados!"})

# Método para retornar resultado de cada currículo na caixa de texto depois da análise usando IA
@app.route('/result', methods=['GET'])
def result():
    if not processed_results:
        return jsonify({"message": "Nenhum currículo foi processado ainda."})
    
    return jsonify({
        "message": "Resultados da análise.",
        "results": processed_results,
    })

if __name__ == "__main__":
    app.run(debug=True)
