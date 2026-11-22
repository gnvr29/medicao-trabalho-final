# Protocolo do Survey: assistentes de IA e produtividade percebida

**Disciplina:** Medição e Experimentação em Engenharia de Software (PUC Minas) · **Integrantes:** [5 nomes] · **Data de entrega:** [data]

---

## 1. Objetivo e questões de pesquisa

**Objetivo (GQM, template de cinco campos, Aula 2).** Analisar o **uso de assistentes de IA generativa em atividades de desenvolvimento de software**, com o propósito de **caracterizar**, com respeito à **produtividade percebida (seu nível, sua relação com a frequência de uso e sua variação segundo o tempo de experiência)**, do ponto de vista dos **desenvolvedores**, no contexto de **pessoas que trabalham atualmente com desenvolvimento de software no Brasil, em emprego, estágio ou trabalho autônomo, e que usam assistentes de IA generativa**.

**Escopo.** O estudo mede percepção por autorrelato, não produtividade objetiva. As conclusões tratam de produtividade percebida e de associação, nunca de causalidade. Quem não usa assistentes de IA não entra: o formulário é encerrado para essas pessoas, e o mínimo de respostas válidas do enunciado é contado só entre usuários.

**Definições operacionais.**
- **Assistente de IA generativa:** ferramenta de IA generativa usada no trabalho de desenvolvimento para escrever, completar, explicar, revisar, testar ou depurar código. Autocomplete tradicional, linters e busca em documentação não contam.
- **Usuário:** desenvolvedor que usou assistente de IA no trabalho ao menos uma vez nos últimos 3 meses (U1 nos níveis 2 a 5; o nível 1 é "nunca usou").
- **Produtividade percebida (PP):** autoavaliação sobre rapidez, qualidade e esforço ao usar assistentes de IA, medida por cinco itens Likert de 5 pontos (PP1 a PP5, com o item de esforço invertido e recodificado) e resumida pela mediana dos itens (PP_med). Os itens são obrigatórios, então PP_med é sempre um inteiro de 1 a 5, e 3 é o ponto neutro.
- **Tempo de experiência:** anos completos de atuação profissional em desenvolvimento.
- **Frequência de uso:** frequência de uso de assistentes de IA nos últimos 3 meses, em escala ordinal de 5 níveis.

**RQ1. A produtividade percebida dos usuários de assistentes de IA generativa difere do ponto neutro da escala?**
- **Entidade e atributo:** Recurso, atributo externo *Produtividade*, medido por percepção.
- **Métricas:** PP_med (itens PP1 a PP5, ordinal, derivada); proporção de usuários com PP_med ≥ 4, o mesmo que acima do neutro (derivada, usada na margem de erro); proporção com PP_med ≤ 2 (derivada).
- **Hipóteses (teste do sinal, bicaudal):** H0: a probabilidade de PP_med ficar acima do neutro é igual à de ficar abaixo. H1: as probabilidades são diferentes. Usuários com PP_med = 3 ficam fora do teste, e o n efetivo e o número de empates são relatados.

**RQ2. A frequência de uso de assistentes de IA generativa está associada à produtividade percebida dos desenvolvedores?**
- **Entidades e atributos:** Processo, a prática de uso de assistentes de IA, atributo *Frequência de uso*, por autorrelato (proxy do uso real); Recurso, atributo externo *Produtividade*, por percepção.
- **Métricas:** U1, frequência nos últimos 3 meses (ordinal, níveis 2 a 5 entre usuários); PP_med; U2, dias de uso nos últimos 5 dias úteis, contagem de 0 a 5 (razão), só para robustez.
- **Hipóteses:** H0: a correlação de Spearman entre frequência de uso e produtividade percebida é zero na população. H1: é diferente de zero.
- **Observação:** é associação, não efeito. O desenho é transversal, e quem percebe mais ganho pode passar a usar mais.

**RQ3. A produtividade percebida está associada ao tempo de experiência do desenvolvedor?**
- **Entidades e atributos:** Recurso, atributo interno *Nível de experiência*; Recurso, atributo externo *Produtividade*, por percepção.
- **Métricas:** P1, anos completos de atuação (razão); PP_med; faixas de P1 (0 a 2, 3 a 5, 6 a 10, 11 ou mais; ordinal, derivada), usadas só na análise exploratória, e faixas com menos de 5 pessoas são agrupadas com a vizinha.
- **Hipóteses (confirmatórias):** H0: a correlação de Spearman entre anos de experiência e produtividade percebida é zero na população. H1: é diferente de zero.

