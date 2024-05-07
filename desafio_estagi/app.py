from flask import Flask, jsonify, request, render_template, send_file
import pandas as pd

app = Flask(__name__)

dados = {
    1: ["Acre", "Amapa", "Amazonas", "Para", "Rondonia", "Roraima", "Tocantins"],
    2: ["Alagoas", "Bahia", "Ceara", "Maranhao", "Paraiba", "Pernambuco", "Piaui", "Rio Grande do Norte", "Sergipe"],
    3: ["Goias", "Mato Grosso", "Mato Grosso do Sul"],
    4: ["Espirito Santo", "Minas Gerais", "Rio de Janeiro", "Sao Paulo"],
    5: ["Parana", "Rio Grande do Sul", "Santa Catarina"]
}

@app.route('/<int:id>/estados', methods=['GET'])
def listar_estados(id):
    ordem = request.args.get('ordem', 'asc')
    if id in dados:
        estados = sorted(dados[id], reverse=(ordem == 'desc'))
        return jsonify(estados)
    else:
        return jsonify({"erro": "Região não encontrada"}), 404

@app.route('/<int:id>/csv', methods=['GET'])
def gerar_csv(id):
    ordem = request.args.get('ordem', 'asc')
    if id in dados:
        estados = sorted(dados[id], reverse=(ordem == 'desc'))
        df = pd.DataFrame(estados, columns=["Estado"])
        csv_path = f"estados_{id}.csv"
        df.to_csv(csv_path, index=False)
        return send_file(csv_path, as_attachment=True, download_name=f"estados_{id}.csv")
    else:
        return jsonify({"erro": "Região não encontrada"}), 404

@app.route('/<int:id>/excel', methods=['GET'])
def gerar_excel(id):
    ordem = request.args.get('ordem', 'asc')
    if id in dados:
        estados = sorted(dados[id], reverse=(ordem == 'desc'))
        df = pd.DataFrame(estados, columns=["Estado"])
        excel_path = f"estados_{id}.xlsx"
        df.to_excel(excel_path, index=False, engine='openpyxl')
        return send_file(excel_path, as_attachment=True, download_name=f"estados_{id}.xlsx")
    else:
        return jsonify({"erro": "Região não encontrada"}), 404

@app.route('/')
def home():
    return render_template('desafio.html')

if __name__ == '__main__':
    app.run(debug=True)

