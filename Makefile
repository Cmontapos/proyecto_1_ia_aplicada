.PHONY: clean clean-processed clean-matrices clean-dataset clean-all help

help:
	@echo "Comandos disponibles:"
	@echo "  make clean-processed   - Borra imagenes_procesadas/"
	@echo "  make clean-matrices    - Borra datos_matrices.npz"
	@echo "  make clean-dataset     - Borra dataset_con_etiquetas.*"
	@echo "  make clean-preview     - Borra preview.png"
	@echo "  make clean-all         - Borra TODO lo anterior"
	@echo "  make clean             - Alias de clean-all"

clean-processed:
	@echo "Borrando imagenes procesadas..."
	rm -rf src/imagenes_procesadas/
	@echo "✓ Hecho"

clean-matrices:
	@echo "Borrando matrices (datos_matrices.npz)..."
	rm -f src/datos_matrices.npz
	@echo "✓ Hecho"

clean-dataset:
	@echo "Borrando datasets..."
	rm -f src/dataset_con_etiquetas.npz
	rm -f src/dataset_con_etiquetas.csv
	rm -f src/dataset_info.json
	rm -f src/etiquetas.json
	@echo "✓ Hecho"

clean-preview:
	@echo "Borrando preview..."
	rm -f preview.png
	@echo "✓ Hecho"

clean-all: clean-processed clean-matrices clean-dataset clean-preview
	@echo "Limpieza completa realizada"
	@echo "Se mantienen: src/imagenes_originales/"

clean: clean-all