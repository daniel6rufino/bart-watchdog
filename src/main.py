# src/main.py
from src.ai.model_loader import load_bart_model
from src.analysis.package_parser import parse_package_lock
from src.analysis.vulnerability_checker import load_known_vulns, check_vulnerabilities
from src.ai.interface import generate_summary
from src.report.report_generator import generate_json_report
from tabulate import tabulate

def main():
    print("[+] Carregando modelo BART...")
    model = load_bart_model()

    print("[+] Lendo dependências...")
    deps = parse_package_lock("data/sample_package-lock.json")

    print("[+] Carregando base de vulnerabilidades...")
    base_vulns = load_known_vulns()

    print("[+] Verificando vulnerabilidades...")
    vulns = check_vulnerabilities(model, deps, base_vulns)

    print("[+] Gerando resumo...")
    summary = generate_summary(vulns)

    final_output = {
        "watson_summary": summary,
        "vulnerable_dependencies": vulns
    }

    print("[+] Salvando relatório final...")
    generate_json_report(final_output)

    print("[✓] Análise concluída com sucesso.")
    print("""
    -----------------------------------
          
""")
    exibir_tabela_vulnerabilidades(vulns)

def exibir_tabela_vulnerabilidades(vulns):
    if not vulns:
        print("✅ Nenhuma vulnerabilidade encontrada!")
        return

    print("❌ Vulnerabilidades encontradas!\n")

    headers = ["(index)", "Pacote", "Versão", "CVE", "Descrição"]
    table = []

    for i, v in enumerate(vulns):
        table.append([
            i,
            v.get("package", "—"),
            v.get("version", "—"),
            v.get("cve", "—"),
            v.get("description", "—"),
        ])

    print(tabulate(table, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
