bin_pip         = pip
bin_python      = python
venv_dir        = .venv
venv_bin        = $(venv_dir)/bin

bricklayer_cfg  = etc/bricklayer/bricklayer.ini.dev
bricklayer_env  = BRICKLAYERCONFIG=$(bricklayer_cfg)

clean:
	@find . -name '*.pyc' -delete

install_venv:
	$(bin_pip) install virtualenv

create_venv: install_venv
	virtualenv $(venv_dir)

bootstrap: create_venv
	$(venv_bin)/$(bin_pip) install -r pip-requires

test:
	@$(bricklayer_env) $(venv_bin)/nosetests $(TEST)

rest:
	BRICKLAYERCONFIG=etc/bricklayer/bricklayer.ini PYTHONPATH=bricklayer $(venv_bin)/twistd -ny bricklayer/rest.py --pidfile tmp/rest.pid

service:
	BRICKLAYERCONFIG=etc/bricklayer/bricklayer.ini PYTHONPATH=bricklayer $(venv_bin)/twistd -ny bricklayer/service.py --pidfile tmp/service.pid

console:
	PYTHONPATH=bricklayer $(venv_bin)/python