from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Coleta os valores do formulário
            valor_conta_str = request.form.get('valor_conta')
            quantidade_pessoas_str = request.form.get('quantidade_pessoas')
            percentual_gorjeta_str = request.form.get('percentual_gorjeta')

            # Validação: campos preenchidos
            if not valor_conta_str or not quantidade_pessoas_str or not percentual_gorjeta_str:
                flash('Todos os campos são obrigatórios.', 'danger')
                return render_template('index.html')

            # Conversão e validação de tipos
            try:
                valor_conta = float(valor_conta_str)
                quantidade_pessoas = int(quantidade_pessoas_str)
                percentual_gorjeta = float(percentual_gorjeta_str)
            except ValueError:
                flash('Por favor, insira valores numéricos válidos.', 'danger')
                return render_template('index.html')

            # Validação de valores lógicos
            if valor_conta <= 0:
                flash('O valor da conta deve ser maior que zero.', 'danger')
                return render_template('index.html')
            
            if quantidade_pessoas <= 0:
                flash('A quantidade de pessoas deve ser pelo menos 1.', 'danger')
                return render_template('index.html')
            
            if percentual_gorjeta < 0:
                flash('O percentual de gorjeta não pode ser negativo.', 'danger')
                return render_template('index.html')

            # Cálculos
            valor_gorjeta = valor_conta * (percentual_gorjeta / 100)
            valor_total = valor_conta + valor_gorjeta
            valor_por_pessoa = valor_total / quantidade_pessoas

            # Classificação
            if percentual_gorjeta < 5:
                classificacao = 'Mão de vaca'
            elif 5 <= percentual_gorjeta <= 15:
                classificacao = 'Legal'
            else:
                classificacao = 'Generoso'

            # Renderiza a página de resultados com os dados calculados
            return render_template('resultado.html', 
                                 valor_gorjeta=valor_gorjeta,
                                 valor_total=valor_total,
                                 valor_por_pessoa=valor_por_pessoa,
                                 classificacao=classificacao)

        except Exception as e:
            flash(f'Ocorreu um erro inesperado: {str(e)}', 'danger')
            return render_template('index.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
