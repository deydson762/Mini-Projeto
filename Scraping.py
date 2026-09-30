from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def buscar_ram_kabum(gb):
    """
    Busca memórias RAM no Kabum de acordo com a quantidade de GB especificada usando Selenium.
    
    Args:
        gb (int): Quantidade de GB da memória RAM (ex: 8, 16, 32)
    
    Returns:
        list: Lista de dicionários com nome, preço e link dos produtos
    """
    url = f"https://www.kabum.com.br/busca/memoria-ram-{gb}gb"
    
    # Configurar Chrome em modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # Inicializar o driver do Chrome
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        driver.get(url)
        
        # Esperar a página carregar
        time.sleep(5)
        
        # Tentar encontrar produtos usando diferentes seletores
        produtos = []
        
        # Seletores possíveis para produtos no Kabum
        selectors = [
            '[data-testid="product-card"]',
            '.productCard',
            '[class*="productCard"]',
            '[class*="ProductCard"]',
            'article'
        ]
        
        product_elements = []
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    product_elements = elements
                    break
            except:
                continue
        
        if not product_elements:
            # Fallback: encontrar links que contenham '/produto/'
            links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/produto/"]')
            
            for link in links[:15]:  # Aumentar limite para 15
                try:
                    href = link.get_attribute('href')
                    text = link.text.strip()
                    # Limpar o texto do nome
                    import re
                    text = re.sub(r'Avaliação.*?de\s+\d+\.\d+', '', text)
                    text = re.sub(r'[\u2800-\u28FF\uE000-\uF8FF]', '', text)  # Remover caracteres especiais
                    text = re.sub(r'SELO:.*?$', '', text)  # Remover selos
                    text = re.sub(r'CUPOM.*?$', '', text)  # Remover cupons
                    text = re.sub(r'[✓★☆◉]', '', text)  # Remover símbolos de avaliação
                    text = ' '.join(text.split())  # Remover espaços extras
                    
                    # Extrair preço usando regex
                    preco = "Preço não disponível"
                    preco_match = re.search(r'R\$\s*[\d.,]+', text)
                    if preco_match:
                        preco = preco_match.group()
                        # Remover o preço do nome para não duplicar
                        text = re.sub(r'R\$\s*[\d.,]+.*?$', '', text)
                        text = ' '.join(text.split())
                    
                    # Filtrar apenas produtos que são realmente memórias RAM
                    if (text and href and len(text) > 10 and 
                        ('RAM' in text.upper() or 'DDR' in text.upper() or 
                         'MEMÓRIA' in text.upper() or 'MEMORY' in text.upper())):
                        produtos.append({
                            'nome': text[:100],  # Limitar tamanho
                            'preco': preco,
                            'link': href,
                            'loja': 'Kabum'
                        })
                except:
                    continue
            
            driver.quit()
            return produtos
        
        # Extrair dados dos produtos encontrados
        for element in product_elements:
            try:
                # Tentar extrair nome limpo
                nome = "Nome não encontrado"
                try:
                    # Tentar diferentes seletores para nome
                    nome_selectors = [
                        '[data-testid="product-name"]',
                        'h2.nameCard',
                        'h3.nameCard',
                        '[class*="productName"]',
                        '[class*="ProductCard"]'
                    ]
                    for selector in nome_selectors:
                        try:
                            nome_element = element.find_element(By.CSS_SELECTOR, selector)
                            nome = nome_element.text.strip()
                            # Limpar nome - remover avaliações e selos
                            import re
                            nome = re.sub(r'Avaliação.*?de\s+\d+\.\d+', '', nome)
                            nome = re.sub(r'[\u2800-\u28FF]', '', nome)  # Remover caracteres Braille
                            nome = ' '.join(nome.split())  # Remover espaços extras
                            if nome:
                                break
                        except:
                            continue
                except:
                    pass
                
                # Tentar extrair preço
                preco = "Preço não encontrado"
                try:
                    preco_element = element.find_element(By.CSS_SELECTOR, '[class*="price"], [class*="Price"], [class*="preco"]')
                    preco = preco_element.text.strip()
                except:
                    try:
                        # Tentar encontrar texto que contenha 'R$'
                        all_text = element.text
                        import re
                        preco_match = re.search(r'R\$\s*[\d.,]+', all_text)
                        if preco_match:
                            preco = preco_match.group()
                    except:
                        pass
                
                # Tentar extrair link
                link = ""
                try:
                    link_element = element.find_element(By.CSS_SELECTOR, 'a')
                    link = link_element.get_attribute('href')
                except:
                    pass
                
                if nome != "Nome não encontrado":
                    produtos.append({
                        'nome': nome,
                        'preco': preco,
                        'link': link,
                        'loja': 'Kabum'
                    })
                    
            except Exception as e:
                print(f"Erro ao extrair dados do produto: {e}")
                continue
        
        driver.quit()
        return produtos
        
    except Exception as e:
        print(f"Erro ao usar Selenium: {e}")
        return []

def main():
    import sys
    
    print("=== Comparador de Preços de RAM - Kabum ===")
    
    # Usar argumento de linha de comando por padrão
    if len(sys.argv) > 1:
        try:
            gb = int(sys.argv[1])
            print(f"Buscando memórias RAM de {gb}GB...")
        except ValueError:
            print("Por favor, digite um número válido.")
            print("Uso: python Scraping.py <quantidade_em_GB>")
            print("Exemplo: python Scraping.py 8")
            return
    else:
        # Se não tiver argumento, usar valor padrão
        gb = 8
        print("Usando valor padrão: 8GB")
        print("Para usar outro valor, execute: python Scraping.py <quantidade_em_GB>")
        print("Exemplo: python Scraping.py 16")
    
    produtos = buscar_ram_kabum(gb)
    
    if produtos:
        df = pd.DataFrame(produtos)
        
        # Converter preços para números para ordenação
        def converter_preco(preco_str):
            import re
            if preco_str == "Preço não disponível":
                return float('inf')
            # Extrair valor numérico do preço
            match = re.search(r'[\d.,]+', preco_str)
            if match:
                valor = match.group().replace('.', '').replace(',', '.')
                try:
                    return float(valor)
                except:
                    return float('inf')
            return float('inf')
        
        df['preco_num'] = df['preco'].apply(converter_preco)
        df = df.sort_values('preco_num')
        df = df.drop('preco_num', axis=1)
        
        print(f"\nEncontrados {len(produtos)} produtos:")
        
        # Usar encoding utf-8 para evitar erros de caracteres
        import sys
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
        print(df[['nome', 'preco', 'loja']].to_string(index=False))
        
        # Mostrar os 3 mais baratos
        print(f"\n=== Top 3 Mais Baratos ===")
        print(df.head(3)[['nome', 'preco', 'loja']].to_string(index=False))
    else:
        print("Nenhum produto encontrado.")

if __name__ == "__main__":
    main()
