# importamos o pyqt para ler o arquivo uic, e o qtwidgets para ler a tela a interface
from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0

# criamos uma variavel que recebe uma instancia do mysql.conector
banco = mysql.connector.connect(
    host="192.141.196.215",
    user="semprebom",
    passwd="semprebom",
    database="cadastro_produtos"
)

def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    numero_id = valor_id

    tela_editar.show()
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_4.setText(str(produto[0][2]))
    tela_editar.lineEdit_5.setText(str(produto[0][3]))
    tela_editar.lineEdit_6.setText(str(produto[0][4]))

def salvar_dados_editados(): 
    #pega o numero do id   
    global numero_id
    # valor digitado no lineEdit
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_4.text()
    preco = tela_editar.lineEdit_5.text()
    categoria = tela_editar.lineEdit_6.text()
    #atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = {}".format(codigo,descricao,preco,categoria,numero_id))
    tela_editar.close()
    segunda_tela.close()
    segunda_tela.show()
    chama_segunda_tela()

def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))
    

# aula numero 6 rever...
def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CODIGO")
    pdf.drawString(210, 750, "PRODUTO")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))  

    pdf.save()
    print("PDF GERADO COM SUCESSO!")



# uma fnção para ler os campos que vai ser disprada pelo botão
def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    
    categoria = ""

    if formulario.radioButton.isChecked():
        print("Categoria Informatica foi selecionado:")
        categoria = "Informatica"
    elif formulario.radioButton_2.isChecked():
        print("Categoria Alimentos foi selecionado:")
        categoria = "Alimentos"
    else:
        print("Categoria Eletronicos foi selecionado:")
        categoria = "Eletronicos"

    print("Codigo",linha1)
    print("Descricao",linha2)
    print("Preco",linha3)

    # "cursor" criamos um cursor com a instancia do banco que está fora da função principal DEF
    # "comando_SQL" em seguida criamos uma string sql para qual comando utilizar o comando inserir produtos na ordem aonde deixamos o valor
        # porcentagem "s" pq o valor que eu quero vou enviar como STRING
    # "dados" criei outra @var-dados aonde temos linha1,2,3 aonde criei na parte anterior do meu código na função principal
        #que recebe o que foi digitado dentro da lista, o str é pra converter a variavel em ums string
    #"cursor.execute" recebe dois parametros qual o comando SQL será digitado ele vai substituir %s por str  que
        # passa no segundo parametro dados
    #"banco.commit" manda o comando para o mysql 
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    

    # pega a segunda tela com o nome do componete tablewidget que é a tela branca e coma setRowCount eu afirmo qtas linhas
        # vai ter a minha tabela fiz uma parametro de len(dados_lidos para saber qtas linhas terá a tabela
    # na segunda linha defino o numero de coluna setColumnCount(5) com um valor que é fixo

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)


# dois for's percorrendo uma matriz 
    #primeiro for vai de zero até o tamanho de n° de linhas e o de baixo vai de zero a cinco 
# elemento setItem preciso passar a posição que eu quero inserir na tabela as letras i, j é pq etsamos dentro do for 
   # e as mesmas valem zero na 1° e 2° iteração epercorrem cada item da tabela, aqui str(dados_lidos[i][j]))) é o que 
        # eu quero que apareça na tabela cada elemento lido na posições i e j e o str é para converte entre () em string

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


# objeto app aonde usa a classe QtWidgets e onde cria aplicação 
app=QtWidgets.QApplication([])

# temos o object formulario aonde usa o uic ou loaduic e carrega nosso arquivo
formulario=uic.loadUi("formulario.ui")
segunda_tela=uic.loadUi("listar_dados.ui")
tela_editar=uic.loadUi("menu_editar.ui")

#então podemos usar nosso botão associando ao qt-designer usando metodo clicar aonde clicar no botão usa o DEF
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados_editados)

formulario.show()
app.exec()


