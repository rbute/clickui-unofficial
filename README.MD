
# Unofficial Click UI 

## Usage

```python
from clickui import make_ui # This one is from this framework
import click 

# Decorate your existing click command if you need an UI
@make_ui 
@click.command('Sample Command')
def sample_command():
    pass
```
## Screenshot
![Convert Click command to UI](screenshots/Screenshot_from_2020-05-23_14-39-17.png)