**Observações.** As hipóteses e os testes (Seção 5) são fixados antes da coleta e só mudam como desvio declarado. O sentido é bicaudal porque as questões não indicam direção. Mede-se percepção e não produtividade objetiva (linhas de código, pull requests por pessoa-mês) porque essas métricas ficam distorcidas quando parte do código é gerada por IA. Porte da organização, tempo de uso de IA, ferramentas e tarefas são itens de perfil, usados como possíveis confundidores e filtros do dashboard, e não respondem a nenhuma RQ.

---

## 2. População e amostragem

**População-alvo.** Desenvolvedores que trabalham atualmente com desenvolvimento no Brasil (emprego, estágio ou trabalho autônomo) e que usaram assistente de IA generativa nos últimos 3 meses.
- **Entram:** maiores de 18 anos, com atuação atual em desenvolvimento no Brasil, que usaram assistente de IA no período e consentiram.
- **Não entram:** quem não atua em desenvolvimento (incluindo estudantes sem estágio ou trabalho na área), quem não usou IA no período, quem não consentiu ou tem menos de 18 anos e os **colegas da turma**. O enunciado só aceita colegas quando a população-alvo é de estudantes, o que não é o caso. A divulgação não usa canais da turma.

**Origem dos contatos.** Cerca de 30 contatos diretos (5 integrantes, 6 a 7 cada) e divulgação aberta em redes profissionais e comunidades de desenvolvedores, de onde vem a maior parte do volume (canais na Seção 8).

**Estratégia de amostragem.** Não probabilística, por **conveniência com bola de neve** (divulgação aberta e pedido de repasse a colegas de trabalho). Não existe quadro amostral de todos os desenvolvedores do Brasil. Há risco de autosseleção e de viés de rede, então a margem de erro é só referência de precisão e as conclusões ficam limitadas à amostra.

**Tamanho pretendido e margem de erro.** Pretendem-se **50 respostas válidas** de usuários, ou seja, 10 por integrante (mínimo do enunciado; a carta de anuência não será usada, pois o survey não é em uma única organização). Estimando descartar cerca de 15%, buscam-se ao menos 60 respostas de elegíveis, cerca de 12 por integrante. A coleta termina ao fim dos 5 dias, e todas as válidas entram na análise.

Pela fórmula do enunciado, `e = 1,96 × √( p(1 − p) / n )`, com p = 0,5 (pior caso):

| Situação | n | Margem (± p.p.) |
|---|---|---|
| Pretendido | 50 | 13,9 |
| Teste do sinal da RQ1, se 20% empatarem em PP_med = 3 | 40 | 15,5 |
| Subgrupo, por exemplo uma faixa de experiência | 20 | 21,9 |

Na RQ1 usa-se a proporção observada de PP_med ≥ 4. Para as RQ2 e RQ3, relatam-se a margem geral da amostra e o intervalo de confiança de ρ. Com n = 50, o Spearman detecta com 80% de poder |ρ| a partir de cerca de 0,39.

---

## 3. Questionário com rastreabilidade

**Fluxo.** Termo de consentimento → texto com a definição de assistente de IA (incluindo o que não conta) → triagem (T1, T2, U1) → uso (U2) → perfil (P1 a P5) → produtividade percebida (PP1 a PP5 com a pergunta de atenção AT1 na mesma matriz). Cerca de 5 minutos.

**Encerramento e descarte (definidos antes da coleta).** O formulário **encerra** se C0 = não, T1 = não ou U1 = nível 1, e essas pessoas entram no funil como inelegíveis. A resposta é **descartada**, com o motivo registrado, se AT1 for diferente de "Discordo" ou se algum item obrigatório ficar em branco. Cinco itens PP iguais (linha reta) não descartam: são sinalizados e testados em sensibilidade.

