# Calculo de métricas

Este projeto em Python realiza o cálculo de métricas educacionais a partir de dados extraídos da ferramenta Ralph, que coleta statements no formato xAPI.

## Métricas proposta por leitão (2017)

As métricas implementadas seguem as definições propostas por Leitão (2017) em sua pesquisa sobre análise de desempenho de estudantes com base em dados educacionais.

### Métrica de Pontuação:

- Essa é uma métrica clássica que calcula a média de pontuação obtida por um estudante em atividades avaliativas.

- Os statements utilizados para esse cálculo devem conter o verbo:
`http://adlnet.gov/expapi/verbs/completed`

Também é necessário verificar a existência dos campos `actor` e `result.score.raw` em cada *statement*, pois páginas apenas visualizadas/completadas por alunos podem conter o mesmo verbo, mas não possuem pontuação associada — e, portanto, não devem ser consideradas nessa métrica.

Veja um [exemplo completo de statement de pontuação](statements-exemplos/statement_pontuacao.json).

### Métrica de Nível de Confusão:

### Métrica de Tempo de Resposta:

 Essa métrica mede quanto tempo o estudante levou para concluir uma determinada atividade.

- Os statements utilizados para esse cálculo devem conter o verbo:
`http://adlnet.gov/expapi/verbs/completed`

- E, são utilizados *statements* que contenham os campos:
  - `result.duration` (tempo de realização da atividade).

- Também são extraídas informações complementares sobre:
  - **Matéria** (via `context.contextActivities.parent.definition.name.en`),
  - **Atividade** (via `object.definition.name.en`).

Os *statements* que contêm todos esses campos são considerados válidos para esta métrica.

O resultado gerado é um arquivo JSON com as seguintes informações por usuário:
- Nome do usuário,
- Tempo de resposta (no padrão ISO 8601, ex: `"PT1M30S"`),
- Timestamp,
- Matéria,
- Atividade.

Veja um [exemplo completo de statement de tempo de resposta](statements-exemplos/statement_tempo_resposta.json).

### Métrica de Nível de Desordem: 

### Métrica de Nível de Compreensão: