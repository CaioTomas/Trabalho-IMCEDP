# Uso (apenas no Linux):
#	0.	Dê permissão a este .sh a ser executado como programa
#	1.	Coloque este .sh na pasta com o .tex do thesis, digamos "thesis.tex" 
#	2.	Abra a pasta no terminal
#	3.	Execute na limha de comando "./build.sh thesis" 
#	4.	Se a compilação não tiver erros, o pdf aparecerá em breve.
#	---

#	Etapa 1: compilação de fato
pdflatex    -interaction=nonstopmode $1.tex							    # primeira passagem
makeindex                            $1.idx							    # 
makeindex                            $1.nlo -s nomencl.ist -o $1.nls	# resolve listas de nomenclatura
biber                                $1.bcf							    # resolve citações
pdflatex    -interaction=nonstopmode $1.tex							    # segunda passagem
pdflatex    -interaction=nonstopmode $1.tex							    # terceira passagem

#	Etapa 2: remoção de arquivos temporários na pasta do nome.tex
rm          $1.aux
rm          $1.bbl
rm          $1.bcf
rm          $1.blg
rm          $1.idx
rm          $1.ilg
rm          $1.ind
rm          $1.lof
rm          $1.log
rm          $1.lot
rm          $1.nlo
rm          $1.nls
rm          $1.run.xml
rm          $1.toc

#	Etapa 3: abre o pdf e limpa o terminal
# open        $1.pdf
clear -x
