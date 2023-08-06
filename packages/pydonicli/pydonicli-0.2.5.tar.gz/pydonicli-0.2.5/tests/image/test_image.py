from os.path import join
from click.testing import CliRunner

import sys
sys.path.append(join('..', '..', 'src', 'commands', 'image'))
from ocr import ocr


def test_ocr():
  runner = CliRunner()
  result = runner.invoke(ocr, [join('ocr', 'sample_image_to_ocr.png')])
  import pdb; pdb.set_trace()

  assert result.exit_code == 0

  assert result.output == 'Hello Peter!\n'