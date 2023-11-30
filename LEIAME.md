### Instalação das bibliotecas necessárias
------------------------------------
Antes de executar um código Python, garanta
que todas as bibliotecas necessárias estão instaladas executando
o comando

    pip install -r requirements.txt

O pip normalmente já vem instalado com o Python (caso o
download do Python seja feito no site oficial). Caso você não
tenha o pip instalado, vá [neste link](https://pip.pypa.io/en/stable/installation/).

### Execução dos códigos Python
-------------------------------
Para executar um código Python, basta usar o comando

    python3 <arquivo>.py

Caso você não tenha o Python instalado,
basta fazer o download [neste link](https://www.python.org/downloads/).

### Execução dos códigos Fortran
-------------------------------
Para executar um código Fortran, primeiro é necessário
compilar, usando o comando

    gfortran <arquivo>.f90

e depois executar, usando o comando

    ./a.out

Caso você não tenha o GFortran instalado, basta
seguir o passo a passo [neste link](https://fortran-lang.org/learn/os_setup/install_gfortran/).

### Compilação dos arquivos LaTeX
--------------------------------
Caso queira, você pode compilar o(s) arquivo(s)
.tex usando o comando abaixo no diretório em que o
arquivo estiver.

    ./build.sh <arquivo>.tex