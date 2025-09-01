// Função para carregar e exibir a lista de produtos
async function carregarProdutos() {
    try {
        const response = await fetch('http://127.0.0.1:5000/produtos');
        const produtos = await response.json();
        
        const listaProdutosDiv = document.getElementById('lista-produtos');
        listaProdutosDiv.innerHTML = ''; // Limpa o conteúdo atual

        if (produtos.length === 0) {
            listaProdutosDiv.innerHTML = '<p>Nenhum produto cadastrado ainda.</p>';
            return;
        }

        let tabelaHtml = '<table><thead><tr><th>ID</th><th>Produto</th><th>Valor Pago</th><th>Lucro (%)</th><th>Preço Venda</th></tr></thead><tbody>';
        
        produtos.forEach(produto => {
            tabelaHtml += `
                <tr>
        <td>${produto.id}</td>
        <td>${produto.nome}</td>
        <td>R$ ${produto.valor_pago.toFixed(2)}</td>
        <td>${produto.margem_lucro.toFixed(2)}%</td>
        <td>R$ ${produto.preco_venda_sugerido.toFixed(2)}</td>
        <td><button class="remover-btn" data-id="${produto.id}">Remover</button></td>
    </tr>
            `;
        });

        tabelaHtml += '</tbody></table>';
        listaProdutosDiv.innerHTML = tabelaHtml;

    } catch (error) {
        console.error('Erro ao carregar os produtos:', error);
        document.getElementById('lista-produtos').innerHTML = '<p>Erro ao carregar a lista de produtos.</p>';
    }
}

// Evento para o botão de calcular
document.getElementById('calcular').addEventListener('click', async function() {
    const produto = document.getElementById('produto').value;
    const valor = document.getElementById('valor').value;
    const lucro = document.getElementById('lucro').value;

    const dados = {
        produto: produto,
        valor: parseFloat(valor),
        lucro: parseFloat(lucro)
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/calcular', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const resultados = await response.json();
        const formatar = (valor) => parseFloat(valor).toFixed(2).replace('.', ',');

        const resultadoTexto = `
            Item cadastrado: ${resultados.item}
            Valor pago pelo produto: R$ ${formatar(resultados.valor_pago)}
            Margem de lucro: ${resultados.margem_lucro.toFixed(2)}%
            Imposto ICMS sobre a venda do produto no estado de São Paulo: ${resultados.imposto_icms}%
            Preço de venda sugerido: R$ ${formatar(resultados.preco_venda_sugerido)}
            Valor do ICMS descontado: R$ ${formatar(resultados.valor_icms_descontado)}
            Valor líquido após ICMS: R$ ${formatar(resultados.valor_liquido)}
            Você terá lucro com a venda de: R$ ${formatar(resultados.lucro_final)}
        `;
        
        document.getElementById('resultado').innerText = resultadoTexto;
        
        // Carrega a lista de produtos novamente para incluir o novo item
        carregarProdutos();

    } catch (error) {
        alert("Ocorreu um erro ao conectar com o servidor. Verifique se o servidor Python está rodando.");
        console.error('Erro:', error);
    }
});

// Chama a função para carregar os produtos quando a página for carregada
document.addEventListener('DOMContentLoaded', carregarProdutos);

// Adiciona um listener de evento para os botões de remover
document.addEventListener('click', async function(event) {
    if (event.target.classList.contains('remover-btn')) {
        const produtoId = event.target.getAttribute('data-id');
        const confirmacao = confirm(`Tem certeza que deseja remover o produto com ID ${produtoId}?`);
        
        if (confirmacao) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/produtos/${produtoId}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    alert('Produto removido com sucesso!');
                    carregarProdutos(); // Recarrega a lista
                } else {
                    alert('Erro ao remover o produto.');
                }
            } catch (error) {
                console.error('Erro:', error);
                alert('Erro ao conectar com o servidor para remover o produto.');
            }
        }
    }
});