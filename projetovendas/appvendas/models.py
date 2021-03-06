from django.db import models

# Create your models here.

class Unidade(models.Model):
    descricao=models.CharField("Descrição",max_length=100)
    sigla=models.CharField("Sigla",max_length=5)

class Cargo(models.Model):
    descricao=models.CharField("Descrição",max_length=150)

class Pessoa(models.Model):
    nome=models.CharField("Nome",max_length=255)
    email=models.EmailField("E-Mail",max_length=200)
    telefone=models.CharField("Telefone",max_length=20)

    def __str__(self):
        return self.nome

class Cliente(Pessoa):
    endereco=models.CharField("Endereço",max_length=255)


class Funcionario(Pessoa):
    matricula=models.CharField("Matrícula",max_length=10)
    cargo=models.ForeignKey(Cargo,on_delete=models.PROTECT,verbose_name="Cargo")

class Produto(models.Model):
    descricao=models.CharField("Descrição",max_length=255)
    valorUnitario=models.DecimalField("Valor Unitário",max_digits=10,decimal_places=2)
    unidade=models.ForeignKey(Unidade,on_delete=models.PROTECT,verbose_name="Unidade")

class Venda(models.Model):
    dataVenda=models.DateField("Data da Venda")
    vendedor=models.ForeignKey(Funcionario,on_delete=models.PROTECT,verbose_name="Funcionário")
    cliente=models.ForeignKey(Cliente,on_delete=models.PROTECT,verbose_name="Cliente")
    produtos=models.ManyToManyField(Produto,through="VendaProduto")

    def calculaValorTotal(self):
        lista=VendaProduto.objects.filter(venda=self) # Filtra os itens vinculados a esta venda
        total=0
        for item in lista: # Percorre a lista de itens, calculando o valor unitário
            total=total + item.produto.valorUnitario * item.quantidade
        return total

class VendaProduto(models.Model):
    venda=models.ForeignKey(Venda,on_delete=models.CASCADE)
    produto=models.ForeignKey(Produto,on_delete=models.PROTECT)
    quantidade=models.IntegerField("Quantidade")
