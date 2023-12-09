# A equação do calor e o problema da adega
------------------------------------------

Este repositório armazena o trabalho final do curso de Introdução a
Métodos Computacionais em Equações Diferenciais Parciais (IMCEDP) do
Programa de Pós-Graduação em Matemática (PPGMAT),
ministrado pelo prof. Dr. Yuri Dumaresq Sobral no segundo semestre letivo
de 2023 da Universidade de Brasília.
O objetivo do trabalho foi resolver, numericamente, a equação do calor.

Resolvemos a equação do calor usando os métodos de Euler explícito
e de Crank-Nicolson. Os algoritmos estão implementados em Python
e Fortran (para a validação da ordem do algoritmo de ordem).
Abaixo seguem instruções de compilação/execução dos scripts.

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

### Rotinas
------------------------------------------------
O arquivo `exp-euler.py` contém a solução do problema, para
$\kappa$ constante, usando o método de Euler explícito. Analogamente
para o arquivo `crank-nicolson.py`. O arquivo `exp-euler.f90` traz
a validação (manual) da ordem do método de Euler explícito, que é
traçada usando a rotina `exp-euler.gnu`. Por fim, a rotina `FVM.py`
traz a solução do problema para $\kappa(x) = (6.3 + x)^{\alpha}$,
com $\alpha = 1,2$, usando um método de volumes finitos.