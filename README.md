# Comparador de Preços de RAM - Kabum

Projeto de web scraping para buscar e comparar preços de memórias RAM no Kabum.

## Site Rastreado

- **Kabum** - https://www.kabum.com.br

## Funcionalidades

- Buscar preços de RAM por quantidade (4GB, 8GB, 16GB, 32GB, 64GB, etc.)
- Ordenar do mais barato ao mais caro
- Exibir os 3 mais baratos
- Exibir link para o produto
- Filtrar apenas produtos de memória RAM

## Como Usar

1. Ative o ambiente virtual:
```bash
venv\Scripts\activate
```

2. Instale as dependências (se necessário):
```bash
pip install -r requirements.txt
```

3. Execute o script:
```bash
python Scraping.py
```

Ou especifique a quantidade de GB:
```bash
python Scraping.py 16
python Scraping.py 32
```

## Dependências

- selenium - Para automação de navegador
- webdriver-manager - Para gerenciar drivers do Chrome
- pandas - Para organizar e exibir os dados

## Notas

- Os preços podem variar conforme a disponibilidade e promoções
- Verifique sempre as condições de compra e prazos de entrega diretamente no site
- Este projeto é para fins educacionais
