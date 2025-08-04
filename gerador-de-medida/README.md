# Calculo de métricas

Este projeto em Python realiza o cálculo de métricas educacionais a partir de dados extraídos da ferramenta Ralph, que coleta statements no formato xAPI.

## Métricas proposta por leitão (2017)

As métricas implementadas seguem as definições propostas por Leitão (2017) em sua pesquisa sobre análise de desempenho de estudantes com base em dados educacionais.

### Métrica de Pontuação:

- Essa é uma métrica clássica que calcula a média de pontuação obtida por um estudante em atividades avaliativas.

- Os statements utilizados para esse cálculo devem conter o verbo:
`http://adlnet.gov/expapi/verbs/completed`

Também é necessário verificar a existência dos campos `actor` e `result.score.raw` em cada *statement*, pois páginas apenas visualizadas/completadas por alunos podem conter o mesmo verbo, mas não possuem pontuação associada — e, portanto, não devem ser consideradas nessa métrica.

### Métrica de ...