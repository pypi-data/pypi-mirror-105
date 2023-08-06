import sys
from os.path import join
from click.testing import CliRunner
sys.path.append(join('..', '..', 'pydoni'))

from api import Goodreads


def test_goodreads_search():
  runner = CliRunner()

  # Have to somehow test class method
  result = runner.invoke(hello, [])
  import pdb; pdb.set_trace()

  assert result.exit_code == 0

  assert result.output == 'Hello Peter!\n'