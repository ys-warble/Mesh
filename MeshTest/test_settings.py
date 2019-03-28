import os

# Test Plot
auto_open = False

# Test Output
actual_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output', 'actual')
expected_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output', 'expected')

# Test Property
start_title_format = lambda test_name: '|' + (' START %s ' % test_name).center(80, '=') + '|'
end_title_format = lambda test_name: '|' + ('  END %s  ' % test_name).center(80, '=') + '|'
