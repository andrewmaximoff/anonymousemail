import os
import anonymousemail

is_test_run = 'TEST' in os.environ

if __name__ == '__main__' and not is_test_run:
    anonymousemail.app.run()