**Construto.** Só a produtividade percebida usa mais de um item (cinco: rapidez PP1 e PP2, qualidade PP3 e PP4, esforço PP5). A confiabilidade é medida pelo alfa de Cronbach, com PP5 recodificado (6 − x) e lembrando que os itens são ordinais. U1 e U2 não formam construto: U1 é a métrica da RQ2 e U2 é checagem de robustez.

| RQ | Métricas | Itens |
|---|---|---|
| RQ1 | PP_med; proporção ≥ 4; proporção ≤ 2 | PP1 a PP5 |
| RQ2 | U1; PP_med; U2 (robustez) | U1, U2, PP1 a PP5 |
| RQ3 | P1; PP_med; faixas de P1 (exploratória) | P1, PP1 a PP5 |

Escala dos itens PP: Likert de 5 pontos (1 = Discordo totalmente, 3 = Nem concordo nem discordo, 5 = Concordo totalmente), ordinal.

| ID | Item | RQ | Métrica | Escala |
|---|---|---|---|---|
| C0 | Tenho 18 anos ou mais, li o termo e aceito participar (sim/não) | Filtro | Elegibilidade | Nominal |
| T1 | Hoje trabalha com desenvolvimento de software no Brasil? (sim/não) | Filtro | Elegibilidade | Nominal |
| T2 | Vínculo: emprego, estágio, autônomo ou outro | Apoio | Perfil | Nominal |
| U1 | Nos últimos 3 meses, com que frequência usou assistentes de IA no trabalho de desenvolvimento? 1 Nunca; 2 Uma ou poucas vezes no período; 3 Algumas vezes por mês; 4 Algumas vezes por semana; 5 Todos ou quase todos os dias | RQ2 | Frequência de uso | Ordinal |
| U2 | Em quantos dos últimos 5 dias úteis usou assistentes de IA? (0 a 5) | RQ2 (robustez) | Dias de uso | Razão (contagem) |
| P1 | Anos completos de atuação profissional em desenvolvimento (inteiro; 0 = menos de 1 ano) | RQ3 | Anos de experiência | Razão |
| P2 | Porte da organização: até 10, 11 a 50, 51 a 200, 201 a 1000, mais de 1000 pessoas, ou "não se aplica (autônomo)" (tratado como ausente no porte) | Apoio | Porte | Ordinal |
| P3 | Há quanto tempo usa assistentes de IA no trabalho? Menos de 3 meses, 3 a 6, 6 a 12, mais de 12 meses | Apoio | Tempo de uso de IA | Ordinal |
| P4 | Quais assistentes usa? (múltipla escolha, com "Outra") | Apoio | Ferramentas | Nominal |
| P5 | Em quais tarefas usa? Escrever, completar, explicar, revisar, testar, depurar ou planejar/projetar código (múltipla escolha, com "Outra") | Apoio | Tarefas | Nominal |
| PP1 | Com assistentes de IA, concluo minhas tarefas de desenvolvimento mais rápido | RQ1, 2, 3 | PP_med (rapidez) | Ordinal |
| PP2 | Com assistentes de IA, consigo entregar mais tarefas no mesmo período | RQ1, 2, 3 | PP_med (rapidez) | Ordinal |
| PP3 | Com assistentes de IA, a qualidade do código que entrego é melhor | RQ1, 2, 3 | PP_med (qualidade) | Ordinal |
| PP4 | Com assistentes de IA, preciso refazer menos o meu código depois de entregue | RQ1, 2, 3 | PP_med (qualidade) | Ordinal |
| PP5 (invertido) | Usar assistentes de IA torna meu trabalho de desenvolvimento **mais cansativo ou trabalhoso** (recodificado 6 − x) | RQ1, 2, 3 | PP_med (esforço) | Ordinal |
| AT1 | Pergunta de atenção na matriz PP: "Para mostrar que está lendo com atenção, marque 'Discordo' nesta linha" | Qualidade | Conformidade | Nominal |

Itens de triagem, perfil e controle (C0, T1, T2, P2 a P5) ligam-se às RQs como filtro ou possível confundidor. Não há perguntas abertas obrigatórias, e as respostas "Outra" são codificadas na Seção 5.

---

## 4. Pré-teste

