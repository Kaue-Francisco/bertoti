from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/ia', methods=['POST'])
def ia():
    # Obtendo o texto do corpo da requisição
    text = request.json.get('text')
    
    try:
        # Fazendo a requisição para a API externa
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": text,
                "stream": False
            }
        )
        
        # Verificando o status da resposta
        if response.status_code == 200:
            # Decodificando o JSON da resposta
            data = response.json()  # Transforma o JSON em um dicionário
            return jsonify({"response": data.get('response', '')})
        else:
            return jsonify({"error": "Failed to fetch data from the API"}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)