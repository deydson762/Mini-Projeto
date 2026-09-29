# Comparador de Preços de RAM

Projeto de web scraping para buscar e comparar preços de memórias RAM em diferentes lojas online brasileiras.

## Sites Rastreados

- **Kabum** - https://www.kabum.com.br
- **Terabyte** - https://www.terabyte.com.br
- **Pichau** - https://www.pichau.com.br

## Funcionalidades

- Buscar preços de RAM por quantidade (8GB, 16GB, 32GB, etc.)
- Comparar preços entre os 3 sites
- Ordenar do mais barato ao mais caro
- Exibir link para o produto

## Como Usar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o script:
```bash
python Scraping.py
```

3. Informe a quantidade de RAM desejada quando solicitado

## Dependências

- requests - Para fazer requisições HTTP
- beautifulsoup4 - Para parsear HTML
- pandas - Para organizar e exibir os dados

## Notas

- Os preços podem variar conforme a disponibilidade e promoções
- Verifique sempre as condições de compra e prazos de entrega diretamente no site
- Este projeto é para fins educacionais