**Método.** O formulário final será aplicado a 3 a 5 desenvolvedores que usam IA, de perfis diferentes (por exemplo estagiário, júnior e sênior), que não participam da coleta. Medem-se o tempo de resposta e, em conversa curta, a clareza dos itens PP, o entendimento da definição de assistente de IA, as opções de U1, o encerramento da triagem e a pergunta de atenção. O pré-teste usa uma cópia idêntica do formulário, com planilha própria e uma página extra de feedback, então suas respostas nunca se misturam com as da coleta.

**Instrumento do pré-teste.** Google Formulários (versão PRÉ-TESTE): https://docs.google.com/forms/d/e/1FAIpQLSfvfqzhbticuoK79xMvUB6wbzkhEcYWZj-Dq9JeX2it9uDXFA/viewform

**Resultado.** Aplicado em 06 e 07/11/2026. Foram 5 respostas: 1 pessoa respondeu T1 = não e o formulário encerrou como previsto, e 4 eram elegíveis. O tempo autorrelatado (F1) foi de 3, 5, 5 e 3 minutos, com média de 4 minutos, compatível com os "cerca de 5 minutos" do termo. Os 4 elegíveis acharam a definição de assistente de IA clara (F2), não apontaram item difícil (F3) nem opção faltando (F4), acertaram a pergunta de atenção (AT1) e nenhum respondeu em linha reta.

| Item ou aspecto | Problema observado | Mudança feita |
|---|---|---|
| P5 (tarefas) | Um respondente escreveu "Planejar código" em "Outra", tarefa que não estava na lista | Inclusão da opção "Planejar ou projetar código" |
| P4 (ferramentas) | Um respondente citou em "Outra" uma ferramenta fora da lista | Mantido o "Outra", codificado conforme a Seção 5 |
| PP5 (invertido) | Um respondente concordou com rapidez (PP1 = 4, PP2 = 5) e concordou totalmente que a IA deixa o trabalho mais cansativo (PP5 = 5). Pode ser leitura errada do item invertido | Destaque em negrito de "**mais cansativo ou trabalhoso**" no enunciado de PP5. O item continua invertido, por controlar aquiescência |
| Triagem, AT1, tempo, definição de IA | Funcionaram como previsto | Nenhuma |
| Perfil dos participantes | Os 4 elegíveis eram estagiários, e não houve perfis júnior e sênior como planejado | Limitação declarada: o pré-teste não verificou a compreensão por profissionais mais experientes |

As mudanças foram aplicadas ao formulário de coleta antes da sua abertura. As respostas do pré-teste não entram na análise, e o alfa de Cronbach não foi calculado com n = 4.

---

## 5. Plano de análise

**Preparação.** A exportação bruta (com data e hora) fica intacta e a análise usa uma cópia. Aplicam-se as regras da Seção 3, registrando o motivo de cada exclusão (funil: recebidas, inelegíveis, descartadas, válidas). Recodifica-se PP5, calculam-se PP_med e as faixas de P1. Os itens PP são obrigatórios, então não há imputação.

**Estatística descritiva, por escala.**

| Escala | Itens | Resumo |
|---|---|---|
| Nominal | C0, T1, T2, P4, P5, AT1 | Frequência e percentual, moda. Em P4 e P5, percentual de respondentes por opção |
| Ordinal | U1, P2, P3, PP1 a PP5, PP_med | Distribuição, mediana e quartis, com Likert em barras divergentes. **Sem média** |
| Razão | P1, U2 | Mediana, quartis, média, desvio padrão, mínimo e máximo |
| Construto PP | PP1 a PP5 | Alfa de Cronbach (com k e n), após recodificar PP5 |

**Testes confirmatórios (bicaudais, α = 0,05).** As variáveis de resposta são ordinais, então valem mediana e Spearman. Média, teste t e Pearson não valem nessa escala.

| RQ | Variáveis | Teste | Efeito e margem |
|---|---|---|---|
| RQ1 | PP_med contra o neutro 3 | Teste do sinal exato (binomial, p = 0,5 sob H0), sem os empates | Proporção de PP_med ≥ 4 entre os não empatados, com IC de 95% de Clopper-Pearson. Margem de erro pela fórmula do enunciado |
| RQ2 | U1 × PP_med | Spearman, com postos médios nos empates. Valor p pela aproximação t, conferido por permutação | ρ, com IC de 95% por bootstrap |
| RQ3 | P1 × PP_med | Spearman, como na RQ2 | ρ, com IC de 95% por bootstrap |

