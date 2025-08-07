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

### Nível de Desordem:

- Essa métrica calcula a desordem das respostas finais de um estudante em uma atividade avaliativa, com base na **entropia das permutações** (Hₒ). A ideia é medir o quanto a ordem de resposta de um aluno difere da ordem original proposta pelo professor (Leitão, 2017, p. 36).

- Valores mais próximos de `1` indicam maior desordem — ou seja, o estudante respondeu as questões em uma ordem significativamente diferente da ordem prevista. Isso pode indicar um estilo próprio de resolução ou até confusão na estrutura da atividade. Valores próximos de `0` indicam respostas mais alinhadas com a ordem esperada.

- Para calcular essa métrica corretamente, é necessário conhecer **duas ordens**:
  1. A **ordem original das questões** do quiz (a sequência em que foram apresentadas)
  2. A **ordem em que o aluno respondeu** às questões

- Contudo, **os statements xAPI do Moodle não incluem diretamente a ordem original das questões** dentro do quiz. Além disso, o campo `timestamp` pode não ter precisão suficiente para reconstruir a ordem de respostas. Por isso, recomenda-se usar o campo `stored`, que possui maior precisão temporal, como critério para ordenação.

- Os statements utilizados para esse cálculo devem conter o verbo:  
`http://adlnet.gov/expapi/verbs/answered`

Além disso, é necessário verificar a existência dos campos:
- `actor.account.name` (identificador do estudante)
- `object.id` (identificador da questão)
- `context.contextActivities.parent` (para agrupar as questões por tentativa de quiz)
- `stored` (para reconstruir a ordem das respostas com maior precisão)

**Importante:**  
Sem a ordem original das questões (fornecida, por exemplo, via integração com a API do Moodle ou por dados exportados do banco), não é possível calcular a métrica de desordem com precisão total. 

Veja um [exemplo de statement de resposta de quiz](statements-exemplos/statement_resposta_quiz.json).


### Métrica de Nível de Compreensão: