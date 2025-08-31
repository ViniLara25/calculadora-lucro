#Desenvolver um pequeno sistema para uma loja. Cadastro de produtos, calculo de preço final (com impostos) e exibir o total.
#1. Pedir ao usuário o nome do produto.
#2. Preço de custo do produto.
#3. Porcentagem de lucro desejada.
#4. Imposto sobre o valor de venda.

#Cadastro do produto.
produto = ""
while not produto: 
    produto = input("Digite o produto: ").strip()
if not produto: print("O produto não pode ficar em branco\n")
print ("Item cadastrado com sucesso\n");

#Valor pago pelo produto.

#valor_texto = ""
#while not valor_texto:
#    valor_texto = input("Digite o valor pago pelo produto: ").strip()
#    valor_correto = valor_texto.replace(",",".")
#    valor_pago = float(valor_correto)
#if not valor_texto: print("O valor não pode ficar em branco")

#print(f'O valor é: R${valor_pago:,.2f}')

while True: 
    try: 
        valor_texto = input("Digite o valor pago pelo produto: R$")
        valor_correto = valor_texto.replace(',','.')
        valor = float(valor_correto) 
        print("Valor cadastrado com sucesso!\n")
        break
    except ValueError: print("Valor inválido, digite novamente.\n")

#Margem de lucro.

while True:
    try:
        lucro_texto = input("Digite a porcentagem de lucro: ")
        lucro_correto = lucro_texto.replace(',','.')
        lucro = float(lucro_correto)
        print("Valor cadastrado com sucesso\n")
        break
    except ValueError: print("Valor inválido, digite novamente.\n")

#Calculos de venda com ICMS de São Paulo 18%.

lucro_final = lucro/100

imposto_icms = 0.18

valor_lucro = valor*lucro_final
valor_final = valor+valor_lucro

valor_venda_produto = (valor_final/(1-imposto_icms))
valor_produto = valor_venda_produto-(valor_venda_produto*imposto_icms)


resultado = valor_produto-valor
valor_debitado_icms = valor_venda_produto*imposto_icms
lucro_real_porcentagem = (valor_produto*100)/(valor)-100

print(f"\nItem cadastrado: {produto}. \nValor pago pelo produto: R${valor}. \nMargem de lucro: {lucro:,.2f}%. \nImposto ICMS sobre a venda do produto no estado de São Paulo: {imposto_icms*100}%. \n\nPreço de venda sugerido: R${valor_venda_produto:,.2f} \n\nValor do ICMS descontado: R${valor_debitado_icms:,.2f} \n\nValor líquido após ICMS: R${valor_produto:,.2f}")

if valor_produto <= valor:
    print(f"Você terá prejuizo com este item de: R${resultado:,.2f}")
else:
    print(f"Você terá lucro com a venda de: R${resultado:,.2f}")

print(f"\nPorcentagem real de lucro é de: {lucro_real_porcentagem:,.2f}%")