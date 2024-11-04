# FASTAPI - EXAMPLE

## Comandos de Migração com Alembic

### Criar uma Migração Manualmente

Para criar uma nova migração manualmente, use o seguinte comando:

```bash
alembic revision -m "Descrição da Migração"
```

Este comando cria um novo arquivo de migração em branco, onde você pode definir as alterações no esquema do banco de dados.

### Criar uma Migração com Autogeração

Para gerar automaticamente uma migração baseada nas mudanças detectadas nos modelos, utilize:

```bash
alembic revision --autogenerate -m "Descrição da Migração"
```

Esse comando compara o estado atual dos modelos com o estado do banco de dados e gera as instruções de migração necessárias.

### Aplicar a Migração Mais Recente

Para aplicar a última migração criada ao banco de dados, execute:

```bash
alembic upgrade head
```

Este comando aplica todas as migrações pendentes até a versão mais recente.

### Reverter a Última Migração

Se precisar desfazer a última migração aplicada, use:

```bash
alembic downgrade -1
```

Esse comando reverte a última migração, voltando o banco de dados ao estado anterior.

## Executando o Celery

Para iniciar o worker do Celery, utilize o seguinte comando:

```bash
celery --app celery_app.config.app worker --loglevel=info --pool=solo
```

### Explicação dos parâmetros:

- **`--app celery_app.config.app`**: Especifica o caminho do módulo onde o objeto `Celery` está configurado. No caso, o Celery está sendo configurado no módulo `celery_app.config` no objeto `app`.
- **`worker`**: Indica que você deseja iniciar um worker Celery, que processará as tarefas enfileiradas.

- **`--loglevel=info`**: Define o nível de log como `info`, o que significa que o worker irá registrar mensagens informativas, além de avisos e erros.

- **`--pool=solo`**: Força o Celery a usar o pool de tarefas "solo", que é um modo de execução de tarefas em série e sem múltiplos processos. Esse modo é útil em ambientes como Windows, onde o uso de outros pools pode não ser compatível, ou quando se deseja simplificar a execução para fins de depuração.