**Tamanho de efeito.** Relatado junto ao valor p. A leitura de ρ é declarada antes dos dados (convenção de Cohen): abaixo de 0,1 desprezível, 0,1 a 0,3 pequeno, 0,3 a 0,5 médio, a partir de 0,5 grande. Com n próximo de 50, um ρ moderado com p alto indica pouco poder, e o texto diz "não rejeitamos H0", nunca "aceitamos H0".

**Múltiplas comparações.** A família confirmatória tem 3 testes, com correção de Holm (menor p contra α/3, o seguinte contra α/2, o último contra α, parando na primeira não rejeição). Relatam-se o p bruto e o ajustado.

**Exploratórias (fora da família, sem correção, nunca usadas para concluir).** Kruskal-Wallis da PP_med entre as faixas de experiência (efeito ε²); Spearman entre U2 e PP_med; sensibilidade sem respostas em linha reta; comparações entre segmentos do dashboard (Mann-Whitney para 2 grupos, Kruskal-Wallis para 3 ou mais, χ² em variáveis nominais), sem comparar segmentos com menos de 5 pessoas.

**Respostas abertas (opção "Outra" de P4 e P5).** Duas pessoas leem de forma independente e agrupam em categorias, reclassificando em opções existentes quando couber e criando categorias nominais para o resto. Divergências são resolvidas em conversa. Relatam-se só frequências.

**Relato.** Para cada RQ: teste, estatística, valor p (bruto e ajustado), efeito com intervalo, margem de erro, n e interpretação em termos de produtividade **percebida** e associação.

---

## 6. Ética e LGPD

- **Termo de consentimento.** É a primeira página, e o aceite (C0) é obrigatório antes de qualquer pergunta. Informa objetivo (atividade acadêmica), participação voluntária, duração de cerca de 5 minutos, exigência de 18 anos ou mais, dados coletados (respostas, data e hora), quem acessa (integrantes do grupo e professor) e contato do grupo. Informa também que, sem identificação, não é possível retirar a resposta depois do envio, mas quem desistir pode fechar o formulário antes de enviar, sem consequência.
- **Anonimização.** Não se coletam nome, e-mail, CPF, telefone, IP nem nome da empresa, e o formulário não exige login. O perfil é coletado em categorias, para reduzir risco de identificação por combinação de respostas. Em "Outra", pede-se para não citar nomes, e identificadores que aparecerem são removidos antes da análise. Dashboard e apresentação não exibem segmentos com menos de 5 pessoas. Não se coletam dados sensíveis nem de menores.
- **Armazenamento.** A exportação bruta fica em pasta de acesso restrito aos integrantes (e ao professor, se solicitado), com backup na mesma pasta. O dashboard lê uma cópia sem texto livre, e nenhuma evidência expõe dados pessoais. Os dados são mantidos até o fim da avaliação da disciplina e depois apagados. O grupo segue a LGPD (Lei 13.709/2018) e as orientações da instituição sobre pesquisas com pessoas.

---

## 7. Ameaças à validade

