#!/usr/bin/env sh
set -eu

echo "[boot] Iniciando boot do EdVenturers..."

# 1) Carregar .env se existir (sem erro se não existir)
if [ -f ".env" ]; then
  set -a
  . ./.env
  set +a
fi

# 2) Diretório persistente para a 'instance/'
INSTANCE_PATH="${INSTANCE_PATH:-/var/data/instance}"
echo "[boot] INSTANCE_PATH='${INSTANCE_PATH}'"

# 3) Garantir pasta persistente e symlink local ./instance -> $INSTANCE_PATH
mkdir -p "${INSTANCE_PATH}"
if [ -d "instance" ] && [ ! -L "instance" ]; then
  echo "[boot] Migrando conteúdo existente de ./instance para ${INSTANCE_PATH}..."
  cp -a instance/. "${INSTANCE_PATH}/" 2>/dev/null || true
  rm -rf "instance"
fi
if [ -L "instance" ] || [ -e "instance" ]; then
  rm -rf "instance"
fi
ln -s "${INSTANCE_PATH}" "instance"
echo "[boot] Symlink criado: ./instance -> ${INSTANCE_PATH}"

# 4) Ambiente de produção
export FLASK_ENV="${FLASK_ENV:-production}"
export PYTHONUNBUFFERED=1

# 5) Rodar upgrade de banco (idempotente)
if [ -f "upgrade_banco.py" ]; then
  echo "[boot] Executando upgrade_banco.py..."
  python upgrade_banco.py || echo "[boot] Aviso: upgrade_banco.py retornou código de erro, seguindo assim mesmo."
else
  echo "[boot] upgrade_banco.py não encontrado; seguindo sem upgrade."
fi

# 6) Subir Gunicorn
# Observação: $PORT costuma ser injetado pelo PaaS; usa 8000 localmente se não existir.
PORT="${PORT:-8000}"
echo "[boot] Subindo Gunicorn na porta ${PORT}..."
exec gunicorn -w 2 -k gthread -b 0.0.0.0:"${PORT}" main:app
