
# Guia de Build e Execução

Este documento contém os passos essenciais para levantar o ambiente de desenvolvimento (Moodle + Ralph LRS).

Para um guia detalhado, incluindo solução de problemas, importação de cursos e criação de usuários, consulte a **[Documentação Completa](https://github.com/utfpr-cm-dacom-bcc/learning-analytics/wiki/Guia-de-instala%C3%A7%C3%A3o)**.

## Pré-requisitos
* Docker & Docker Compose
* Git

## 1. Setup do Moodle (Docker)

Execute os comandos abaixo para baixar a imagem, configurar e iniciar o Moodle:

```bash
# 1. Variáveis de ambiente
export MOODLE_DOCKER_DB=mariadb
export MOODLE_DOCKER_WWWROOT=./moodle

# 2. Clonar repositório (Branch Stable)
git clone -b MOODLE_500_STABLE git://git.moodle.org/moodle.git $MOODLE_DOCKER_WWWROOT

# 3. Configuração
cp config.docker-template.php $MOODLE_DOCKER_WWWROOT/config.php

# 4. Iniciar Containers
bin/moodle-docker-compose up -d

# 5. Aguardar DB
bin/moodle-docker-wait-for-db
```

  * **Acesso:** [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)
  * **Instalação:** Siga os passos na tela (Timezone: `America/Sao_Paulo`).

## 2\. Setup do Ralph (LRS)

Em um terminal separado:

```bash
# 1. Clonar repositório
git clone [https://github.com/openfun/ralph.git](https://github.com/openfun/ralph.git)

# 2. Iniciar LRS
cd ralph
make run
```

*(Nota: Se houver erro de dependência no `pyproject.toml`, ajuste a versão do elasticsearch para `~=8.0.0`)*.

## 3\. Conexão de Rede (Bridge)

Para que o Moodle envie dados ao Ralph, ambos devem estar na mesma rede Docker:

```bash
docker network create ralph-moodle-net
docker network connect ralph-moodle-net ralph-app-1
docker network connect ralph-moodle-net moodle-web-1
```

*(Ajuste os nomes dos containers `ralph-app-1` e `moodle-web-1` se necessário, verificando com `docker ps`).*

## 4\. Configuração do Plugin

1.  Instale o plugin **Logstore xAPI** via interface do Moodle.
2.  Vá nas configurações do plugin e aponte para o Ralph:
      * **Endpoint:** `http://ralph-app-1:8100/xAPI/statements`
      * **Username:** `ralph`
      * **Password:** `secret`
