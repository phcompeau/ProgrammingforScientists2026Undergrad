import multiprocessing   # will facilitate parallelism
import time

def main():
    print("Parallel and concurrent programming in Python.")

    # by default, Python will use only core unless we tell it not to (e.g., with multiprocessing)
    # some languages are not this way, meaning that the languages are inherently CONCURRENT -- serial programs run on multiple cores cannot be parallel

    # first question: how many cores do we have available?
    print("Number of cores on this computer:", multiprocessing.cpu_count())

    # sum_example_two_procs()

    # sum_example_multiple_procs()

    timing_comparison_serial_vs_multi_procs(1000000000)

def timing_comparison_serial_vs_multi_procs(n:int):
    data = list(range(1, n+1))
    num_procs = multiprocessing.cpu_count()

    # time the parallel approach
    start_parallel = time.time()
    sum_multi_procs(data, num_procs)
    end_parallel =time.time()
    total_parallel = end_parallel - start_parallel
    print(f"Sum of first {n} integers using {num_procs} processes is: {total_parallel}")

    # time the serial approach
    start_serial = time.time()
    sum(data)
    # sum_multi_procs(data, 1) # a serial algorithm in disguise as a parallel one
    end_serial =time.time()
    total_serial = end_serial - start_serial
    print(f"Sum of first {n} integers using serial computing is: {total_serial}")

    print(f"Speedup provided by parallel approach: {total_serial/total_parallel}")    



def sum_example_multiple_procs():
    # we would rather split a problem into a number of pieces that is equal to the number of processors available 

    # let's get some data 
    n = 100
    data = list(range(1, n+1)) # gives me [1, ..., n]

    # get num of cores
    num_procs = multiprocessing.cpu_count()

    total = sum_multi_procs(data, num_procs)

    print(f"Sum of first {n} integers using {num_procs} processes is: {total}")

    # NOTE: THIS FUNCTION IS SERIAL
    # the parallelism is going to be in SUBROUTINE

def sum_multi_procs(data: list[int], num_procs:int) -> int:
    """
    Divides the work of summing all values in a list over num_procs concurrent (and hopefully parallel) processes.
    """
    # divide the data into equally sized chunks

    # how big should each sublist be?
    chunk_size = len(data) // num_procs

    # need to be aware that num_procs * chunk_size may be < len(data)

    # make a list containing the sublists that I want
    data_slices: list[list[int]] = []
    for i in range(num_procs):
        start_index = i * chunk_size
        end_index = (i+1) * chunk_size

        if i == num_procs - 1:
            # final process, end_index should be end of data 
            end_index = len(data)

        current_list = data[start_index:end_index]
        data_slices.append(current_list)
    
    # we now know which component of the data each process is responsible for 

    # make a queue to store results
    result_queue = multiprocessing.Queue()

    # next, create num_procs processes in a list 

    processes: list[multiprocessing.Process] = []

    # range over all the data slices and start processes 
    for slice in data_slices:
        p = multiprocessing.Process(target = partial_sum, args = (slice, result_queue))
        processes.append(p) # add it this process to list 
        p.start() # start process 
        # p.join() # this is horrendous. What would happen is WAITING until p finishes for this line to execute


    # processes are running, and let's go in and get them when they're done

    for p in processes: # this has num_procs processes in it
        # collect the results
        # first time through the loop, this WAITS until the first process to finish has completed 
        p.join()

    # I can't make it here until all processes are done 

    # I have control back, and now we can do serial programming to show the results 
    total_sum = 0

    for _ in range(num_procs):
        # get val from queue and add it to total_sum
        total_sum += result_queue.get()

    return total_sum

def sum_serial(data: list[int]) -> int:
    """
    Hopefully an easy function.
    """
    s = 0

    for element in data:
        s += element

    return s

def sum_example_two_procs():
    # we're going back to our Gauss example of summing first n integers 
    
    # let's get some data 
    n = 100
    data = list(range(1, n+1)) # gives me [1, ..., n]

    # to divide our work, split the data into two halves 
    mid = len(data) // 2

    # make a list containing two sublists that we want 
    data_slices = [data[:mid], data[mid:]]

    # create a "queue" to collect the results of two different processes that will each sum the values in a sublist 
    # a "queue" is like an array/list, but it's going to be a "safe" structure for communications w/parallel programming 
    # Friday's recitation will be on stacks and queues 

    # the results from each process that we run in parallel are going to be added to a queue
    result_queue = multiprocessing.Queue()
    # this is a Queue object 
    
    # create two processes, one for each sublist 
    # these are our workers 
    # the workers take two things as input: the function name (target), and the arguments (args) as a TUPLE
    # args in this case are the slice of the list we care about and the queue to put the result into
    p0 = multiprocessing.Process(target = partial_sum, args = (data_slices[0], result_queue))

    p1 = multiprocessing.Process(target = partial_sum, args = (data_slices[1], result_queue))

    # at this point, we just defined p0 and p1 as process objects 
    # now, run them 
    p0.start()
    p1.start()

    # this is your first ever parallel program as of now
    # it's also CONCURRENT -- because it will run on one core -- and because there is task coordination

    # we will call join() to wait for process to finish 
    p0.join()
    # this doesn't proceed (it's called blocking) within this function until p0 finishes

    p1.join()
    # occurs when p1 is finished (or if p1 finishes p0, it will happen instantaneously)

    # it doesn't matter which one finishes first
    # if I make it here, all I care about is that >>> they're both done

    # so they are both in the queue 
    # if I cared about which one got in first, I would need to put into the queue the value and also a label so I know which value is which
    # in this case I don't care 

    # collect the results from the queue
    val_a = result_queue.get() # which process does this correspond to? the one that finishes first (FIFO) and IDC
    val_b = result_queue.get()

    print("Sum of array elements is", val_a + val_b) 



def partial_sum(data_slice: list[int], result_queue: multiprocessing.Queue) -> None:
    """
    Takes as input a list of integers and a Queue.
    It puts the sum of the list into the Queue.
    """
    # note: when we move to parallel programming, we no longer are returning values.
    # we put them into the queue for someone else to remove when they are ready
    val = sum(data_slice)
    # put this into the queue 
    result_queue.put(val)


if __name__ == "__main__":
    main()
