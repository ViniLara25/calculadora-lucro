from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# 1. Cria a instância do Flask
app = Flask(__name__, static_folder='static')
CORS(app)

# 2. Configura a app e o banco de dados
import os

# Pega a URL do banco de dados do ambiente, ou usa o SQLite se ela não existir
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///produtos.db'

# 3. Cria a instância do banco de dados
db = SQLAlchemy(app)

# 4. Define o modelo de dados
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=False, nullable=False)
    valor_pago = db.Column(db.Float, nullable=False)
    lucro_percentual = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    valor_icms = db.Column(db.Float, nullable=False)
    valor_liquido = db.Column(db.Float, nullable=False)
    lucro_final = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome}>'

# 5. Sua função de cálculo e a rota da API
def calcular_preco(produto, valor_pago, lucro_percentual):
    icms_aliquota = 0.18
    
    valor_venda_sugerido = valor_pago / (1 - lucro_percentual / 100 - icms_aliquota)
    valor_icms_descontado = valor_venda_sugerido * icms_aliquota
    valor_liquido = valor_venda_sugerido - valor_icms_descontado
    lucro_final = valor_liquido - valor_pago
    
    return {
        "item": produto,
        "valor_pago": valor_pago,
        "margem_lucro": lucro_percentual,
        "imposto_icms": icms_aliquota * 100,
        "preco_venda_sugerido": valor_venda_sugerido,
        "valor_icms_descontado": valor_icms_descontado,
        "valor_liquido": valor_liquido,
        "lucro_final": lucro_final
    }

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.get_json()
    
    produto = dados['produto']
    valor_pago = float(dados['valor'])
    lucro_percentual = float(dados['lucro'])
    
    resultados = calcular_preco(produto, valor_pago, lucro_percentual)
    
    # Cria uma nova instância da classe Produto com os resultados
    novo_produto = Produto(
        nome=resultados['item'],
        valor_pago=resultados['valor_pago'],
        lucro_percentual=resultados['margem_lucro'],
        preco_venda=resultados['preco_venda_sugerido'],
        valor_icms=resultados['valor_icms_descontado'],
        valor_liquido=resultados['valor_liquido'],
        lucro_final=resultados['lucro_final']
    )
    
    # Adiciona e salva o novo produto no banco de dados
    db.session.add(novo_produto)
    db.session.commit()
    
    return jsonify(resultados)

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    lista_de_produtos = []
    for produto in produtos:
        lista_de_produtos.append({
            'id': produto.id,
            'nome': produto.nome,
            'valor_pago': produto.valor_pago,
            'margem_lucro': produto.lucro_percentual, # CORRIGIDO AQUI!
            'preco_venda_sugerido': produto.preco_venda,
            'valor_icms_descontado': produto.valor_icms,
            'valor_liquido': produto.valor_liquido,
            'lucro_final': produto.lucro_final
        })
    return jsonify(lista_de_produtos)

@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto deletado com sucesso!'})

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

# 6. Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()

# 7. Roda o servidor
if __name__ == '__main__':
    app.run(debug=True)