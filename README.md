# backend-elsa-tech-test

## Manual de instalación

### Clonar el repositorio

```bash
git clone https://github.com/DiegoOrtizS/backend-elsa-tech-test
cd backend-elsa-tech-test
```

### Instale versión de Python 3.11.9 o cree un entorno virtual

```bash
conda create -n elsa python=3.11.9 pip
conda activate elsa
```

### Instalar requerimientos

```bash
pip install -r requirements.txt
```

### Ejecutar migraciones

```bash
./scripts/migrate.sh
```

### Crear un superusuario

```bash
./scripts/createsuperuser.sh
```

## Instalar git hooks

```bash
./scripts/install-hooks.sh
```
