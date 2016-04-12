FILE = paper
BIBS = Annexes/biblio.bib

$(FILE).pdf: $(FILE).tex $(BIBS)
	pdflatex   --shell-escape $(FILE)
	bibtex $(FILE)
	pdflatex   --shell-escape $(FILE)	
	bibtex $(FILE)
	pdflatex   --shell-escape $(FILE)
	
clean:
	rm -f  $(FILE).pdf $(FILE).aux $(FILE).bbl $(FILE).blg $(FILE).log $(FILE).out $(FILE).toc $(FILE).ind $(FILE).ilg $(FILE).cb $(FILE).idx $(FILE).dvi $(FILE).ps *~ figs/*-converted-to.pdf

