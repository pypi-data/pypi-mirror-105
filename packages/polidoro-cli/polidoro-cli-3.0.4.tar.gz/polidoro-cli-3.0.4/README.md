# Custom CLI
### To install

```
sudo apt install python3-pip -y
pip3 install polidoro_cli
```

Then add to your `.bashrc`
```
export PATH="$PATH:$HOME/.local/bin/"
```

### To use:
`cli --help`

### Tips:
Create alias:

Add in your `.bashrc`
```
alias dk='cli docker'
alias ex='cli elixir'
alias rb='cli ruby'
```

### Commands:
#### Docker `cli docker COMMAND` or `dk COMMAND`
```
stop_all    Stop all containers
ps          Run "docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}""
up          Run "docker-compose up"
down        Run "docker-compose down"
exec        Run "docker-compose exec $service"
bash        Run "docker-compose exec $service bash"
stop        Run "docker-compose stop"
logs        Run "docker-compose logs $service"
run         Run "docker-compose run --rm $service"
```
The CLI will replace `$service` for the first argument um command line, if is a valid service, 
or will use the first service with `build` in `docker-compose.yml`

Example:
```
/home/workspace/my_project$ dk bash
+ docker-compose my_project_service bash

/home/workspace/my_project$ dk web bash
+ docker-compose exec web bash

```

#### Elixir `cli elixir COMMAND` or `ex COMMAND`
```
compile     Run "$docker mix compile"
credo       Run "$docker mix credo"
deps        Run "$docker mix deps.get"
iex         Run "$docker iex -S mix"
iexup       Run "$docker iex -S mix phx.server"
test        Run "MIX_ENV=test mix test"
setup       Run "$docker mix ecto.setup"
reset       Run "$docker mix ecto.reset"
migrate     Run "$docker mix ecto.migrate"
up          Run "$docker mix phx.server"
schema      Run "$docker mix phx.gen.schema"
gettext     Run "$docker mix gettext.extract --merge"
```
The CLI will replace the `$docker` for `docker-compose exec $service` 
if the parameter `-d/--docker` is in the command line
```
/home/workspace/my_project$ ex iex
+ iex -S mix

/home/workspace/my_project$ ex iex -d
+ docker exec -it my_project_service iex -S mix
```

#### Ruby `cli ruby COMMAND` or `rb COMMAND`
```
console (c)     Run "$docker bundle exec rails console"
migrate (dbm)   Run "$docker bundle exec rails db:migrate"
create (dbc)    Run "$docker bundle exec rails db:create"
bundle (b)      Run "$docker bundle install"
```
The CLI will replace the `$docker` for `docker-compose exec $service`
if the parameter `-d/--docker` is in the command line
