# TLDR

Practicing for video

##

```sh
cd anthropic-python-sdk
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install uv
uv -V
uv init
uv run hello.py
uv add agentops anthropic packaging python-dotenv # and peep L7 of the pyproject.toml file
touch .env
echo "ANTHROPIC_API_KEY=" > .env # and copy in your ANTHROPIC_API_KEY
```

In the name of OCD, let's delete the `hello.py` file and create an `examples` folder with a `1.py` file that will hold the first example we will now walk through...

```sh
rm hello.py
mkdir examples
touch examples/1.py
```

