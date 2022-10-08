from threading import Thread
import time
def secondf():
_time.sleep(5)
_print('secondf')

def main():
_Thread(target=secondf).start()
_return "ok"

print(main())
print(main())