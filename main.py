from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Rota para exibir a página inicial com as categorias de votação
@app.route('/votar', methods=['POST'])
def votar():
    dados_voto = request.json  # Recebe os dados do voto (categoria e candidato) do front-end
    categoria = dados_voto.get('categoria')
    candidato = dados_voto.get('candidato')

    # Carrega os votos existentes do arquivo JSON
    with open('votos.json', 'r') as file:
        votos = json.load(file)

    # Atualiza a contagem de votos para a categoria e candidato correspondentes
    if categoria in votos and candidato in votos[categoria]:
        votos[categoria][candidato] += 1
    else:
        votos.setdefault(categoria, {})[candidato] = 1

    # Salva os votos atualizados de volta no arquivo JSON
    with open('votos.json', 'w') as file:
        json.dump(votos, file, indent=2)

    return jsonify({'message': 'Voto registrado com sucesso!'}), 200

# Rota para recuperar os resultados dos votos
@app.route('/resultados', methods=['GET'])
def obter_resultados():
    try:
        # Lê o arquivo votos.json para recuperar os resultados dos votos
        with open('votos.json', 'r') as file:
            resultados = json.load(file)
        return jsonify(resultados), 200
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de votos não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para reinicializar os votos para zero
@app.route('/resetar-votos', methods=['POST'])
def resetar_votos():
    try:
        # Abre o arquivo votos.json para leitura
        with open('votos.json', 'r') as file:
            votos = json.load(file)  # Carrega os votos existentes

        # Zera o número de votos para cada candidato em cada categoria
        for categoria, candidatos in votos.items():
            for candidato in candidatos:
                votos[categoria][candidato] = 0

        # Salva os votos atualizados de volta no arquivo JSON
        with open('votos.json', 'w') as file:
            json.dump(votos, file, indent=2)

        return jsonify({'message': 'Número de votos reiniciado para todos os candidatos em todas as categorias!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,  port=os.getenv("PORT", default=5000))