| Ameaça | Como aparece | Mitigação |
|---|---|---|
| Não resposta | Quem não responde pode ter menos interesse em IA ou tempo, e a divulgação aberta não permite taxa de resposta | Formulário curto, lembretes, relato do funil, taxa de resposta só nos contatos diretos, limitação declarada |
| Autosseleção e viés de rede | Quem tem opinião forte sobre IA tende a responder, e a bola de neve traz respondentes parecidos | Convite neutro (sem citar ganho de produtividade), vários canais e pontos de partida, relato do perfil, conclusões restritas à amostra |
| Desejabilidade social | Parecer moderno ou produtivo ao usar IA | Anonimato, linguagem neutra, itens sobre a prática, item de esforço invertido (PP5) |
| Respostas descuidadas ou automáticas | Marcação sem ler | AT1 com regra de descarte prévia, linhas retas em sensibilidade |
| Percepção diferente da realidade | O caso METR (Aula 2): desenvolvedores se percebiam mais rápidos e mediram mais lentos. Toda medida é um proxy (Goodhart) | Conclui-se só sobre produtividade **percebida**, sem afirmar ganho real |
| Causalidade reversa e confundidores | Estudo transversal: quem percebe ganho pode usar mais, e tempo de uso, porte e ferramentas podem confundir | Linguagem de associação, confundidores medidos e usados só na leitura descritiva |
| Medição | Mediana de 5 itens perde informação e gera empates. "IA" pode ser entendida de formas diferentes. Frequências dependem de memória | Itens cobrindo rapidez, qualidade e esforço, alfa, pré-teste, definição de IA exibida antes da triagem, janelas curtas e U2 como checagem de U1 |
| Validade estatística | Com n = 50, só ρ a partir de cerca de 0,39 é detectado com 80% de poder. Empates reduzem o n do teste do sinal. Há 3 testes | Relato do poder e do n efetivo, correção de Holm, subgrupos pequenos só descritivos |
| Validade externa | Amostra não probabilística, só no Brasil, coletada em 5 dias, com ferramentas que mudam rápido | Sem generalização, margem de erro como referência |

---

## 8. Plano de divulgação

**Período.** De segunda-feira, 09/11/2026, a sexta-feira, 13/11/2026 (5 dias úteis). A divulgação só começa depois do envio do protocolo (data da Parte 1), e o formulário fecha ao fim da sexta-feira. A meta do grupo é de 50 respostas válidas, 10 por integrante, e cada integrante divulga nas próprias redes.

**Instrumento e registro dos dados.** O questionário é um Google Formulários (versão COLETA), sem login e sem coleta de e-mail: https://docs.google.com/forms/d/e/1FAIpQLSd2wm9FwwFUBmADLLqTiH9ChwPw5o7NAsM57JEJdjPGntZCKA/viewform. O formulário foi construído e conferido antes da coleta e permanece **fechado para respostas** até o envio deste protocolo, para que nenhuma resposta anteceda a data de entrega. Ele é aberto na segunda-feira, 09/11/2026, e fechado ao fim da sexta-feira, 13/11/2026. Cada resposta é gravada automaticamente em uma planilha própria, com data e hora de envio (carimbo gerado pelo Google, que não é digitado por ninguém). Ao fim da coleta, a planilha é exportada em CSV, sem alteração, como dado bruto e evidência de data. O pré-teste usa formulário e planilha separados, então seus dados não entram na análise. Todos os integrantes divulgam o mesmo link, e a origem de cada resposta não é registrada, para preservar o anonimato.

**Canais.** Convite individual aos contatos diretos de cada integrante; publicação de cada integrante no LinkedIn com pedido de compartilhamento; grupos de WhatsApp, Telegram e Discord e fóruns de desenvolvedores, respeitando as regras de cada grupo; pedido de repasse a colegas de trabalho. Não se usam canais da turma.

**Convite.** Texto neutro: tema (uso de assistentes de IA no trabalho de desenvolvimento), tempo (cerca de 5 minutos), anonimato e quem pode responder. Não cita ganho de produtividade nem resultados esperados.

| Dia | Ação |
|---|---|
| 1 (seg, 09/11) | Convites individuais, publicações no LinkedIn e envio nas comunidades |
| 2 (ter, 10/11) | Lembrete aos contatos diretos e pedido de repasse |
| 3 (qua, 11/11) | Segundo reforço nas comunidades |
| 4 (qui, 12/11) | Conferência das respostas válidas por integrante e no total. Se o total estiver abaixo de 50, novo reforço em todos os canais |
| 5 (sex, 13/11) | Último lembrete, fechamento e exportação bruta com data e hora |

**Evidências.** Capturas datadas das publicações e dos envios, sem dados pessoais, e a exportação bruta com data e hora de cada resposta.

---

**Referências.** BASILI, V.; CALDIERA, G.; ROMBACH, H. D. The Goal Question Metric approach, 1994. COHEN, J. *Statistical Power Analysis for the Behavioral Sciences*, 1988. KITCHENHAM, B.; PFLEEGER, S. L. Personal opinion surveys, 2008. WOHLIN, C. et al. *Experimentation in Software Engineering*, 2012.
