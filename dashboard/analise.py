"""Preparação dos dados e estatística do survey (Seções 3 e 5 do protocolo).

Este módulo não depende do Streamlit, para poder ser conferido isoladamente.
Todas as regras de elegibilidade, descarte e os testes seguem o protocolo da
Parte 1. Qualquer decisão que o protocolo não fixou está marcada com
"DECISÃO OPERACIONAL" e aparece na página de metodologia do dashboard.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# --------------------------------------------------------------------------
# Parâmetros fixados no protocolo
# --------------------------------------------------------------------------
ALPHA = 0.05
Z95 = 1.96
N_META = 50
MIN_SEGMENTO = 5  # Seção 6: não exibir segmentos com menos de 5 pessoas
JANELA_COLETA = (pd.Timestamp("2026-11-09 00:00:00"), pd.Timestamp("2026-11-13 23:59:59"))

# DECISÃO OPERACIONAL: o protocolo cita permutação e bootstrap sem fixar
# número de reamostragens nem semente. Fixamos para o resultado ser reprodutível.
SEMENTE = 20261109
N_PERMUTACOES = 10_000
N_BOOTSTRAP = 5_000

PP_ITENS = ["PP1", "PP2", "PP3", "PP4", "PP5"]
PP_TEXTO = {
    "PP1": "PP1. Concluo minhas tarefas mais rápido",
    "PP2": "PP2. Entrego mais tarefas no mesmo período",
    "PP3": "PP3. A qualidade do código que entrego é melhor",
    "PP4": "PP4. Preciso refazer menos o código depois de entregue",
    "PP5": "PP5 (invertido). O trabalho fica mais cansativo ou trabalhoso",
}
LIKERT = {
    1: "Discordo totalmente",
    2: "Discordo",
    3: "Nem concordo nem discordo",
    4: "Concordo",
    5: "Concordo totalmente",
}
U1_ROTULOS = {
    1: "1 - Nunca",
    2: "2 - Uma ou poucas vezes no período",
    3: "3 - Algumas vezes por mês",
    4: "4 - Algumas vezes por semana",
    5: "5 - Todos ou quase todos os dias",
}
# Opções exatamente como aparecem no Google Formulários
OPCOES_T2 = ["Emprego", "Estágio", "Trabalho autônomo", "Outro"]
OPCOES_P2 = [
    "Até 10 pessoas",
    "11 a 50 pessoas",
    "51 a 200 pessoas",
    "201 a 1000 pessoas",
    "Mais de 1000 pessoas",
    "Não se aplica (trabalho autônomo)",
]
OPCOES_P3 = ["Menos de 3 meses", "3 a 6 meses", "6 a 12 meses", "Mais de 12 meses"]
OPCOES_P4 = ["ChatGPT", "GitHub Copilot", "Claude", "Gemini", "Cursor"]
OPCOES_P5 = [
    "Escrever código",
    "Completar código",
    "Explicar código",
    "Revisar código",
    "Escrever testes",
    "Depurar código",
    "Planejar ou projetar código",  # incluída após o pré-teste (Seção 4)
]
OUTRA = "Outra (não codificada)"

FAIXAS_P1 = [(0, 2), (3, 5), (6, 10), (11, None)]
CLASSES_PP = ["Abaixo do neutro (1–2)", "Neutro (3)", "Acima do neutro (4–5)"]

# Cabeçalhos do CSV do Google Formulários -> código do item.
# Colunas que não casam (F1 a F5 do pré-teste, texto livre) são descartadas
# na leitura: o dashboard nunca carrega texto livre (Seção 6).
PADROES_COLUNAS = {
    "carimbo": r"^Carimbo de data",
    "C0": r"^C0\.",
    "T1": r"^T1\.",
    "T2": r"^T2\.",
    "U1": r"^U1\.",
    "U2": r"^U2\.",
    "P1": r"^P1\.",
    "P2": r"^P2\.",
    "P3": r"^P3\.",
    "P4": r"^P4\.",
    "P5": r"^P5\.",
    "PP1": r"\[PP1\.",
    "PP2": r"\[PP2\.",
    "PP3": r"\[PP3\.",
    "PP4": r"\[PP4\.",
    "PP5": r"\[PP5\.",
    "AT1": r"\[AT1\.",
}
OBRIGATORIOS = ["T2", "U1", "U2", "P1", "P2", "P3", "P4", "P5", *PP_ITENS, "AT1"]


# --------------------------------------------------------------------------
# Leitura e preparação
# --------------------------------------------------------------------------
def ler_arquivo(origem, nome: str = "dados.csv") -> pd.DataFrame:
    """Lê a exportação bruta CSV ou XLSX sem alterar o arquivo.

    No XLSX do Google Formulários, usa a primeira planilha não vazia. Isso
    ignora abas auxiliares vazias sem depender do nome traduzido da aba.
    """
    sufixo = Path(nome).suffix.lower()
    if sufixo == ".csv":
        return pd.read_csv(origem, dtype=str, keep_default_na=False, encoding="utf-8")
    if sufixo == ".xlsx":
        planilhas = pd.read_excel(origem, sheet_name=None, dtype=str, keep_default_na=False)
        for df in planilhas.values():
            if len(df.columns) and len(df):
                return df
        raise ValueError("A planilha XLSX não contém uma aba com respostas.")
    raise ValueError("Formato não aceito. Use a exportação CSV ou XLSX do Google Formulários.")


def ler_csv(origem) -> pd.DataFrame:
    """Compatibilidade com chamadas existentes que fornecem CSV."""
    return ler_arquivo(origem, "dados.csv")


def localizar_colunas(colunas) -> dict[str, str]:
    mapa: dict[str, str] = {}
    for col in colunas:
        nome = str(col).strip()
        for chave, padrao in PADROES_COLUNAS.items():
            if chave not in mapa and re.search(padrao, nome):
                mapa[chave] = col
                break
    return mapa


def _primeiro_digito(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.str.extract(r"^\s*(\d)", expand=False), errors="coerce")


def _faixa_p1(anos: float) -> str | None:
    if pd.isna(anos):
        return None
    for lo, hi in FAIXAS_P1:
        if anos >= lo and (hi is None or anos <= hi):
            return rotulo_faixa(lo, hi)
    return None


def rotulo_faixa(lo: int, hi: int | None) -> str:
    return f"{lo} ou mais" if hi is None else f"{lo} a {hi}"


ORDEM_FAIXAS = [rotulo_faixa(lo, hi) for lo, hi in FAIXAS_P1]


def _multipla(valor: str, opcoes: list[str], codificacao: dict[str, str]) -> set[str]:
    """Separa uma resposta de múltipla escolha. Texto fora da lista vai para
    a categoria definida no livro de códigos ou, se não houver, para OUTRA."""
    marcadas: set[str] = set()
    if not valor:
        return marcadas
    for parte in valor.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if parte in opcoes:
            marcadas.add(parte)
        else:
            marcadas.add(codificacao.get(parte.casefold(), OUTRA))
    return marcadas


@dataclass
class DadosPreparados:
    todas: pd.DataFrame          # uma linha por resposta recebida, com status e motivo
    validas: pd.DataFrame        # só as válidas, com variáveis derivadas
    colunas_ausentes: list[str]
    categorias_p4: list[str]
    categorias_p5: list[str]


def preparar(bruto: pd.DataFrame, codificacao: dict | None = None) -> DadosPreparados:
    codificacao = codificacao or {}
    cod_p4 = {k.casefold(): v for k, v in codificacao.get("P4", {}).items()}
    cod_p5 = {k.casefold(): v for k, v in codificacao.get("P5", {}).items()}

    mapa = localizar_colunas(bruto.columns)
    ausentes = [k for k in PADROES_COLUNAS if k not in mapa]
    criticas = {"C0", "T1", "U1", *PP_ITENS, "AT1", "P1"}
    if criticas & set(ausentes):
        raise ValueError(
            "O CSV não tem as colunas esperadas do formulário: "
            + ", ".join(sorted(criticas & set(ausentes)))
        )

    d = pd.DataFrame(index=bruto.index)
    for chave in PADROES_COLUNAS:
        d[chave] = bruto[mapa[chave]].astype(str).str.strip() if chave in mapa else ""

    out = pd.DataFrame({"id": np.arange(1, len(d) + 1)}, index=d.index)
    # CSVs trazem normalmente dd/mm/aaaa; XLSX lido como texto pode trazer ISO.
    # O modo mixed aceita ambos sem alterar o valor bruto no arquivo.
    out["carimbo"] = pd.to_datetime(d["carimbo"], format="mixed", dayfirst=True, errors="coerce")
    for item in ["U1", *PP_ITENS, "AT1"]:
        out[item] = _primeiro_digito(d[item])
    out["U2"] = pd.to_numeric(d["U2"].where(d["U2"].str.fullmatch(r"\d+"), None), errors="coerce")
    p1_ok = d["P1"].str.fullmatch(r"\d+")
    out["P1"] = pd.to_numeric(d["P1"].where(p1_ok, None), errors="coerce")
    for item in ["T2", "P2", "P3"]:
        out[item] = d[item].replace("", None)

    status, motivos = [], []
    for i in d.index:
        r = d.loc[i]
        m: list[str] = []
        # Encerramento do formulário (inelegíveis), Seção 3
        if not r["C0"].startswith("Sim"):
            m.append("C0: não consentiu ou tem menos de 18 anos")
        elif r["T1"] != "Sim":
            m.append("T1: não trabalha hoje com desenvolvimento no Brasil")
        elif out.at[i, "U1"] == 1:
            m.append("U1 = 1: não usou assistente de IA nos últimos 3 meses")
        if m:
            status.append("Inelegível")
            motivos.append("; ".join(m))
            continue
        # Descarte (regras definidas antes da coleta), Seção 3
        brancos = [k for k in OBRIGATORIOS if r[k] == ""]
        if brancos:
            m.append("Item obrigatório em branco: " + ", ".join(brancos))
        if r["P1"] != "" and not p1_ok[i]:
            # DECISÃO OPERACIONAL: P1 é resposta curta; valor não inteiro é tratado como inválido
            m.append("P1 não é um número inteiro de anos")
        at1 = out.at[i, "AT1"]
        if r["AT1"] != "" and at1 != 2:
            marcado = LIKERT.get(int(at1), r["AT1"]) if pd.notna(at1) else r["AT1"]
            m.append(f"AT1 diferente de 'Discordo' (marcou '{marcado}')")
        if m:
            status.append("Descartada")
            motivos.append("; ".join(m))
        else:
            status.append("Válida")
            motivos.append("")
    out["status"] = status
    out["motivo"] = motivos
    out["fora_janela"] = out["carimbo"].notna() & (
        (out["carimbo"] < JANELA_COLETA[0]) | (out["carimbo"] > JANELA_COLETA[1])
    )

    # Variáveis derivadas (só para válidas)
    v = out[out["status"] == "Válida"].copy()
    v["PP5r"] = 6 - v["PP5"]
    itens_r = ["PP1", "PP2", "PP3", "PP4", "PP5r"]
    v["PP_med"] = v[itens_r].median(axis=1).astype(int)
    v["classe_PP"] = pd.cut(v["PP_med"], bins=[0, 2, 3, 5], labels=CLASSES_PP)
    v["linha_reta"] = v[PP_ITENS].nunique(axis=1) == 1  # cinco itens PP iguais (antes de recodificar)
    v["faixa_P1"] = pd.Categorical(v["P1"].map(_faixa_p1), categories=ORDEM_FAIXAS, ordered=True)
    v["U1_rotulo"] = pd.Categorical(
        v["U1"].map(U1_ROTULOS), categories=list(U1_ROTULOS.values()), ordered=True
    )
    v["T2"] = pd.Categorical(v["T2"], categories=OPCOES_T2)
    v["P2"] = pd.Categorical(v["P2"], categories=OPCOES_P2, ordered=True)
    v["P3"] = pd.Categorical(v["P3"], categories=OPCOES_P3, ordered=True)
    # Porte como ordinal: "Não se aplica" é tratado como ausente (Seção 3)
    v["P2_ord"] = v["P2"].map({o: i + 1 for i, o in enumerate(OPCOES_P2[:-1])}).astype(float)

    p4 = d.loc[v.index, "P4"].map(lambda x: _multipla(x, OPCOES_P4, cod_p4))
    p5 = d.loc[v.index, "P5"].map(lambda x: _multipla(x, OPCOES_P5, cod_p5))
    cat_p4 = _ordenar_categorias(p4, OPCOES_P4)
    cat_p5 = _ordenar_categorias(p5, OPCOES_P5)
    for c in cat_p4:
        v[f"P4::{c}"] = p4.map(lambda s, c=c: c in s)
    for c in cat_p5:
        v[f"P5::{c}"] = p5.map(lambda s, c=c: c in s)

    return DadosPreparados(out, v, ausentes, cat_p4, cat_p5)


def _ordenar_categorias(series: pd.Series, opcoes: list[str]) -> list[str]:
    todas = set().union(*series.tolist()) if len(series) else set()
    extras = sorted(c for c in todas if c not in opcoes and c != OUTRA)
    return [*opcoes, *extras, *([OUTRA] if OUTRA in todas else [])]


# --------------------------------------------------------------------------
# Estatística descritiva
# --------------------------------------------------------------------------
def resumo_ordinal(s: pd.Series) -> dict:
    s = pd.to_numeric(s, errors="coerce").dropna()
    if s.empty:
        return {"n": 0, "Mediana": np.nan, "Q1": np.nan, "Q3": np.nan}
    return {"n": len(s), "Mediana": s.median(), "Q1": s.quantile(0.25), "Q3": s.quantile(0.75)}


def resumo_razao(s: pd.Series) -> dict:
    s = pd.to_numeric(s, errors="coerce").dropna()
    base = resumo_ordinal(s)
    base.update(
        {
            "Média": s.mean() if len(s) else np.nan,
            "DP": s.std(ddof=1) if len(s) > 1 else np.nan,
            "Mín": s.min() if len(s) else np.nan,
            "Máx": s.max() if len(s) else np.nan,
        }
    )
    return base


def margem_erro(p: float, n: int) -> float:
    """Fórmula do enunciado: e = 1,96 × √(p(1 − p)/n)."""
    if n <= 0 or pd.isna(p):
        return np.nan
    return Z95 * np.sqrt(p * (1 - p) / n)


# --------------------------------------------------------------------------
# Testes confirmatórios
# --------------------------------------------------------------------------
@dataclass
class Resultado:
    rq: str
    pergunta: str
    teste: str
    n: int
    estatistica_nome: str
    estatistica: float
    p: float
    efeito_nome: str
    efeito: float
    ic: tuple[float, float]
    ic_metodo: str
    margem: float
    margem_texto: str
    leitura_efeito: str = ""
    p_holm: float = np.nan
    rejeita: bool = False
    notas: list[str] = field(default_factory=list)


def teste_rq1(v: pd.DataFrame) -> Resultado:
    pm = v["PP_med"]
    acima, abaixo, empates = int((pm >= 4).sum()), int((pm <= 2).sum()), int((pm == 3).sum())
    n_eff = acima + abaixo
    notas = [
        f"n válido = {len(v)}; empates em PP_med = 3 fora do teste: {empates}; n efetivo = {n_eff}.",
        f"Proporção com PP_med ≥ 4 entre todos os válidos: {_pct(acima / len(v)) if len(v) else '–'}; "
        f"com PP_med ≤ 2: {_pct(abaixo / len(v)) if len(v) else '–'}.",
    ]
    if n_eff == 0:
        return Resultado("RQ1", "PP_med difere do neutro (3)?", "Teste do sinal exato (binomial, p = 0,5)",
                         0, "k (acima do neutro)", np.nan, np.nan, "Proporção ≥ 4 (sem empates)", np.nan,
                         (np.nan, np.nan), "Clopper-Pearson 95%", np.nan, "", notas=notas + ["Sem casos fora do neutro."])
    res = stats.binomtest(acima, n_eff, 0.5, alternative="two-sided")
    ic = res.proportion_ci(confidence_level=0.95, method="exact")
    prop = acima / n_eff
    margem = margem_erro(prop, n_eff)
    pior = margem_erro(0.5, n_eff)
    texto = f"± {_pp(margem)} com p observado ({_pct(prop)}, n = {n_eff}); pior caso p = 0,5: ± {_pp(pior)}"
    if prop in (0.0, 1.0):
        notas.append("Com proporção observada de 0% ou 100% a fórmula do enunciado dá margem zero; "
                     "use o pior caso e o IC de Clopper-Pearson como referência de precisão.")
    return Resultado("RQ1", "A produtividade percebida difere do ponto neutro da escala?",
                     "Teste do sinal exato (binomial, p = 0,5 sob H0), bicaudal",
                     n_eff, "k (acima do neutro)", float(acima), float(res.pvalue),
                     "Proporção de PP_med ≥ 4 entre não empatados", prop,
                     (float(ic.low), float(ic.high)), "Clopper-Pearson 95%", margem, texto, notas=notas)


def _rank_pearson_linhas(rx: np.ndarray, ry: np.ndarray) -> np.ndarray:
    """Correlação de Pearson linha a linha entre matrizes de postos (B × n)."""
    rx = rx - rx.mean(axis=1, keepdims=True)
    ry = ry - ry.mean(axis=1, keepdims=True)
    num = (rx * ry).sum(axis=1)
    den = np.sqrt((rx**2).sum(axis=1) * (ry**2).sum(axis=1))
    with np.errstate(invalid="ignore", divide="ignore"):
        return num / den


def spearman_completo(x, y, semente: int = SEMENTE) -> dict:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    n = len(x)
    vazio = {"n": n, "rho": np.nan, "p_t": np.nan, "p_perm": np.nan, "ic": (np.nan, np.nan), "motivo": ""}
    if n < 3:
        return vazio | {"motivo": "menos de 3 observações"}
    if np.unique(x).size < 2 or np.unique(y).size < 2:
        return vazio | {"motivo": "uma das variáveis é constante no conjunto filtrado"}
    rho, p_t = stats.spearmanr(x, y)  # postos médios nos empates; p pela aproximação t
    rng = np.random.default_rng(semente)
    rx, ry = stats.rankdata(x), stats.rankdata(y)
    perm = rng.permuted(np.tile(ry, (N_PERMUTACOES, 1)), axis=1)
    r_perm = _rank_pearson_linhas(np.tile(rx, (N_PERMUTACOES, 1)), perm)
    p_perm = (np.sum(np.abs(r_perm) >= abs(rho) - 1e-12) + 1) / (N_PERMUTACOES + 1)
    idx = rng.integers(0, n, size=(N_BOOTSTRAP, n))
    bx = stats.rankdata(x[idx], axis=1)
    by = stats.rankdata(y[idx], axis=1)
    r_boot = _rank_pearson_linhas(bx, by)
    r_boot = r_boot[~np.isnan(r_boot)]
    ic = (float(np.percentile(r_boot, 2.5)), float(np.percentile(r_boot, 97.5))) if r_boot.size else (np.nan, np.nan)
    return {"n": n, "rho": float(rho), "p_t": float(p_t), "p_perm": float(p_perm), "ic": ic, "motivo": ""}


def leitura_cohen(rho: float) -> str:
    if pd.isna(rho):
        return "não calculável"
    a = abs(rho)
    if a < 0.1:
        return "desprezível"
    if a < 0.3:
        return "pequeno"
    if a < 0.5:
        return "médio"
    return "grande"


def _teste_spearman(rq: str, pergunta: str, v: pd.DataFrame, col_x: str, nome_x: str) -> Resultado:
    s = spearman_completo(v[col_x], v["PP_med"])
    notas = [f"Valor p por permutação ({milhar(N_PERMUTACOES)} permutações, semente {SEMENTE}): "
             f"{fmt_p(s['p_perm'])}."]
    if s["motivo"]:
        notas.append(f"Não calculável: {s['motivo']}.")
    margem = margem_erro(0.5, s["n"])
    return Resultado(rq, pergunta, f"Correlação de Spearman ({nome_x} × PP_med), postos médios, bicaudal",
                     s["n"], "ρ de Spearman", s["rho"], s["p_t"], "ρ de Spearman", s["rho"], s["ic"],
                     f"bootstrap percentil 95% ({milhar(N_BOOTSTRAP)} reamostras)",
                     margem, f"± {_pp(margem)} (margem geral da amostra, p = 0,5, n = {s['n']})",
                     leitura_cohen(s["rho"]), notas=notas)


def teste_rq2(v: pd.DataFrame) -> Resultado:
    return _teste_spearman("RQ2", "A frequência de uso (U1) está associada à produtividade percebida?", v, "U1", "U1")


def teste_rq3(v: pd.DataFrame) -> Resultado:
    return _teste_spearman("RQ3", "O tempo de experiência (P1) está associado à produtividade percebida?", v, "P1", "P1")


def holm(resultados: list[Resultado], alpha: float = ALPHA) -> list[Resultado]:
    """Correção de Holm na família de 3 testes. p não calculável conta como 1."""
    m = len(resultados)
    ps = np.array([1.0 if pd.isna(r.p) else r.p for r in resultados])
    ordem = np.argsort(ps)
    ajust = np.empty(m)
    acumulado = 0.0
    parou = False
    for posicao, i in enumerate(ordem):
        acumulado = max(acumulado, min(1.0, (m - posicao) * ps[i]))
        ajust[i] = acumulado
        if not parou and ps[i] <= alpha / (m - posicao):
            resultados[i].rejeita = True
        else:
            parou = True
            resultados[i].rejeita = False
    for r, pa in zip(resultados, ajust):
        r.p_holm = np.nan if pd.isna(r.p) else float(pa)
    return resultados


def testes_confirmatorios(v: pd.DataFrame) -> list[Resultado]:
    return holm([teste_rq1(v), teste_rq2(v), teste_rq3(v)])


# --------------------------------------------------------------------------
# Confiabilidade
# --------------------------------------------------------------------------
def _alfa(m: np.ndarray) -> float:
    k = m.shape[-1]
    var_itens = m.var(axis=-2, ddof=1).sum(axis=-1)
    var_total = m.sum(axis=-1).var(axis=-1, ddof=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return k / (k - 1) * (1 - var_itens / var_total)


def cronbach(v: pd.DataFrame, itens: list[str], semente: int = SEMENTE) -> dict:
    m = v[itens].to_numpy(dtype=float)
    n, k = m.shape
    if n < 3:
        return {"n": n, "k": k, "alfa": np.nan, "ic": (np.nan, np.nan), "itens": pd.DataFrame(),
                "motivo": "menos de 3 respostas válidas"}
    alfa = float(_alfa(m))
    rng = np.random.default_rng(semente)
    boot = _alfa(m[rng.integers(0, n, size=(N_BOOTSTRAP, n))])
    boot = boot[np.isfinite(boot)]
    ic = (float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))) if boot.size else (np.nan, np.nan)
    linhas = []
    for j, item in enumerate(itens):
        resto = np.delete(m, j, axis=1)
        total_resto = resto.sum(axis=1)
        if np.std(m[:, j]) > 0 and np.std(total_resto) > 0:
            r_it = float(np.corrcoef(m[:, j], total_resto)[0, 1])
        else:
            r_it = np.nan
        linhas.append({"Item": item, "Correlação item-total corrigida": r_it,
                       "Alfa se o item for removido": float(_alfa(resto))})
    motivo = "" if np.isfinite(alfa) else "variância total zero (todos responderam igual)"
    return {"n": n, "k": k, "alfa": alfa, "ic": ic, "itens": pd.DataFrame(linhas), "motivo": motivo}


# --------------------------------------------------------------------------
# Análises exploratórias (fora da família, sem correção)
# --------------------------------------------------------------------------
def agrupar_faixas(contagens: pd.Series) -> dict[str, str]:
    """Agrupa faixas de P1 com menos de 5 pessoas com a vizinha (Seção 1, RQ3)."""
    grupos = [[(lo, hi)] for lo, hi in FAIXAS_P1]
    cont = [int(contagens.get(rotulo_faixa(lo, hi), 0)) for lo, hi in FAIXAS_P1]
    # remove faixas vazias nas pontas não altera o agrupamento; vazias no meio são absorvidas
    while len(grupos) > 1 and min(cont) < MIN_SEGMENTO:
        i = int(np.argmin(cont))
        if i == 0:
            j = 1
        elif i == len(grupos) - 1:
            j = i - 1
        else:
            j = i - 1 if cont[i - 1] <= cont[i + 1] else i + 1
        a, b = sorted((i, j))
        grupos[a] = grupos[a] + grupos[b]
        cont[a] = cont[a] + cont[b]
        del grupos[b], cont[b]
    mapa = {}
    for g in grupos:
        rot = rotulo_faixa(g[0][0], g[-1][1])
        for lo, hi in g:
            mapa[rotulo_faixa(lo, hi)] = rot
    return mapa


def comparar_grupos(v: pd.DataFrame, col_grupo: str, col_y: str = "PP_med") -> dict:
    """Mann-Whitney (2 grupos) ou Kruskal-Wallis (3+), só com grupos de ≥ 5 pessoas."""
    dados = v[[col_grupo, col_y]].dropna()
    tamanhos = dados.groupby(col_grupo, observed=True).size()
    usados = tamanhos[tamanhos >= MIN_SEGMENTO].index.tolist()
    excluidos = tamanhos[tamanhos < MIN_SEGMENTO].index.tolist()
    grupos = [dados.loc[dados[col_grupo] == g, col_y].to_numpy() for g in usados]
    base = {"usados": usados, "excluidos": excluidos, "tamanhos": tamanhos}
    if len(grupos) < 2:
        return base | {"teste": None, "motivo": "menos de 2 grupos com 5 ou mais pessoas"}
    n = sum(len(g) for g in grupos)
    try:
        if len(grupos) == 2:
            u, p = stats.mannwhitneyu(grupos[0], grupos[1], alternative="two-sided")
            r_rb = 2 * u / (len(grupos[0]) * len(grupos[1])) - 1
            return base | {"teste": "Mann-Whitney U", "estatistica": float(u), "p": float(p),
                           "efeito_nome": f"correlação rank-biserial ({usados[0]} vs {usados[1]})",
                           "efeito": float(r_rb), "n": n, "motivo": ""}
        h, p = stats.kruskal(*grupos)
        return base | {"teste": "Kruskal-Wallis H", "estatistica": float(h), "p": float(p),
                       "efeito_nome": "ε² = H / (n − 1)", "efeito": float(h / (n - 1)), "n": n, "motivo": ""}
    except ValueError as exc:  # todos os valores iguais
        return base | {"teste": None, "motivo": f"teste não calculável ({exc})"}


def qui_quadrado(v: pd.DataFrame, col_grupo: str) -> dict:
    dados = v[[col_grupo, "classe_PP"]].dropna()
    tamanhos = dados.groupby(col_grupo, observed=True).size()
    usados = tamanhos[tamanhos >= MIN_SEGMENTO].index.tolist()
    dados = dados[dados[col_grupo].isin(usados)]
    tab = pd.crosstab(dados[col_grupo], dados["classe_PP"])
    tab = tab.loc[:, tab.sum() > 0]
    if tab.shape[0] < 2 or tab.shape[1] < 2:
        return {"tabela": tab, "motivo": "tabela com menos de 2 linhas ou colunas"}
    chi2, p, gl, esperado = stats.chi2_contingency(tab)
    n = tab.to_numpy().sum()
    v_cramer = np.sqrt(chi2 / (n * (min(tab.shape) - 1)))
    return {"tabela": tab, "chi2": float(chi2), "p": float(p), "gl": int(gl), "v": float(v_cramer),
            "esperado_baixo": bool((esperado < 5).any()), "motivo": ""}


# --------------------------------------------------------------------------
# Formatação (pt-BR)
# --------------------------------------------------------------------------
def fmt(x, casas: int = 3) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "–"
    return f"{x:.{casas}f}".replace(".", ",")


def fmt_p(p) -> str:
    if p is None or pd.isna(p):
        return "–"
    return "< 0,001" if p < 0.001 else fmt(p, 3)


def _pct(x: float) -> str:
    return "–" if pd.isna(x) else f"{x * 100:.1f}%".replace(".", ",")


def _pp(x: float) -> str:
    return "–" if pd.isna(x) else f"{x * 100:.1f}".replace(".", ",") + " p.p."


def milhar(n: int) -> str:
    return f"{n:,}".replace(",", ".")


pct = _pct
pp = _pp
