import threading
  
lock = threading.Lock()
  
def thread_test(num):
    phrase = "I am number " + str(num)
    with lock:
        print(phrase)
        f.write(phrase + "\n")
 
  
threads = []
f = open("text.txt", 'w')
for i in range (100):
    t = threading.Thread(target = thread_test, args = (i,))
    threads.append(t)
    t.start()
  
while threading.activeCount() > 1:
    pass
else:
    f.close()