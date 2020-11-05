# First try with python
{
  pip uninstall coronacli
} ||
{ # If python fails, try with python3
  pip3 uninstall coronacli
}
rm -rf ./.eggs ./build ./dist ./.pytest_cache ./.coverage ./test_dir* coronadb *.egg*