## Desvios em relação ao protocolo da Parte 1

Cada linha diz o que o protocolo previa, o que foi feito e por quê. O grupo atualiza esta tabela depois do fim da coleta (13/11/2026). As checagens automáticas acima desta seção são recalculadas a partir do CSV e mostram desvios que dependem dos dados (tamanho da amostra, faixas agrupadas, respostas fora da janela).

| # | Seção do protocolo | Previsto | Feito no dashboard | Motivo |
|---|---|---|---|---|
| D1 | 6 (Armazenamento) | "O dashboard lê uma cópia sem texto livre" | O dashboard lê a exportação CSV bruta do Google Formulários, sem alterar o arquivo. Na leitura, descarta em memória as colunas de texto livre e troca o texto de "Outra" em P4 e P5 pela categoria codificada (ou "Outra (não codificada)"). Nenhum texto livre é exibido | O enunciado da Parte 2 exige que o dashboard leia os dados brutos. A remoção do texto livre passa a ser feita na leitura, e o objetivo de proteção da Seção 6 se mantém |
| D2 | 5 (Respostas abertas) | Duas pessoas codificam "Outra" de P4 e P5 de forma independente | Pendente até o fim da coleta. O resultado da codificação entra em `dashboard/codificacao_outra.json`, e o dashboard aplica o mapeamento | A codificação depende das respostas, que só existem depois da coleta |
| D3 | 8 (Período) | Coleta de 09 a 13/11/2026 | O arquivo oficial contém 90 respostas entre 13/11/2026 20:46 e 19/11/2026 17:50; 89 delas ficaram depois do encerramento previsto em 13/11 | O cronograma efetivo foi deslocado. **Antes da apresentação, o grupo precisa registrar aqui o motivo factual do deslocamento** |

## Decisões operacionais (o protocolo não fixava estes detalhes)

Estas escolhas não mudam nenhuma hipótese, teste ou regra de descarte. Elas só deixam explícitos parâmetros que o protocolo não definiu.

- **Permutação (RQ2 e RQ3):** 10.000 permutações, semente fixa 20261109, valor p bicaudal com correção +1 no numerador e no denominador. O valor p confirmatório continua sendo o da aproximação t, como no protocolo. A permutação é a conferência.
- **Bootstrap:** 5.000 reamostras com reposição, intervalo percentil de 95%, mesma semente. Também é usado para dar um intervalo ao alfa de Cronbach, que o protocolo não pedia.
- **P1 não inteiro:** P1 é resposta curta. Um valor que não seja inteiro (por exemplo "dez") é tratado como item obrigatório inválido e a resposta é descartada, com o motivo registrado.
- **Margem de erro da RQ1:** calculada com a proporção observada de PP_med ≥ 4 entre os não empatados (n efetivo). Quando essa proporção é 0% ou 100%, a fórmula dá zero, então o dashboard mostra também o pior caso (p = 0,5).
- **Holm com p não calculável:** se um teste não puder ser calculado (variável constante), entra na correção com p = 1 e é relatado como "não calculável".
- **χ² entre segmentos:** cruza o segmento com a classe de PP_med (abaixo do neutro, neutro, acima do neutro), só com grupos de 5 ou mais pessoas. O dashboard avisa quando alguma frequência esperada fica abaixo de 5.
- **Filtros:** a resposta confirmatória de cada RQ é sempre calculada na amostra completa de válidas. Resultados com filtro aparecem separados e marcados como exploratórios. Com filtro ativo, segmentos com menos de 5 pessoas não são exibidos (Seção 6).
- **Respostas fora da janela de coleta (09 a 13/11/2026):** são sinalizadas e não descartadas, porque o protocolo não previa esse descarte.
